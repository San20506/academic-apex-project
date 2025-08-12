#!/usr/bin/env python3
"""
Main Launcher for Academic Apex Strategist Executable
Handles startup of both curator service and web UI in a single executable
"""

import os
import sys
import time
import signal
import logging
import threading
import subprocess
from pathlib import Path
from typing import Optional

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global process tracking
curator_process: Optional[subprocess.Popen] = None
web_ui_thread: Optional[threading.Thread] = None
shutdown_event = threading.Event()

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def setup_environment():
    """Set up default environment variables"""
    defaults = {
        'OLLAMA_HOST': 'http://localhost:11434',
        'CURATOR_SERVICE_URL': 'http://localhost:5001',
        'CURATOR_MODEL': 'mistral-7b',
        'WEB_UI_PORT': '5000',
        'DEBUG': 'false'
    }
    
    for key, value in defaults.items():
        if not os.getenv(key):
            os.environ[key] = value
            logger.info(f"Set {key}={value}")

def check_python_modules():
    """Verify that required modules are available"""
    required_modules = ['flask', 'requests', 'pathlib']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        logger.error(f"Missing required modules: {missing_modules}")
        return False
    
    return True

def start_curator_service():
    """Start the curator service as a separate process"""
    global curator_process
    
    try:
        # Import here to avoid issues with frozen executable
        import curator_service
        
        logger.info("Starting curator service...")
        
        # Start curator in a separate thread to avoid blocking
        def run_curator():
            try:
                # Start Flask app directly
                curator_service.app.run(
                    host='0.0.0.0',
                    port=5001,
                    debug=False,
                    threaded=True,
                    use_reloader=False  # Important for executable
                )
            except Exception as e:
                logger.error(f"Curator service error: {e}")
        
        curator_thread = threading.Thread(target=run_curator, daemon=True)
        curator_thread.start()
        
        # Give curator time to start
        time.sleep(3)
        logger.info("✓ Curator service started")
        return True
        
    except Exception as e:
        logger.error(f"Failed to start curator service: {e}")
        return False

def start_web_ui():
    """Start the web UI"""
    global web_ui_thread
    
    try:
        # Import the web UI module
        import web_ui
        
        logger.info("Starting web UI...")
        
        def run_web_ui():
            try:
                # Configure Flask app
                web_ui.app.run(
                    host='0.0.0.0',
                    port=int(os.getenv('WEB_UI_PORT', '5000')),
                    debug=os.getenv('DEBUG', 'false').lower() == 'true',
                    threaded=True,
                    use_reloader=False  # Important for executable
                )
            except Exception as e:
                logger.error(f"Web UI error: {e}")
        
        web_ui_thread = threading.Thread(target=run_web_ui, daemon=False)
        web_ui_thread.start()
        
        logger.info("✓ Web UI started")
        return True
        
    except Exception as e:
        logger.error(f"Failed to start web UI: {e}")
        return False

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info("Shutdown signal received. Cleaning up...")
    shutdown_event.set()
    
    # Cleanup processes
    global curator_process
    if curator_process and curator_process.poll() is None:
        curator_process.terminate()
    
    sys.exit(0)

def print_startup_banner():
    """Print the startup banner"""
    # Clear the console for a clean start
    os.system('cls' if os.name == 'nt' else 'clear')
    
    banner = """
==========================================
  Academic Apex Strategist v1.0
==========================================

🚀 Starting Academic Apex Strategist...
📊 Dashboard: http://localhost:{}
🔧 Ollama: {}
🎯 Curator: {}
📝 Vault: {}

==========================================
  All services starting...
  Press Ctrl+C to stop
==========================================
    """.format(
        os.getenv('WEB_UI_PORT', '5000'),
        os.getenv('OLLAMA_HOST', 'http://localhost:11434'),
        os.getenv('CURATOR_SERVICE_URL', 'http://localhost:5001'),
        os.getenv('OBSIDIAN_VAULT_PATH', 'Not configured')
    )
    
    print(banner)
    
    # Make sure output is visible
    sys.stdout.flush()

def main():
    """Main entry point for the executable"""
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Print startup banner
    print_startup_banner()
    
    # Setup environment
    setup_environment()
    
    # Check requirements
    if not check_python_modules():
        print("\n❌ ERROR: Missing required Python modules!")
        input("Press Enter to exit...")
        return 1
    
    # Create necessary directories
    Path("generated").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    
    # Start services
    logger.info("Starting Academic Apex Strategist services...")
    
    # Start curator service
    if not start_curator_service():
        print("\n⚠️  WARNING: Curator service failed to start!")
        print("Some features may not work properly.")
        input("Press Enter to continue or Ctrl+C to exit...")
    
    # Start web UI
    if not start_web_ui():
        print("\n❌ ERROR: Failed to start web UI!")
        input("Press Enter to exit...")
        return 1
    
    try:
        print("\n✅ Academic Apex Strategist is running!")
        print(f"🌐 Open your browser to: http://localhost:{os.getenv('WEB_UI_PORT', '5000')}")
        print("\nPress Ctrl+C to stop all services")
        
        # Keep main thread alive
        while not shutdown_event.is_set():
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt. Shutting down...")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1
    finally:
        shutdown_event.set()
        logger.info("Academic Apex Strategist stopped.")
    
    return 0

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)
