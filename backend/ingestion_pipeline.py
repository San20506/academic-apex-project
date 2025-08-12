#!/usr/bin/env python3
"""
Ingestion Pipeline for Academic Apex Strategist

Handles document processing, OCR, and text extraction with Tesseract fallback.
"""

import os
import logging
import asyncio
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
import subprocess
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IngestionPipeline:
    """
    Document ingestion pipeline with OCR capabilities.
    
    Supports PDF, image files, and plain text with Tesseract OCR fallback.
    """
    
    def __init__(self):
        """Initialize the ingestion pipeline."""
        self.supported_types = {
            'application/pdf': self._process_pdf,
            'image/jpeg': self._process_image,
            'image/png': self._process_image,
            'image/gif': self._process_image,
            'text/plain': self._process_text
        }
        
        # Check for Tesseract installation
        self.tesseract_available = self._check_tesseract()
        if not self.tesseract_available:
            logger.warning("⚠ Tesseract not found - OCR functionality will be limited")
            
        # Check for PyMuPDF for PDF processing
        self.pymupdf_available = self._check_pymupdf()
        if not self.pymupdf_available:
            logger.warning("⚠ PyMuPDF not found - PDF processing will be limited")
    
    def _check_tesseract(self) -> bool:
        """Check if Tesseract is available."""
        try:
            subprocess.run(['tesseract', '--version'], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL, 
                         check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _check_pymupdf(self) -> bool:
        """Check if PyMuPDF is available."""
        try:
            import fitz  # PyMuPDF
            return True
        except ImportError:
            return False
    
    async def process_document(self, file_path: Path) -> Dict[str, Any]:
        """
        Process a document and extract text.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Dict containing extracted text and metadata
        """
        start_time = time.time()
        
        try:
            # Detect file type
            content_type = self._detect_content_type(file_path)
            
            if content_type not in self.supported_types:
                return {
                    'success': False,
                    'error': f'Unsupported file type: {content_type}',
                    'processing_time': time.time() - start_time
                }
            
            # Process with appropriate handler
            processor = self.supported_types[content_type]
            result = await processor(file_path)
            
            # Add timing information
            result['processing_time'] = time.time() - start_time
            result['file_size'] = file_path.stat().st_size
            result['content_type'] = content_type
            
            logger.info(f"Document processed: {file_path.name} "
                       f"({result.get('text_length', 0)} chars, "
                       f"{result['processing_time']:.2f}s)")
            
            return result
            
        except Exception as e:
            logger.error(f"Document processing error: {e}")
            return {
                'success': False,
                'error': str(e),
                'processing_time': time.time() - start_time
            }
    
    def _detect_content_type(self, file_path: Path) -> str:
        """Detect file content type."""
        suffix = file_path.suffix.lower()
        
        type_map = {
            '.pdf': 'application/pdf',
            '.txt': 'text/plain',
            '.md': 'text/plain',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif'
        }
        
        return type_map.get(suffix, 'application/octet-stream')
    
    async def _process_text(self, file_path: Path) -> Dict[str, Any]:
        """Process plain text files."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            return {
                'success': True,
                'text': text,
                'text_length': len(text),
                'confidence': 1.0,  # Plain text has 100% confidence
                'method': 'direct_text'
            }
            
        except UnicodeDecodeError:
            # Try different encodings
            for encoding in ['latin-1', 'cp1252']:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        text = f.read()
                    
                    return {
                        'success': True,
                        'text': text,
                        'text_length': len(text),
                        'confidence': 0.9,  # Slightly lower confidence
                        'method': f'text_{encoding}',
                        'warning': f'Used {encoding} encoding'
                    }
                except UnicodeDecodeError:
                    continue
            
            return {
                'success': False,
                'error': 'Unable to decode text file with any supported encoding'
            }
    
    async def _process_pdf(self, file_path: Path) -> Dict[str, Any]:
        """Process PDF files."""
        if self.pymupdf_available:
            return await self._process_pdf_pymupdf(file_path)
        else:
            return await self._process_pdf_fallback(file_path)
    
    async def _process_pdf_pymupdf(self, file_path: Path) -> Dict[str, Any]:
        """Process PDF using PyMuPDF."""
        try:
            import fitz
            
            doc = fitz.open(file_path)
            text_parts = []
            page_count = len(doc)
            
            for page_num in range(page_count):
                page = doc.load_page(page_num)
                text = page.get_text()
                
                if text.strip():
                    text_parts.append(f"--- Page {page_num + 1} ---\n{text}")
                else:
                    # Try OCR for pages with no text (scanned pages)
                    if self.tesseract_available:
                        pix = page.get_pixmap()
                        img_data = pix.tobytes("png")
                        
                        # Save to temp file and OCR
                        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                            tmp.write(img_data)
                            tmp_path = Path(tmp.name)
                        
                        try:
                            ocr_text = await self._ocr_image(tmp_path)
                            if ocr_text.strip():
                                text_parts.append(f"--- Page {page_num + 1} (OCR) ---\n{ocr_text}")
                        finally:
                            tmp_path.unlink()
            
            doc.close()
            
            full_text = "\n\n".join(text_parts)
            
            return {
                'success': True,
                'text': full_text,
                'text_length': len(full_text),
                'confidence': 0.9,
                'method': 'pymupdf',
                'pages': page_count
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'PyMuPDF processing failed: {str(e)}'
            }
    
    async def _process_pdf_fallback(self, file_path: Path) -> Dict[str, Any]:
        """Fallback PDF processing using system tools."""
        return {
            'success': False,
            'error': 'PDF processing requires PyMuPDF (pip install PyMuPDF)'
        }
    
    async def _process_image(self, file_path: Path) -> Dict[str, Any]:
        """Process image files with OCR."""
        if not self.tesseract_available:
            return {
                'success': False,
                'error': 'OCR requires Tesseract (install tesseract-ocr)'
            }
        
        try:
            text = await self._ocr_image(file_path)
            
            return {
                'success': True,
                'text': text,
                'text_length': len(text),
                'confidence': 0.8,  # OCR typically has lower confidence
                'method': 'tesseract_ocr'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'OCR processing failed: {str(e)}'
            }
    
    async def _ocr_image(self, image_path: Path) -> str:
        """Perform OCR on an image using Tesseract."""
        try:
            # Run Tesseract
            result = subprocess.run([
                'tesseract', str(image_path), 'stdout', 
                '--psm', '3',  # Fully automatic page segmentation
                '--oem', '3'   # Use both neural nets LSTM and legacy engine
            ], capture_output=True, text=True, check=True)
            
            return result.stdout.strip()
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Tesseract OCR failed: {e}")
            return ""
    
    def get_supported_types(self) -> List[str]:
        """Get list of supported content types."""
        return list(self.supported_types.keys())
    
    def validate_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Validate a file for processing.
        
        Args:
            file_path: Path to validate
            
        Returns:
            Dict with validation result
        """
        if not file_path.exists():
            return {
                'valid': False,
                'error': 'File does not exist'
            }
        
        if not file_path.is_file():
            return {
                'valid': False,
                'error': 'Path is not a file'
            }
        
        content_type = self._detect_content_type(file_path)
        if content_type not in self.supported_types:
            return {
                'valid': False,
                'error': f'Unsupported file type: {content_type}',
                'supported_types': self.get_supported_types()
            }
        
        # Check file size (limit to 50MB)
        size = file_path.stat().st_size
        max_size = 50 * 1024 * 1024  # 50MB
        
        if size > max_size:
            return {
                'valid': False,
                'error': f'File too large: {size / (1024*1024):.1f}MB (max: 50MB)'
            }
        
        return {
            'valid': True,
            'content_type': content_type,
            'size': size
        }


async def test_ingestion_pipeline():
    """Test the ingestion pipeline."""
    pipeline = IngestionPipeline()
    
    print("🧪 Testing Ingestion Pipeline")
    print("=" * 50)
    
    # Test with a simple text file
    test_content = """# Test Document

This is a test document for the Academic Apex Strategist ingestion pipeline.

## Features Tested
- Text extraction
- File processing
- Error handling

The system should be able to process this content correctly.
"""
    
    # Create test file
    test_dir = Path("test_ingestion")
    test_dir.mkdir(exist_ok=True)
    
    test_file = test_dir / "test_document.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    try:
        # Test validation
        validation = pipeline.validate_file(test_file)
        print(f"✓ File validation: {validation}")
        
        # Test processing
        result = await pipeline.process_document(test_file)
        print(f"✓ Processing result: {result.get('success', False)}")
        print(f"  - Text length: {result.get('text_length', 0)} chars")
        print(f"  - Processing time: {result.get('processing_time', 0):.3f}s")
        print(f"  - Method: {result.get('method', 'unknown')}")
        
        # Test capabilities
        print(f"\n📊 Pipeline Capabilities:")
        print(f"  - Tesseract OCR: {'✓' if pipeline.tesseract_available else '✗'}")
        print(f"  - PyMuPDF (PDF): {'✓' if pipeline.pymupdf_available else '✗'}")
        print(f"  - Supported types: {', '.join(pipeline.get_supported_types())}")
        
        print("\n🎉 Ingestion pipeline test completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    finally:
        # Cleanup
        if test_file.exists():
            test_file.unlink()
        if test_dir.exists():
            test_dir.rmdir()


if __name__ == "__main__":
    asyncio.run(test_ingestion_pipeline())
