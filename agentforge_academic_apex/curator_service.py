#!/usr/bin/env python3
"""
Curator Service for Academic Apex Strategist

MIT License

Copyright (c) 2025 Academic Apex Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
"""

import os
import logging
from typing import Dict, Any, Tuple
from flask import Flask, request, jsonify
from ollama_adapter import OllamaAdapter


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Flask app initialization
app = Flask(__name__)

# Get configuration from environment
CURATOR_MODEL = os.getenv('CURATOR_MODEL', 'mistral-7b')
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')

# Initialize Ollama adapter for curator model
curator_adapter = OllamaAdapter(base_url=OLLAMA_HOST, model=CURATOR_MODEL)


def validate_request_data(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate incoming request data.
    
    Args:
        data: Request JSON data
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(data, dict):
        return False, "Request data must be JSON object"
    
    if 'prompt' not in data:
        return False, "Missing required field 'prompt'"
    
    if not isinstance(data['prompt'], str):
        return False, "Field 'prompt' must be a string"
    
    if len(data['prompt'].strip()) == 0:
        return False, "Field 'prompt' cannot be empty"
    
    if len(data['prompt']) > 10000:  # Reasonable limit
        return False, "Field 'prompt' too long (max 10,000 characters)"
    
    # Instruction is optional
    if 'instruction' in data and not isinstance(data['instruction'], str):
        return False, "Field 'instruction' must be a string"
    
    return True, ""


def curate_prompt(prompt: str, instruction: str = "") -> Dict[str, Any]:
    """
    Curate and refine a prompt using the curator model.
    
    Args:
        prompt: Original prompt text
        instruction: Optional instruction for refinement
        
    Returns:
        Dict containing the refined prompt and metadata
    """
    try:
        # Build curation prompt
        if instruction.strip():
            curation_prompt = f"""You are a prompt curator. Your task is to refine and improve prompts for better clarity and effectiveness.

INSTRUCTION: {instruction}

ORIGINAL PROMPT:
{prompt}

REFINED PROMPT:"""
        else:
            curation_prompt = f"""You are a prompt curator. Your task is to refine and improve prompts for better clarity, specificity, and effectiveness while maintaining the original intent.

ORIGINAL PROMPT:
{prompt}

Please provide a refined version that is:
1. More specific and clear
2. Better structured
3. More actionable

REFINED PROMPT:"""
        
        # Generate refined prompt using curator model
        logger.info(f"Curating prompt with model {CURATOR_MODEL}")
        result = curator_adapter.generate(
            curation_prompt,
            max_tokens=2048,
            temperature=0.3  # Lower temperature for more consistent refinement
        )
        
        refined_text = result["text"].strip()
        
        # Extract just the refined prompt if it contains extra formatting
        if "REFINED PROMPT:" in refined_text:
            refined_text = refined_text.split("REFINED PROMPT:")[-1].strip()
        
        logger.info("Prompt curation successful")
        
        return {
            "refined": refined_text,
            "original_length": len(prompt),
            "refined_length": len(refined_text),
            "curator_model": CURATOR_MODEL,
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Prompt curation failed: {e}")
        
        # Fallback: return original prompt unchanged
        return {
            "refined": prompt,
            "original_length": len(prompt),
            "refined_length": len(prompt),
            "curator_model": CURATOR_MODEL,
            "success": False,
            "error": str(e),
            "fallback": True
        }


@app.route('/api/curate', methods=['POST'])
def curate_endpoint():
    """
    POST /api/curate - Curate and refine a prompt.
    
    Request JSON:
    {
        "prompt": "text to refine",
        "instruction": "optional instruction for refinement"  
    }
    
    Response JSON:
    {
        "refined": "refined prompt text",
        "original_length": 123,
        "refined_length": 145,
        "curator_model": "mistral-7b",
        "success": true
    }
    """
    try:
        # Parse request data
        data = request.get_json(force=True)
        if data is None:
            return jsonify({"error": "Invalid JSON data"}), 400
        
        # Validate input
        is_valid, error_msg = validate_request_data(data)
        if not is_valid:
            return jsonify({"error": error_msg}), 400
        
        # Extract parameters
        prompt = data['prompt'].strip()
        instruction = data.get('instruction', '').strip()
        
        logger.info(f"Received curation request: {len(prompt)} chars, instruction: {bool(instruction)}")
        
        # Curate the prompt
        result = curate_prompt(prompt, instruction)
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Curation endpoint error: {e}")
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500


@app.route('/healthz', methods=['GET'])
def health_check():
    """
    GET /healthz - Health check endpoint.
    
    Returns system status including Ollama connectivity.
    """
    try:
        # Test Ollama connection
        ollama_healthy = curator_adapter.test_connection()
        
        # Get available models
        models_info = curator_adapter.list_models()
        
        status = {
            "status": "healthy" if ollama_healthy else "degraded",
            "curator_model": CURATOR_MODEL,
            "ollama_host": OLLAMA_HOST,
            "ollama_connected": ollama_healthy,
            "available_models": len(models_info.get('models', [])),
            "service": "curator-service"
        }
        
        return jsonify(status), 200 if ollama_healthy else 503
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "service": "curator-service"
        }), 503


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "error": "Not found",
        "message": "The requested endpoint does not exist"
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({
        "error": "Method not allowed",
        "message": "The requested method is not allowed for this endpoint"
    }), 405


def validate_model_availability() -> bool:
    """
    Validate that the curator model is available in Ollama.
    
    Returns:
        True if model is available, False otherwise
    """
    try:
        models_info = curator_adapter.list_models()
        available_models = [model['name'] for model in models_info.get('models', [])]
        
        if CURATOR_MODEL in available_models:
            logger.info(f"✓ Curator model '{CURATOR_MODEL}' is available")
            return True
        else:
            logger.warning(f"✗ Curator model '{CURATOR_MODEL}' not found")
            logger.warning(f"Available models: {', '.join(available_models)}")
            logger.warning("Service will attempt to use the specified model anyway")
            return False
            
    except Exception as e:
        logger.error(f"Failed to validate model availability: {e}")
        return False


if __name__ == '__main__':
    logger.info(f"Starting Curator Service...")
    logger.info(f"Curator Model: {CURATOR_MODEL}")
    logger.info(f"Ollama Host: {OLLAMA_HOST}")
    
    # Test connection on startup
    if curator_adapter.test_connection():
        logger.info("✓ Ollama connection successful")
        
        # Validate model availability
        validate_model_availability()
        
    else:
        logger.warning("✗ Ollama connection failed - service will run in fallback mode")
    
    # Start Flask server
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=False,
        threaded=True
    )
