#!/usr/bin/env python3
"""
Academic Apex Theme Overlay - Standalone Offline Theme Controller

A simple desktop overlay application for managing themes without web dependencies.
Focus on theme changing functionality only.

MIT License - Copyright (c) 2025 Academic Apex Project
"""

import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import json
import os
import sys
import subprocess
from pathlib import Path
import threading
import time
from typing import Dict, Any, Optional

class ThemeOverlay:
    """Standalone theme overlay application."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        
        # Theme configuration
        self.theme_config = {
            "theme_name": "Academic Apex Theme",
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
            "overlay_settings": {
                "always_on_top": True,
                "transparency": 0.95,
                "position_x": 100,
                "position_y": 100
            }
        }
        
        self.project_root = Path(__file__).parent
        self.config_file = self.project_root / "theme_overlay_config.json"
        self.load_config()
        
        # Track overlay state
        self.is_minimized = False
        self.original_geometry = None
        
        self.create_widgets()
        self.apply_theme()
        self.setup_overlay_behavior()

    def setup_window(self):
        """Configure the main window."""
        self.root.title("Academic Apex Theme Overlay")
        self.root.geometry("350x500+100+100")
        self.root.configure(bg="#1a1a1a")
        
        # Make window always on top
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-alpha", 0.95)
        
        # Remove window decorations for overlay feel
        self.root.overrideredirect(False)  # Keep decorations for now
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        """Create all UI widgets."""
        
        # Header
        self.header_frame = tk.Frame(self.root, bg="#2d2d2d", height=50)
        self.header_frame.pack(fill=tk.X, padx=5, pady=5)
        self.header_frame.pack_propagate(False)
        
        self.title_label = tk.Label(
            self.header_frame,
            text="🎨 Academic Apex Theme",
            font=("Segoe UI", 12, "bold"),
            bg="#2d2d2d",
            fg="#ffffff"
        )
        self.title_label.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.minimize_btn = tk.Button(
            self.header_frame,
            text="−",
            font=("Segoe UI", 12, "bold"),
            bg="#4a9eff",
            fg="white",
            width=3,
            command=self.toggle_minimize
        )
        self.minimize_btn.pack(side=tk.RIGHT, padx=5, pady=10)
        
        # Main content
        self.main_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Theme selection
        self.create_theme_section()
        
        # Color customization
        self.create_color_section()
        
        # Actions
        self.create_actions_section()
        
        # Status
        self.create_status_section()

    def create_theme_section(self):
        """Create theme selection section."""
        theme_frame = tk.LabelFrame(
            self.main_frame,
            text="Theme Selection",
            font=("Segoe UI", 10, "bold"),
            bg="#2d2d2d",
            fg="#ffffff",
            bd=1
        )
        theme_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Predefined themes
        themes = [
            ("Academic Apex (Default)", "academic_apex"),
            ("Dark Professional", "dark_professional"),
            ("Blue Steel", "blue_steel"),
            ("Green Matrix", "green_matrix"),
            ("Purple Haze", "purple_haze"),
            ("Custom", "custom")
        ]
        
        self.selected_theme = tk.StringVar(value="academic_apex")
        
        for i, (name, value) in enumerate(themes):
            rb = tk.Radiobutton(
                theme_frame,
                text=name,
                variable=self.selected_theme,
                value=value,
                font=("Segoe UI", 9),
                bg="#2d2d2d",
                fg="#ffffff",
                selectcolor="#4a9eff",
                activebackground="#2d2d2d",
                activeforeground="#ffffff",
                command=self.on_theme_change
            )
            rb.pack(anchor=tk.W, padx=10, pady=2)

    def create_color_section(self):
        """Create color customization section."""
        color_frame = tk.LabelFrame(
            self.main_frame,
            text="Color Customization",
            font=("Segoe UI", 10, "bold"),
            bg="#2d2d2d",
            fg="#ffffff",
            bd=1
        )
        color_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Color buttons
        colors = [
            ("Background", "primary_bg"),
            ("Accent", "accent_color"),
            ("Success", "success_color"),
            ("Warning", "warning_color"),
            ("Error", "error_color")
        ]
        
        self.color_buttons = {}
        
        for i, (name, key) in enumerate(colors):
            row = i // 2
            col = i % 2
            
            btn = tk.Button(
                color_frame,
                text=f"{name}\n{self.theme_config['colors'][key]}",
                font=("Segoe UI", 8),
                bg=self.theme_config['colors'][key],
                fg="white" if self.is_dark_color(self.theme_config['colors'][key]) else "black",
                width=15,
                height=2,
                command=lambda k=key, n=name: self.change_color(k, n)
            )
            btn.grid(row=row, column=col, padx=5, pady=3, sticky="ew")
            self.color_buttons[key] = btn
        
        # Configure grid weights
        for i in range(2):
            color_frame.grid_columnconfigure(i, weight=1)

    def create_actions_section(self):
        """Create actions section."""
        action_frame = tk.LabelFrame(
            self.main_frame,
            text="Actions",
            font=("Segoe UI", 10, "bold"),
            bg="#2d2d2d",
            fg="#ffffff",
            bd=1
        )
        action_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Action buttons
        actions = [
            ("Apply CMD Theme", self.apply_cmd_theme, "#4caf50"),
            ("Preview Theme", self.preview_theme, "#4a9eff"),
            ("Reset to Default", self.reset_theme, "#ff9800"),
            ("Save Configuration", self.save_config, "#9c27b0")
        ]
        
        for i, (text, command, color) in enumerate(actions):
            btn = tk.Button(
                action_frame,
                text=text,
                font=("Segoe UI", 9, "bold"),
                bg=color,
                fg="white",
                width=20,
                height=1,
                command=command
            )
            btn.pack(pady=2, padx=10, fill=tk.X)

    def create_status_section(self):
        """Create status section."""
        status_frame = tk.LabelFrame(
            self.main_frame,
            text="Status",
            font=("Segoe UI", 10, "bold"),
            bg="#2d2d2d",
            fg="#ffffff",
            bd=1
        )
        status_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.status_text = tk.Text(
            status_frame,
            height=6,
            font=("Consolas", 8),
            bg="#000000",
            fg="#00ff00",
            insertbackground="#00ff00",
            wrap=tk.WORD
        )
        self.status_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(self.status_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.status_text.yview)
        
        self.log_message("Academic Apex Theme Overlay initialized", "success")
        self.log_message("Ready for theme operations", "info")

    def setup_overlay_behavior(self):
        """Setup overlay-specific behaviors."""
        # Make draggable
        self.header_frame.bind("<Button-1>", self.start_drag)
        self.header_frame.bind("<B1-Motion>", self.do_drag)
        self.title_label.bind("<Button-1>", self.start_drag)
        self.title_label.bind("<B1-Motion>", self.do_drag)
        
        # Double-click to toggle always on top
        self.title_label.bind("<Double-Button-1>", self.toggle_always_on_top)

    def start_drag(self, event):
        """Start dragging the window."""
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def do_drag(self, event):
        """Handle window dragging."""
        x = self.root.winfo_pointerx() - self.drag_start_x
        y = self.root.winfo_pointery() - self.drag_start_y
        self.root.geometry(f"+{x}+{y}")

    def toggle_always_on_top(self, event=None):
        """Toggle always on top behavior."""
        current = self.root.wm_attributes("-topmost")
        self.root.wm_attributes("-topmost", not current)
        self.theme_config["overlay_settings"]["always_on_top"] = not current
        
        status = "enabled" if not current else "disabled"
        self.log_message(f"Always on top {status}", "info")

    def toggle_minimize(self):
        """Toggle minimize/restore."""
        if not self.is_minimized:
            self.original_geometry = self.root.geometry()
            self.main_frame.pack_forget()
            self.root.geometry("350x50")
            self.minimize_btn.config(text="+")
            self.is_minimized = True
        else:
            self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            if self.original_geometry:
                self.root.geometry(self.original_geometry)
            self.minimize_btn.config(text="−")
            self.is_minimized = False

    def is_dark_color(self, hex_color):
        """Check if a color is dark."""
        try:
            hex_color = hex_color.lstrip('#')
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            brightness = (r * 299 + g * 587 + b * 114) / 1000
            return brightness < 128
        except:
            return True

    def on_theme_change(self):
        """Handle theme selection change."""
        theme_name = self.selected_theme.get()
        self.log_message(f"Switching to theme: {theme_name}", "info")
        
        # Predefined theme colors
        themes = {
            "academic_apex": {
                "primary_bg": "#1a1a1a",
                "secondary_bg": "#2d2d2d",
                "accent_color": "#4a9eff",
                "success_color": "#4caf50",
                "warning_color": "#ff9800",
                "error_color": "#f44336"
            },
            "dark_professional": {
                "primary_bg": "#0d1117",
                "secondary_bg": "#161b22",
                "accent_color": "#58a6ff",
                "success_color": "#3fb950",
                "warning_color": "#d29922",
                "error_color": "#f85149"
            },
            "blue_steel": {
                "primary_bg": "#1e2124",
                "secondary_bg": "#2f3136",
                "accent_color": "#7289da",
                "success_color": "#43b581",
                "warning_color": "#faa61a",
                "error_color": "#f04747"
            },
            "green_matrix": {
                "primary_bg": "#0d1b2a",
                "secondary_bg": "#1b263b",
                "accent_color": "#00ff00",
                "success_color": "#00cc00",
                "warning_color": "#ffff00",
                "error_color": "#ff0000"
            },
            "purple_haze": {
                "primary_bg": "#1a0d26",
                "secondary_bg": "#2d1b42",
                "accent_color": "#9b59b6",
                "success_color": "#27ae60",
                "warning_color": "#f39c12",
                "error_color": "#e74c3c"
            }
        }
        
        if theme_name in themes:
            self.theme_config["colors"].update(themes[theme_name])
            self.update_color_buttons()
            self.apply_theme()
            self.log_message(f"Applied {theme_name} theme", "success")

    def change_color(self, color_key, color_name):
        """Open color picker for a specific color."""
        current_color = self.theme_config["colors"][color_key]
        color = colorchooser.askcolor(color=current_color, title=f"Choose {color_name} Color")
        
        if color[1]:  # If a color was selected
            self.theme_config["colors"][color_key] = color[1]
            self.update_color_buttons()
            self.apply_theme()
            self.log_message(f"Changed {color_name} to {color[1]}", "success")

    def update_color_buttons(self):
        """Update color button appearances."""
        for key, button in self.color_buttons.items():
            color = self.theme_config["colors"][key]
            button.config(
                bg=color,
                fg="white" if self.is_dark_color(color) else "black",
                text=f"{button.cget('text').split('\n')[0]}\n{color}"
            )

    def apply_theme(self):
        """Apply theme to the overlay itself."""
        colors = self.theme_config["colors"]
        
        # Update window background
        self.root.configure(bg=colors["primary_bg"])
        self.main_frame.configure(bg=colors["primary_bg"])
        self.header_frame.configure(bg=colors["secondary_bg"])

    def preview_theme(self):
        """Show a preview of the current theme."""
        colors = self.theme_config["colors"]
        
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Theme Preview")
        preview_window.geometry("300x200")
        preview_window.configure(bg=colors["primary_bg"])
        preview_window.wm_attributes("-topmost", True)
        
        tk.Label(
            preview_window,
            text="Theme Preview",
            font=("Segoe UI", 16, "bold"),
            bg=colors["primary_bg"],
            fg=colors["text_primary"]
        ).pack(pady=10)
        
        for name, color_key in [("Background", "primary_bg"), ("Accent", "accent_color"), 
                                ("Success", "success_color"), ("Warning", "warning_color"), 
                                ("Error", "error_color")]:
            tk.Label(
                preview_window,
                text=f"{name}: {colors[color_key]}",
                font=("Segoe UI", 10),
                bg=colors[color_key],
                fg="white" if self.is_dark_color(colors[color_key]) else "black",
                pady=5
            ).pack(fill=tk.X, padx=10, pady=2)
        
        tk.Button(
            preview_window,
            text="Close Preview",
            command=preview_window.destroy,
            bg=colors["accent_color"],
            fg="white"
        ).pack(pady=10)

    def apply_cmd_theme(self):
        """Apply theme to Windows CMD."""
        self.log_message("Applying theme to Windows CMD...", "info")
        
        try:
            ps_script_path = self.project_root / "apply-cmd-theme.ps1"
            
            if not ps_script_path.exists():
                self.log_message("PowerShell script not found", "error")
                messagebox.showerror("Error", "CMD theme script not found")
                return
            
            def run_cmd_theme():
                try:
                    result = subprocess.run([
                        "powershell.exe", 
                        "-ExecutionPolicy", "Bypass",
                        "-File", str(ps_script_path),
                        "-Backup"
                    ], capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0:
                        self.log_message("CMD theme applied successfully!", "success")
                        self.log_message("Open a new CMD window to see changes", "info")
                        messagebox.showinfo("Success", "CMD theme applied! Open a new Command Prompt to see changes.")
                    else:
                        self.log_message(f"CMD theme failed: {result.stderr}", "error")
                        messagebox.showerror("Error", f"Failed to apply CMD theme:\n{result.stderr}")
                        
                except subprocess.TimeoutExpired:
                    self.log_message("CMD theme script timed out", "error")
                    messagebox.showerror("Error", "Theme application timed out")
                except Exception as e:
                    self.log_message(f"CMD theme error: {e}", "error")
                    messagebox.showerror("Error", f"Failed to apply CMD theme: {e}")
            
            # Run in separate thread to avoid blocking UI
            threading.Thread(target=run_cmd_theme, daemon=True).start()
            
        except Exception as e:
            self.log_message(f"CMD theme error: {e}", "error")
            messagebox.showerror("Error", f"Failed to apply CMD theme: {e}")

    def reset_theme(self):
        """Reset theme to default."""
        if messagebox.askyesno("Reset Theme", "Reset to default Academic Apex theme?"):
            self.theme_config["colors"] = {
                "primary_bg": "#1a1a1a",
                "secondary_bg": "#2d2d2d",
                "accent_color": "#4a9eff",
                "text_primary": "#ffffff",
                "text_secondary": "#b0b0b0",
                "success_color": "#4caf50",
                "warning_color": "#ff9800",
                "error_color": "#f44336"
            }
            
            self.selected_theme.set("academic_apex")
            self.update_color_buttons()
            self.apply_theme()
            self.log_message("Theme reset to default", "success")

    def load_config(self):
        """Load configuration from file."""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    self.theme_config.update(loaded_config)
                    self.log_message("Configuration loaded", "success")
        except Exception as e:
            self.log_message(f"Failed to load config: {e}", "error")

    def save_config(self):
        """Save current configuration."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.theme_config, f, indent=2)
            self.log_message("Configuration saved", "success")
            messagebox.showinfo("Success", "Theme configuration saved!")
        except Exception as e:
            self.log_message(f"Failed to save config: {e}", "error")
            messagebox.showerror("Error", f"Failed to save configuration: {e}")

    def log_message(self, message, msg_type="info"):
        """Add message to status log."""
        timestamp = time.strftime("%H:%M:%S")
        
        colors = {
            "info": "#ffffff",
            "success": "#4caf50",
            "warning": "#ff9800",
            "error": "#f44336"
        }
        
        color = colors.get(msg_type, "#ffffff")
        
        self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
        
        # Color the last line
        last_line = self.status_text.index(tk.END + "-2l")
        current_line = self.status_text.index(tk.END + "-1l")
        
        self.status_text.tag_add(msg_type, last_line, current_line)
        self.status_text.tag_config(msg_type, foreground=color)
        
        # Auto-scroll to bottom
        self.status_text.see(tk.END)
        
        # Limit log length
        line_count = int(self.status_text.index(tk.END).split('.')[0])
        if line_count > 100:
            self.status_text.delete('1.0', '20.0')

    def on_closing(self):
        """Handle application closing."""
        if messagebox.askokcancel("Quit", "Close Academic Apex Theme Overlay?"):
            self.save_config()
            self.root.quit()
            self.root.destroy()

    def run(self):
        """Start the application."""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing()


def main():
    """Main entry point."""
    try:
        app = ThemeOverlay()
        app.run()
    except Exception as e:
        print(f"Failed to start theme overlay: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
