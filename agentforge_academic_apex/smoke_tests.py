#!/usr/bin/env python3
"""
Smoke Tests for Academic Apex Strategist

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
import sys
import logging
import requests
from pathlib import Path
from typing import Dict, Any, Optional

# Import our components
from ollama_adapter import OllamaAdapter
from obsidian_adapter import ObsidianAdapter


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AcademicApexSmokeTests:
    """
    Comprehensive smoke tests for Academic Apex Strategist.
    
    Tests all major components and integrations to ensure the system
    is working correctly before deployment.
    """
    
    def __init__(self):
        """Initialize smoke tests with configuration from environment."""
        self.ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        self.curator_url = os.getenv('CURATOR_SERVICE_URL', 'http://localhost:5001')
        self.vault_path = os.getenv('OBSIDIAN_VAULT_PATH')
        
        # Initialize adapters
        self.ollama_adapter = OllamaAdapter(base_url=self.ollama_host)
        self.obsidian_adapter = None
        
        # Setup vault if path provided
        if self.vault_path:
            try:
                self.obsidian_adapter = ObsidianAdapter(self.vault_path)
                logger.info(f"✓ Obsidian adapter initialized with vault: {self.vault_path}")
            except Exception as e:
                logger.error(f"✗ Failed to initialize Obsidian adapter: {e}")
        else:
            logger.warning("⚠ OBSIDIAN_VAULT_PATH not set, Obsidian tests will be skipped")
        
        # Create generated directory
        self.generated_dir = Path("generated")
        self.generated_dir.mkdir(exist_ok=True)
        
        # Test results tracking
        self.test_results = {
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'details': []
        }
    
    def log_test_result(self, test_name: str, passed: bool, message: str = "", 
                       skipped: bool = False) -> None:
        """Log test result and update counters."""
        if skipped:
            self.test_results['skipped'] += 1
            logger.info(f"⏭ SKIPPED: {test_name} - {message}")
            self.test_results['details'].append({
                'test': test_name,
                'status': 'skipped',
                'message': message
            })
        elif passed:
            self.test_results['passed'] += 1
            logger.info(f"✓ PASSED: {test_name} - {message}")
            self.test_results['details'].append({
                'test': test_name,
                'status': 'passed', 
                'message': message
            })
        else:
            self.test_results['failed'] += 1
            logger.error(f"✗ FAILED: {test_name} - {message}")
            self.test_results['details'].append({
                'test': test_name,
                'status': 'failed',
                'message': message
            })
    
    def test_curator_service_health(self) -> bool:
        """Test curator service health and availability."""
        test_name = "curator_service_health"
        
        try:
            # Test health endpoint
            response = requests.get(f"{self.curator_url}/healthz", timeout=10)
            
            if response.status_code == 200:
                health_data = response.json()
                is_healthy = health_data.get('status') == 'healthy'
                
                if is_healthy:
                    self.log_test_result(test_name, True, 
                                       f"Curator service healthy, model: {health_data.get('curator_model')}")
                    return True
                else:
                    self.log_test_result(test_name, False, 
                                       f"Curator service degraded: {health_data}")
                    return False
            else:
                self.log_test_result(test_name, False, 
                                   f"Health check failed with status {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test_result(test_name, False, f"Curator service unreachable: {e}")
            return False
        except Exception as e:
            self.log_test_result(test_name, False, f"Health check error: {e}")
            return False
    
    def test_curator_prompt_refinement(self) -> bool:
        """Test curator service prompt refinement functionality."""
        test_name = "curator_prompt_refinement"
        
        try:
            # Test prompt curation
            test_payload = {
                "prompt": "Create a quiz about Python programming",
                "instruction": "Make it more specific and detailed"
            }
            
            response = requests.post(
                f"{self.curator_url}/api/curate",
                json=test_payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('success') and result.get('refined'):
                    refined_length = result.get('refined_length', 0)
                    original_length = result.get('original_length', 0)
                    
                    self.log_test_result(test_name, True,
                                       f"Prompt refined: {original_length} -> {refined_length} chars")
                    return True
                else:
                    self.log_test_result(test_name, False,
                                       f"Curation failed: {result.get('error', 'Unknown error')}")
                    return False
            else:
                self.log_test_result(test_name, False,
                                   f"Curation request failed with status {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test_result(test_name, False, f"Curation test error: {e}")
            return False
    
    def test_diagnostic_quiz(self, adapter: OllamaAdapter) -> bool:
        """
        Test diagnostic quiz generation.
        
        Args:
            adapter: OllamaAdapter instance
            
        Returns:
            True if test passes, False otherwise
        """
        test_name = "diagnostic_quiz"
        
        try:
            # Test connection first
            if not adapter.test_connection():
                self.log_test_result(test_name, False, "Ollama connection failed")
                return False
            
            # Generate diagnostic quiz
            quiz_prompt = """Create a diagnostic quiz for Python Programming Basics with exactly 5 questions.

Requirements:
- Include multiple choice and short answer questions
- Cover fundamental concepts like variables, data types, functions
- Provide clear instructions
- End with "---ANSWERS---" section containing detailed answer explanations
- Format professionally for educational use

Make this a comprehensive assessment suitable for intermediate learners."""

            logger.info("Generating diagnostic quiz...")
            result = adapter.generate(
                quiz_prompt,
                max_tokens=1500,
                temperature=0.5
            )
            
            quiz_text = result["text"].strip()
            
            # Validate quiz content
            validation_checks = [
                ("non_empty", len(quiz_text) > 100, "Quiz text too short"),
                ("has_questions", "?" in quiz_text, "No questions found"),
                ("has_answers", "---ANSWERS---" in quiz_text, "Answer section missing"),
                ("reasonable_length", len(quiz_text) > 500, "Quiz content insufficient")
            ]
            
            failed_checks = []
            for check_name, condition, error_msg in validation_checks:
                if not condition:
                    failed_checks.append(error_msg)
            
            if failed_checks:
                self.log_test_result(test_name, False, f"Validation failed: {', '.join(failed_checks)}")
                return False
            
            # Save quiz for review
            quiz_file = self.generated_dir / "diagnostic_quiz_sample.md"
            with open(quiz_file, 'w', encoding='utf-8') as f:
                f.write(f"# Diagnostic Quiz - Generated by Academic Apex\n\n")
                f.write(f"Generated: {result.get('model', 'unknown')} model\n")
                f.write(f"Tokens: {result.get('completion_tokens', 0)}\n\n")
                f.write(quiz_text)
            
            self.log_test_result(test_name, True, 
                               f"Quiz generated ({len(quiz_text)} chars, saved to {quiz_file})")
            
            print("\n" + "="*80)
            print("SAMPLE DIAGNOSTIC QUIZ OUTPUT:")
            print("="*80)
            print(quiz_text[:500] + "..." if len(quiz_text) > 500 else quiz_text)
            print("="*80 + "\n")
            
            return True
            
        except Exception as e:
            self.log_test_result(test_name, False, f"Quiz generation error: {e}")
            return False
    
    def test_study_plan(self, adapter: OllamaAdapter, obs_adapter: Optional[ObsidianAdapter] = None) -> bool:
        """
        Test study plan generation and Obsidian integration.
        
        Args:
            adapter: OllamaAdapter instance
            obs_adapter: Optional ObsidianAdapter instance
            
        Returns:
            True if test passes, False otherwise
        """
        test_name = "study_plan"
        
        try:
            # Test connection first
            if not adapter.test_connection():
                self.log_test_result(test_name, False, "Ollama connection failed")
                return False
            
            # Generate study plan
            study_plan_prompt = """Create a comprehensive 120-minute (2 hour) study plan for "Machine Learning Fundamentals" at intermediate level.

Requirements:
- Break down into specific time blocks with exact timing (e.g., "0:00-0:15 - Introduction")
- Include variety: reading, hands-on practice, review, strategic breaks
- Add progress checkpoints and self-assessment moments
- Use active learning techniques
- Format as clear markdown with timeline structure
- Include specific resources and activities for each time block

Learning objectives:
- Understand supervised vs unsupervised learning
- Learn basic algorithms (linear regression, decision trees)
- Practice with real datasets
- Understand model evaluation metrics

Create a detailed minute-by-minute timeline that maximizes learning effectiveness."""

            logger.info("Generating study plan...")
            result = adapter.generate(
                study_plan_prompt,
                max_tokens=2000,
                temperature=0.4
            )
            
            study_plan_text = result["text"].strip()
            
            # Validate study plan content
            validation_checks = [
                ("non_empty", len(study_plan_text) > 200, "Study plan too short"),
                ("has_timeline", any(time_marker in study_plan_text.lower() 
                                   for time_marker in ["0:00", "minutes", "hour", ":"]), 
                 "No timeline structure found"),
                ("has_structure", any(marker in study_plan_text 
                                    for marker in ["#", "##", "-", "*"]), 
                 "No clear structure found"),
                ("reasonable_length", len(study_plan_text) > 800, "Study plan content insufficient")
            ]
            
            failed_checks = []
            for check_name, condition, error_msg in validation_checks:
                if not condition:
                    failed_checks.append(error_msg)
            
            if failed_checks:
                self.log_test_result(test_name, False, f"Validation failed: {', '.join(failed_checks)}")
                return False
            
            # Save to Obsidian if adapter available
            obsidian_success = False
            if obs_adapter:
                try:
                    obs_result = obs_adapter.create_study_plan_note(
                        "Machine Learning Fundamentals",
                        study_plan_text,
                        "2 hours"
                    )
                    
                    if obs_result["success"]:
                        obsidian_success = True
                        logger.info(f"✓ Study plan saved to Obsidian: {obs_result['filename']}")
                    else:
                        logger.warning(f"⚠ Failed to save to Obsidian: {obs_result.get('error')}")
                        
                except Exception as e:
                    logger.warning(f"⚠ Obsidian integration error: {e}")
            
            # Also save as regular file for review
            plan_file = self.generated_dir / "study_plan_sample.md"
            with open(plan_file, 'w', encoding='utf-8') as f:
                f.write(f"# Study Plan - Generated by Academic Apex\n\n")
                f.write(f"Generated: {result.get('model', 'unknown')} model\n")
                f.write(f"Tokens: {result.get('completion_tokens', 0)}\n")
                f.write(f"Obsidian Integration: {'✓' if obsidian_success else '✗'}\n\n")
                f.write(study_plan_text)
            
            message = f"Study plan generated ({len(study_plan_text)} chars, saved to {plan_file}"
            if obsidian_success:
                message += " + Obsidian vault"
                
            self.log_test_result(test_name, True, message)
            
            print("\n" + "="*80)
            print("SAMPLE STUDY PLAN OUTPUT:")
            print("="*80)
            print(study_plan_text[:600] + "..." if len(study_plan_text) > 600 else study_plan_text)
            print("="*80 + "\n")
            
            return True
            
        except Exception as e:
            self.log_test_result(test_name, False, f"Study plan generation error: {e}")
            return False
    
    def test_code_generation(self, adapter: OllamaAdapter) -> bool:
        """
        Test Python code module generation.
        
        Args:
            adapter: OllamaAdapter instance
            
        Returns:
            True if test passes, False otherwise
        """
        test_name = "code_generation"
        
        try:
            # Test connection first
            if not adapter.test_connection():
                self.log_test_result(test_name, False, "Ollama connection failed")
                return False
            
            # Generate Python module
            code_prompt = """Create a complete Python module named 'study_utils' that provides utility functions for academic tasks.

Required functionality:
- schedule_to_markdown(schedule_dict): Convert a study schedule dictionary to markdown format
- quiz_scorer(answers, correct_answers): Score a quiz and return percentage and feedback
- study_timer(duration_minutes): A simple study timer function with breaks
- progress_tracker(completed_tasks, total_tasks): Track and display study progress

Requirements:
- Write complete, runnable Python code
- Include comprehensive docstrings for all functions
- Add type hints where appropriate
- Include proper error handling
- Follow PEP 8 style guidelines
- Add a few unit tests at the bottom
- Make functions practical for real academic use

Ensure the code is production-ready with clear documentation."""

            logger.info("Generating Python module...")
            result = adapter.generate(
                code_prompt,
                max_tokens=2500,
                temperature=0.3
            )
            
            code_text = result["text"].strip()
            
            # Validate generated code
            validation_checks = [
                ("non_empty", len(code_text) > 100, "Generated code too short"),
                ("has_functions", "def " in code_text, "No function definitions found"),
                ("has_docstrings", '"""' in code_text or "'''" in code_text, "No docstrings found"),
                ("has_schedule_func", "schedule_to_markdown" in code_text, "Required function schedule_to_markdown missing"),
                ("python_like", any(keyword in code_text for keyword in ["import", "def", "class", "return"]), 
                 "Doesn't look like Python code"),
                ("reasonable_length", len(code_text) > 500, "Generated code insufficient")
            ]
            
            failed_checks = []
            for check_name, condition, error_msg in validation_checks:
                if not condition:
                    failed_checks.append(error_msg)
            
            if failed_checks:
                self.log_test_result(test_name, False, f"Validation failed: {', '.join(failed_checks)}")
                return False
            
            # Save generated module
            code_file = self.generated_dir / "study_utils.py"
            with open(code_file, 'w', encoding='utf-8') as f:
                f.write(f'"""\nStudy Utilities Module - Generated by Academic Apex\n')
                f.write(f'Generated: {result.get("model", "unknown")} model\n')
                f.write(f'Tokens: {result.get("completion_tokens", 0)}\n')
                f.write(f'"""\n\n')
                f.write(code_text)
            
            # Test basic Python syntax (try to compile)
            syntax_valid = False
            try:
                with open(code_file, 'r', encoding='utf-8') as f:
                    compile(f.read(), code_file, 'exec')
                syntax_valid = True
                logger.info("✓ Generated code has valid Python syntax")
            except SyntaxError as e:
                logger.warning(f"⚠ Generated code has syntax issues: {e}")
            except Exception as e:
                logger.warning(f"⚠ Code compilation check failed: {e}")
            
            message = f"Code module generated ({len(code_text)} chars, saved to {code_file}"
            if syntax_valid:
                message += ", syntax valid"
                
            self.log_test_result(test_name, True, message)
            
            print("\n" + "="*80)
            print("SAMPLE CODE MODULE OUTPUT:")
            print("="*80)
            print(code_text[:800] + "..." if len(code_text) > 800 else code_text)
            print("="*80 + "\n")
            
            return True
            
        except Exception as e:
            self.log_test_result(test_name, False, f"Code generation error: {e}")
            return False
    
    def test_obsidian_integration(self) -> bool:
        """Test Obsidian vault integration and file creation."""
        test_name = "obsidian_integration"
        
        if not self.obsidian_adapter:
            self.log_test_result(test_name, True, "Obsidian adapter not configured", skipped=True)
            return True
        
        try:
            # Test vault validation
            validation = self.obsidian_adapter.validate_vault()
            if not validation.get("valid"):
                self.log_test_result(test_name, False, 
                                   f"Vault validation failed: {validation.get('issues')}")
                return False
            
            # Test note creation
            test_note = self.obsidian_adapter.create_note(
                "Academic Apex Test",
                "This is a test note created during smoke tests.\n\n- Feature: Note creation\n- Status: Testing\n- Component: ObsidianAdapter",
                "testing"
            )
            
            if not test_note.get("success"):
                self.log_test_result(test_name, False, 
                                   f"Note creation failed: {test_note.get('error')}")
                return False
            
            # Test note listing
            notes_list = self.obsidian_adapter.list_notes()
            if not notes_list.get("success"):
                self.log_test_result(test_name, False, 
                                   f"Note listing failed: {notes_list.get('error')}")
                return False
            
            note_count = notes_list.get("count", 0)
            vault_path = notes_list.get("vault_path")
            
            self.log_test_result(test_name, True, 
                               f"Obsidian integration working ({note_count} notes in {vault_path})")
            return True
            
        except Exception as e:
            self.log_test_result(test_name, False, f"Obsidian integration error: {e}")
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """
        Run all smoke tests and return comprehensive results.
        
        Returns:
            Dict containing test results and summary
        """
        logger.info("🚀 Starting Academic Apex Strategist Smoke Tests")
        logger.info("="*60)
        
        # Environment check
        logger.info(f"Ollama Host: {self.ollama_host}")
        logger.info(f"Curator URL: {self.curator_url}")
        logger.info(f"Vault Path: {self.vault_path or 'Not set'}")
        logger.info("="*60)
        
        # Run individual tests
        test_functions = [
            # Infrastructure tests
            ("curator_health", self.test_curator_service_health),
            ("curator_functionality", self.test_curator_prompt_refinement),
            ("obsidian_integration", self.test_obsidian_integration),
            
            # Core functionality tests  
            ("diagnostic_quiz", lambda: self.test_diagnostic_quiz(self.ollama_adapter)),
            ("study_plan", lambda: self.test_study_plan(self.ollama_adapter, self.obsidian_adapter)),
            ("code_generation", lambda: self.test_code_generation(self.ollama_adapter)),
        ]
        
        # Execute tests
        for test_category, test_func in test_functions:
            try:
                logger.info(f"\n📋 Running test: {test_category}")
                test_func()
            except Exception as e:
                self.log_test_result(test_category, False, f"Test execution error: {e}")
        
        # Generate summary
        total_tests = self.test_results['passed'] + self.test_results['failed'] + self.test_results['skipped']
        success_rate = (self.test_results['passed'] / max(total_tests - self.test_results['skipped'], 1)) * 100
        
        logger.info("\n" + "="*60)
        logger.info("📊 SMOKE TESTS SUMMARY")
        logger.info("="*60)
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"✓ Passed: {self.test_results['passed']}")
        logger.info(f"✗ Failed: {self.test_results['failed']}")
        logger.info(f"⏭ Skipped: {self.test_results['skipped']}")
        logger.info(f"📈 Success Rate: {success_rate:.1f}%")
        
        # Show detailed results
        if self.test_results['failed'] > 0:
            logger.error("\n❌ FAILED TESTS:")
            for detail in self.test_results['details']:
                if detail['status'] == 'failed':
                    logger.error(f"  - {detail['test']}: {detail['message']}")
        
        if self.test_results['skipped'] > 0:
            logger.info("\n⏭ SKIPPED TESTS:")
            for detail in self.test_results['details']:
                if detail['status'] == 'skipped':
                    logger.info(f"  - {detail['test']}: {detail['message']}")
        
        # Final verdict
        all_critical_passed = self.test_results['failed'] == 0
        logger.info("\n" + "="*60)
        
        if all_critical_passed:
            logger.info("🎉 ALL SMOKE TESTS PASSED!")
            logger.info("✅ Academic Apex Strategist is ready for use")
        else:
            logger.error("❌ SOME TESTS FAILED!")
            logger.error("🔧 Please address the issues before deployment")
        
        logger.info("="*60)
        
        return {
            'success': all_critical_passed,
            'summary': self.test_results,
            'success_rate': success_rate,
            'generated_files': list(self.generated_dir.glob("*")),
            'vault_path': self.vault_path,
            'timestamp': logger.name  # Using logger name as placeholder for timestamp
        }


def main():
    """Main entry point for smoke tests."""
    
    # Check required environment variables
    required_env_check = []
    
    if not os.getenv('OBSIDIAN_VAULT_PATH'):
        required_env_check.append("OBSIDIAN_VAULT_PATH not set (Obsidian tests will be skipped)")
    
    if required_env_check:
        print("⚠ Environment Setup Warnings:")
        for warning in required_env_check:
            print(f"  - {warning}")
        print()
    
    # Create test instance and run
    try:
        smoke_tests = AcademicApexSmokeTests()
        results = smoke_tests.run_all_tests()
        
        # Exit with appropriate code
        exit_code = 0 if results['success'] else 1
        return exit_code
        
    except KeyboardInterrupt:
        logger.info("\n🛑 Tests interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"\n💥 Critical error running smoke tests: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
