#!/usr/bin/env python3
"""
Obsidian Adapter for Academic Apex Strategist

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
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any


class ObsidianAdapter:
    """
    Adapter for creating and managing notes in an Obsidian vault.
    
    Handles creation of study plans, notes, and academic content with
    proper organization and timestamping.
    """
    
    def __init__(self, vault_path: str):
        """
        Initialize the ObsidianAdapter.
        
        Args:
            vault_path: Path to the Obsidian vault directory
            
        Raises:
            ValueError: If vault path is invalid
        """
        self.vault_path = Path(vault_path).resolve()
        self.academic_apex_dir = self.vault_path / "AcademicApex"
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Validate and create directories
        self._setup_vault()
    
    def _setup_vault(self) -> None:
        """
        Setup the vault directory structure and validate paths.
        
        Raises:
            ValueError: If vault path setup fails
        """
        try:
            # Create vault directory if it doesn't exist
            self.vault_path.mkdir(parents=True, exist_ok=True)
            
            # Create AcademicApex subdirectory
            self.academic_apex_dir.mkdir(exist_ok=True)
            
            # Create additional subdirectories for organization
            (self.academic_apex_dir / "StudyPlans").mkdir(exist_ok=True)
            (self.academic_apex_dir / "Quizzes").mkdir(exist_ok=True)
            (self.academic_apex_dir / "CodeModules").mkdir(exist_ok=True)
            
            self.logger.info(f"✓ Vault setup complete at {self.vault_path}")
            self.logger.info(f"✓ AcademicApex directory: {self.academic_apex_dir}")
            
        except Exception as e:
            raise ValueError(f"Failed to setup vault at {self.vault_path}: {e}")
    
    def _generate_timestamp_filename(self, prefix: str, extension: str = "md") -> str:
        """
        Generate a timestamped filename.
        
        Args:
            prefix: Filename prefix
            extension: File extension (default: md)
            
        Returns:
            Timestamped filename
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.{extension}"
    
    def create_study_plan_note(self, subject: str, markdown_content: str, 
                              duration: str = "") -> Dict[str, Any]:
        """
        Create a study plan note in the Obsidian vault.
        
        Args:
            subject: Subject/topic of the study plan
            markdown_content: Markdown content for the study plan
            duration: Optional duration information
            
        Returns:
            Dict with file path and metadata
        """
        try:
            # Generate filename
            safe_subject = "".join(c for c in subject if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_subject = safe_subject.replace(' ', '_')[:50]  # Limit length
            
            filename = self._generate_timestamp_filename(f"StudyPlan_{safe_subject}")
            file_path = self.academic_apex_dir / "StudyPlans" / filename
            
            # Create frontmatter
            frontmatter = f"""---
title: "Study Plan: {subject}"
subject: "{subject}"
created: {datetime.now().isoformat()}
type: "study-plan"
duration: "{duration}"
tags: ["academic-apex", "study-plan", "ai-generated"]
---

# Study Plan: {subject}

Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Duration: {duration}

---

"""
            
            # Combine frontmatter with content
            full_content = frontmatter + markdown_content
            
            # Write file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(full_content)
            
            self.logger.info(f"✓ Study plan created: {file_path}")
            
            return {
                "file_path": str(file_path),
                "filename": filename,
                "subject": subject,
                "duration": duration,
                "size": len(full_content),
                "created": datetime.now().isoformat(),
                "success": True
            }
            
        except Exception as e:
            self.logger.error(f"Failed to create study plan: {e}")
            return {
                "success": False,
                "error": str(e),
                "subject": subject
            }
    
    def create_quiz_note(self, subject: str, quiz_content: str) -> Dict[str, Any]:
        """
        Create a quiz note in the Obsidian vault.
        
        Args:
            subject: Subject/topic of the quiz
            quiz_content: Quiz content in markdown format
            
        Returns:
            Dict with file path and metadata
        """
        try:
            # Generate filename
            safe_subject = "".join(c for c in subject if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_subject = safe_subject.replace(' ', '_')[:50]
            
            filename = self._generate_timestamp_filename(f"Quiz_{safe_subject}")
            file_path = self.academic_apex_dir / "Quizzes" / filename
            
            # Create frontmatter
            frontmatter = f"""---
title: "Quiz: {subject}"
subject: "{subject}"
created: {datetime.now().isoformat()}
type: "quiz"
tags: ["academic-apex", "quiz", "ai-generated"]
---

# Quiz: {subject}

Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

"""
            
            # Combine frontmatter with content
            full_content = frontmatter + quiz_content
            
            # Write file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(full_content)
            
            self.logger.info(f"✓ Quiz created: {file_path}")
            
            return {
                "file_path": str(file_path),
                "filename": filename,
                "subject": subject,
                "size": len(full_content),
                "created": datetime.now().isoformat(),
                "success": True
            }
            
        except Exception as e:
            self.logger.error(f"Failed to create quiz: {e}")
            return {
                "success": False,
                "error": str(e),
                "subject": subject
            }
    
    def create_note(self, title: str, content: str, category: str = "general") -> Dict[str, Any]:
        """
        Create a general note in the Obsidian vault.
        
        Args:
            title: Note title
            content: Note content in markdown format
            category: Category for organization
            
        Returns:
            Dict with file path and metadata
        """
        try:
            # Generate filename
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_title = safe_title.replace(' ', '_')[:50]
            
            filename = self._generate_timestamp_filename(f"Note_{safe_title}")
            file_path = self.academic_apex_dir / filename
            
            # Create frontmatter
            frontmatter = f"""---
title: "{title}"
category: "{category}"
created: {datetime.now().isoformat()}
type: "note"
tags: ["academic-apex", "{category}", "ai-generated"]
---

# {title}

Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Category: {category}

---

"""
            
            # Combine frontmatter with content
            full_content = frontmatter + content
            
            # Write file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(full_content)
            
            self.logger.info(f"✓ Note created: {file_path}")
            
            return {
                "file_path": str(file_path),
                "filename": filename,
                "title": title,
                "category": category,
                "size": len(full_content),
                "created": datetime.now().isoformat(),
                "success": True
            }
            
        except Exception as e:
            self.logger.error(f"Failed to create note: {e}")
            return {
                "success": False,
                "error": str(e),
                "title": title
            }
    
    def list_notes(self, category: Optional[str] = None) -> Dict[str, Any]:
        """
        List notes in the vault.
        
        Args:
            category: Optional category filter
            
        Returns:
            Dict with list of notes and metadata
        """
        try:
            notes = []
            
            # Search in all subdirectories
            for path in self.academic_apex_dir.rglob("*.md"):
                if path.is_file():
                    try:
                        stat = path.stat()
                        note_info = {
                            "filename": path.name,
                            "path": str(path),
                            "size": stat.st_size,
                            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                            "category": path.parent.name if path.parent != self.academic_apex_dir else "general"
                        }
                        
                        if category is None or note_info["category"] == category:
                            notes.append(note_info)
                    except Exception as e:
                        self.logger.warning(f"Could not read metadata for {path}: {e}")
            
            notes.sort(key=lambda x: x["modified"], reverse=True)
            
            return {
                "notes": notes,
                "count": len(notes),
                "vault_path": str(self.vault_path),
                "success": True
            }
            
        except Exception as e:
            self.logger.error(f"Failed to list notes: {e}")
            return {
                "success": False,
                "error": str(e),
                "notes": [],
                "count": 0
            }
    
    def validate_vault(self) -> Dict[str, Any]:
        """
        Validate the vault structure and accessibility.
        
        Returns:
            Dict with validation results
        """
        try:
            issues = []
            
            # Check vault path
            if not self.vault_path.exists():
                issues.append(f"Vault path does not exist: {self.vault_path}")
            elif not self.vault_path.is_dir():
                issues.append(f"Vault path is not a directory: {self.vault_path}")
            
            # Check AcademicApex directory
            if not self.academic_apex_dir.exists():
                issues.append(f"AcademicApex directory missing: {self.academic_apex_dir}")
            
            # Check subdirectories
            subdirs = ["StudyPlans", "Quizzes", "CodeModules"]
            for subdir in subdirs:
                path = self.academic_apex_dir / subdir
                if not path.exists():
                    issues.append(f"Subdirectory missing: {path}")
            
            # Check write permissions
            try:
                test_file = self.academic_apex_dir / ".test_write"
                test_file.write_text("test")
                test_file.unlink()
            except Exception as e:
                issues.append(f"Write permission test failed: {e}")
            
            is_valid = len(issues) == 0
            
            return {
                "valid": is_valid,
                "issues": issues,
                "vault_path": str(self.vault_path),
                "academic_apex_dir": str(self.academic_apex_dir),
                "success": True
            }
            
        except Exception as e:
            return {
                "valid": False,
                "success": False,
                "error": str(e),
                "issues": [str(e)]
            }


def test_obsidian_adapter():
    """Unit test for ObsidianAdapter."""
    import tempfile
    import shutil
    
    # Create temporary vault for testing
    temp_vault = tempfile.mkdtemp(prefix="test_vault_")
    
    try:
        print(f"Testing with temporary vault: {temp_vault}")
        
        # Initialize adapter
        adapter = ObsidianAdapter(temp_vault)
        
        # Test validation
        validation = adapter.validate_vault()
        assert validation["valid"], f"Vault validation failed: {validation}"
        print("✓ Vault validation passed")
        
        # Test study plan creation
        study_plan_result = adapter.create_study_plan_note(
            "Test Subject",
            "## Study Plan Content\n\n- Topic 1\n- Topic 2\n",
            "2 hours"
        )
        assert study_plan_result["success"], f"Study plan creation failed: {study_plan_result}"
        print("✓ Study plan creation passed")
        
        # Test quiz creation
        quiz_result = adapter.create_quiz_note(
            "Test Quiz",
            "## Question 1\n\nWhat is 2+2?\n\n---ANSWERS---\n\n4"
        )
        assert quiz_result["success"], f"Quiz creation failed: {quiz_result}"
        print("✓ Quiz creation passed")
        
        # Test note listing
        notes_result = adapter.list_notes()
        assert notes_result["success"], f"Note listing failed: {notes_result}"
        assert notes_result["count"] >= 2, f"Expected at least 2 notes, got {notes_result['count']}"
        print(f"✓ Note listing passed ({notes_result['count']} notes found)")
        
        print("✓ All ObsidianAdapter tests passed")
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False
        
    finally:
        # Cleanup temporary vault
        try:
            shutil.rmtree(temp_vault)
        except Exception as e:
            print(f"Warning: Could not cleanup temp vault {temp_vault}: {e}")


if __name__ == "__main__":
    # Run self-test
    success = test_obsidian_adapter()
    exit(0 if success else 1)
