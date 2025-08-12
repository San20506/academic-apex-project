#!/usr/bin/env python3
"""
Ollama Adapter for Academic Apex Strategist

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

import json
import logging
import time
from typing import Dict, Any, Optional
import requests


class OllamaAdapter:
    """
    Adapter for communicating with Ollama API running locally.
    
    Provides robust error handling with exponential backoff and retry logic
    for generating text using DeepSeek Coder or other Ollama models.
    """
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "deepseek-coder"):
        """
        Initialize the OllamaAdapter.
        
        Args:
            base_url: Base URL for the Ollama API
            model: Default model name to use
        """
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.session = requests.Session()
        self.session.timeout = 120  # 2 minutes timeout for long generation tasks
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def _exponential_backoff(self, attempt: int) -> float:
        """Calculate exponential backoff delay."""
        return min(2 ** attempt, 30)  # Cap at 30 seconds
    
    def generate(self, prompt: str, max_tokens: int = 1024, temperature: float = 0.7, 
                model: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate text using Ollama API with robust error handling.
        
        Args:
            prompt: Input prompt for generation
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0 to 1.0)
            model: Optional model override
            
        Returns:
            Dict containing the generated response and metadata
            
        Raises:
            ConnectionError: If Ollama is not reachable after retries
            ValueError: If response is invalid
        """
        model_name = model or self.model
        
        payload = {
            "model": model_name,
            "prompt": prompt,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature,
            },
            "stream": False  # Get complete response at once
        }
        
        # Retry with exponential backoff
        for attempt in range(3):
            try:
                self.logger.info(f"Attempting to generate text (attempt {attempt + 1}/3)")
                
                response = self.session.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                
                response.raise_for_status()
                result = response.json()
                
                # Validate response structure
                if "response" not in result:
                    raise ValueError(f"Invalid response format: {result}")
                
                self.logger.info("Text generation successful")
                return {
                    "text": result["response"],
                    "model": model_name,
                    "prompt_tokens": result.get("prompt_eval_count", 0),
                    "completion_tokens": result.get("eval_count", 0),
                    "done": result.get("done", True)
                }
                
            except requests.exceptions.ConnectionError as e:
                self.logger.warning(f"Connection failed (attempt {attempt + 1}/3): {e}")
                if attempt == 2:  # Last attempt
                    raise ConnectionError(
                        f"Could not connect to Ollama at {self.base_url}. "
                        f"Please ensure Ollama is running and accessible."
                    )
                
                # Wait before retry
                delay = self._exponential_backoff(attempt)
                self.logger.info(f"Waiting {delay} seconds before retry...")
                time.sleep(delay)
                
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request failed: {e}")
                if attempt == 2:
                    raise ConnectionError(f"Request to Ollama failed: {e}")
                
                delay = self._exponential_backoff(attempt)
                time.sleep(delay)
                
            except (json.JSONDecodeError, ValueError) as e:
                self.logger.error(f"Response parsing failed: {e}")
                if attempt == 2:
                    raise ValueError(f"Invalid response from Ollama: {e}")
                
                delay = self._exponential_backoff(attempt)
                time.sleep(delay)
    
    def test_connection(self) -> bool:
        """
        Test if Ollama is reachable and responsive.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = self.session.get(f"{self.base_url}/api/tags", timeout=10)
            response.raise_for_status()
            self.logger.info("Ollama connection test successful")
            return True
        except Exception as e:
            self.logger.error(f"Ollama connection test failed: {e}")
            return False
    
    def list_models(self) -> Dict[str, Any]:
        """
        List available models in Ollama.
        
        Returns:
            Dict containing available models
        """
        try:
            response = self.session.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Failed to list models: {e}")
            return {"models": []}


def test_ollama_adapter():
    """Unit test for OllamaAdapter - skips if Ollama not reachable."""
    adapter = OllamaAdapter()
    
    # Test connection first
    if not adapter.test_connection():
        print("SKIP: Ollama not reachable, skipping test")
        return True
    
    try:
        # Test basic generation
        result = adapter.generate("Hello from test", max_tokens=50)
        assert result["text"], "Generated text should not be empty"
        assert result["model"] == "deepseek-coder", f"Model should be deepseek-coder, got {result['model']}"
        
        print(f"✓ Test passed: Generated {len(result['text'])} characters")
        print(f"✓ Sample output: {result['text'][:100]}...")
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


if __name__ == "__main__":
    # Run self-test
    success = test_ollama_adapter()
    exit(0 if success else 1)
