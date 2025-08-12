#!/usr/bin/env python3
"""
Slider Theme Controller for Academic Apex Strategist

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
import json
import logging
import subprocess
import webbrowser
from typing import Dict, Any, Optional
from pathlib import Path
import threading
import time
from flask import Flask, render_template_string, jsonify, request, send_file
from curator_service import app as curator_app
from curator_service import curator_adapter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SliderThemeController:
    """
    Controller for managing slider-based theme interface and Windows CMD theming.
    """
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.theme_config = {
            "theme_name": "Academic Apex Slider Theme",
            "version": "1.0.0",
            "colors": {
                "primary_bg": "#1a1a1a",
                "secondary_bg": "#2d2d2d", 
                "accent_color": "#4a9eff",
                "text_primary": "#ffffff",
                "text_secondary": "#b0b0b0",
                "success_color": "#4caf50",
                "warning_color": "#ff9800",
                "error_color": "#f44336"
            },
            "model_settings": {
                "temperature": 0.7,
                "max_tokens": 1024,
                "top_p": 0.9,
                "timeout": 120,
                "retry_attempts": 3
            }
        }
        
        # Windows CMD color mappings (BGR format for Windows registry)
        self.cmd_colors = {
            "ColorTable00": 0x1a1a1a,  # Black (Background)
            "ColorTable01": 0xff9e4a,  # Blue (Accent) - BGR format
            "ColorTable02": 0x50af4c,  # Green (Success)
            "ColorTable03": 0xaad400,  # Cyan (Info)
            "ColorTable04": 0x3643f4,  # Red (Error) - BGR format
            "ColorTable05": 0xb0279c,  # Magenta
            "ColorTable06": 0x0098ff,  # Yellow (Warning) - BGR format
            "ColorTable07": 0xffffff,  # White (Text)
        }

    def load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load theme configuration from file."""
        if not config_path:
            config_path = self.project_root / "theme_config.json"
        
        try:
            if Path(config_path).exists():
                with open(config_path, 'r') as f:
                    loaded_config = json.load(f)
                    self.theme_config.update(loaded_config)
                    logger.info(f"Loaded theme config from {config_path}")
            else:
                logger.info("No existing config found, using defaults")
        except Exception as e:
            logger.warning(f"Failed to load config: {e}, using defaults")
        
        return self.theme_config

    def save_config(self, config_path: Optional[str] = None) -> bool:
        """Save current theme configuration to file."""
        if not config_path:
            config_path = self.project_root / "theme_config.json"
        
        try:
            with open(config_path, 'w') as f:
                json.dump(self.theme_config, f, indent=2)
            logger.info(f"Saved theme config to {config_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            return False

    def apply_cmd_theme(self) -> Dict[str, Any]:
        """Apply theme to Windows Command Prompt via PowerShell."""
        ps_script_path = self.project_root / "apply-cmd-theme.ps1"
        
        if not ps_script_path.exists():
            return {
                "success": False,
                "error": "PowerShell theme script not found",
                "path": str(ps_script_path)
            }
        
        try:
            # Run PowerShell script to apply CMD theme
            result = subprocess.run([
                "powershell.exe", 
                "-ExecutionPolicy", "Bypass",
                "-File", str(ps_script_path),
                "-Backup"
            ], capture_output=True, text=True, timeout=30)
            
            success = result.returncode == 0
            
            return {
                "success": success,
                "output": result.stdout,
                "error": result.stderr if not success else None,
                "return_code": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "PowerShell script execution timed out"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to execute PowerShell script: {e}"
            }

    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status for the theme interface."""
        status = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "theme": {
                "name": self.theme_config["theme_name"],
                "version": self.theme_config["version"],
                "applied": True
            },
            "services": {},
            "system": {
                "os": "Windows" if os.name == 'nt' else "Unix-like",
                "python_version": sys.version.split()[0],
                "project_root": str(self.project_root)
            }
        }
        
        # Check curator service status
        try:
            ollama_connected = curator_adapter.test_connection()
            models_info = curator_adapter.list_models()
            
            status["services"]["curator"] = {
                "status": "online" if ollama_connected else "offline",
                "ollama_connected": ollama_connected,
                "available_models": len(models_info.get('models', [])),
                "model_names": [m.get('name', 'unknown') for m in models_info.get('models', [])]
            }
        except Exception as e:
            status["services"]["curator"] = {
                "status": "error",
                "error": str(e)
            }
        
        return status

    def update_model_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Update model configuration settings."""
        try:
            # Validate settings
            valid_keys = {"temperature", "max_tokens", "top_p", "timeout", "retry_attempts"}
            filtered_settings = {k: v for k, v in settings.items() if k in valid_keys}
            
            # Type conversion and validation
            if "temperature" in filtered_settings:
                filtered_settings["temperature"] = max(0.0, min(1.0, float(filtered_settings["temperature"])))
            
            if "max_tokens" in filtered_settings:
                filtered_settings["max_tokens"] = max(1, min(4000, int(filtered_settings["max_tokens"])))
            
            if "top_p" in filtered_settings:
                filtered_settings["top_p"] = max(0.1, min(1.0, float(filtered_settings["top_p"])))
            
            if "timeout" in filtered_settings:
                filtered_settings["timeout"] = max(10, min(600, int(filtered_settings["timeout"])))
            
            if "retry_attempts" in filtered_settings:
                filtered_settings["retry_attempts"] = max(1, min(10, int(filtered_settings["retry_attempts"])))
            
            # Update configuration
            self.theme_config["model_settings"].update(filtered_settings)
            
            # Save to file
            self.save_config()
            
            logger.info(f"Updated model settings: {filtered_settings}")
            
            return {
                "success": True,
                "updated_settings": filtered_settings,
                "current_settings": self.theme_config["model_settings"]
            }
            
        except Exception as e:
            logger.error(f"Failed to update model settings: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def launch_interface(self, port: int = 5002, auto_open: bool = True):
        """Launch the slider theme interface web server."""
        
        # Create Flask app for theme interface
        theme_app = Flask(__name__)
        
        @theme_app.route('/')
        def index():
            """Serve the main theme interface."""
            html_path = self.project_root / "slider_theme_interface.html"
            try:
                with open(html_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except FileNotFoundError:
                return jsonify({"error": "Theme interface HTML not found"}), 404
        
        @theme_app.route('/api/status')
        def status():
            """Get system status."""
            return jsonify(self.get_system_status())
        
        @theme_app.route('/api/config', methods=['GET', 'POST'])
        def config():
            """Get or update theme configuration."""
            if request.method == 'GET':
                return jsonify(self.theme_config)
            else:
                try:
                    data = request.get_json()
                    if 'model_settings' in data:
                        result = self.update_model_settings(data['model_settings'])
                        return jsonify(result)
                    else:
                        return jsonify({"error": "Invalid configuration data"}), 400
                except Exception as e:
                    return jsonify({"error": str(e)}), 500
        
        @theme_app.route('/api/apply-cmd-theme', methods=['POST'])
        def apply_cmd_theme():
            """Apply theme to Windows CMD."""
            result = self.apply_cmd_theme()
            return jsonify(result)
        
        @theme_app.route('/api/export-config')
        def export_config():
            """Export current configuration as JSON file."""
            try:
                config_path = self.project_root / "academic-apex-config-export.json"
                
                export_data = {
                    "theme": self.theme_config,
                    "system_status": self.get_system_status(),
                    "export_timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                
                with open(config_path, 'w') as f:
                    json.dump(export_data, f, indent=2)
                
                return send_file(
                    str(config_path),
                    as_attachment=True,
                    download_name="academic-apex-config.json",
                    mimetype='application/json'
                )
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        # Start the server
        logger.info(f"Starting slider theme interface on port {port}")
        
        if auto_open:
            # Open browser after short delay
            def open_browser():
                time.sleep(1)
                webbrowser.open(f"http://localhost:{port}")
            
            threading.Thread(target=open_browser, daemon=True).start()
        
        try:
            theme_app.run(
                host='0.0.0.0',
                port=port,
                debug=False,
                threaded=True
            )
        except Exception as e:
            logger.error(f"Failed to start theme interface: {e}")
            raise


def main():
    """Main entry point for slider theme controller."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Academic Apex Slider Theme Controller")
    parser.add_argument("--port", type=int, default=5002, help="Port for theme interface")
    parser.add_argument("--no-open", action="store_true", help="Don't auto-open browser")
    parser.add_argument("--apply-cmd", action="store_true", help="Apply CMD theme and exit")
    parser.add_argument("--config", help="Path to theme configuration file")
    
    args = parser.parse_args()
    
    # Initialize controller
    controller = SliderThemeController()
    
    # Load configuration
    controller.load_config(args.config)
    
    if args.apply_cmd:
        # Apply CMD theme only
        logger.info("Applying CMD theme...")
        result = controller.apply_cmd_theme()
        
        if result["success"]:
            print("✅ CMD theme applied successfully!")
            if result.get("output"):
                print(result["output"])
        else:
            print("❌ Failed to apply CMD theme:")
            print(result.get("error", "Unknown error"))
            sys.exit(1)
    else:
        # Launch interface
        try:
            controller.launch_interface(
                port=args.port,
                auto_open=not args.no_open
            )
        except KeyboardInterrupt:
            logger.info("Theme interface stopped by user")
        except Exception as e:
            logger.error(f"Theme interface error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
