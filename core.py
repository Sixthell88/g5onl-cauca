# core.py - Upload file này lên GitHub và lấy link raw
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import cv2
import numpy as np
import pyautogui
import threading
import time
import os
import sys
import ctypes
import json
import platform
from PIL import Image
from datetime import datetime

# Import các thư viện input
try:
    import pydirectinput
    pydirectinput.FAILSAFE = False
except:
    pydirectinput = None

try:
    import keyboard
except:
    keyboard = None

try:
    import win32api
    import win32con
except:
    win32api = None
    win32con = None

class AutoClickCore:
    def __init__(self, root, discord_monitor):
        self.root = root
        self.discord = discord_monitor
        self.root.title("[F] - AUTO CÂU CÁ GTA 5 ONLINE")
        self.root.geometry("600x800")
        self.root.resizable(False, False)
        
        # Set modern colors
        self.colors = {
            'bg': '#1e1e1e',
            'fg': '#ffffff',
            'accent': '#0078d4',
            'success': '#16c60c',
            'warning': '#ffb900',
            'error': '#d83b01',
            'card': '#2d2d30',
            'border': '#3e3e42'
        }
        
        self.root.configure(bg=self.colors['bg'])
        self.setup_styles()
        
        # Check admin
        self.is_admin = self.check_admin_status()
        
        # Variables
        self.running = False
        self.thread = None
        self.cycle_count = 0
        self.total_cycles = 0
        self.start_time = None
        
        # Image paths
        self.cauca_path = ""
        self.moicau_path = ""
        self.sudung_path = ""
        self.doivitri_path = ""
        
        # Default settings
        self.first_count = tk.IntVar(value=20)
        self.first_delay = tk.DoubleVar(value=0.5)
        self.second_count = tk.IntVar(value=12)
        self.second_delay = tk.DoubleVar(value=0.9)
        self.wait_before_f2 = tk.DoubleVar(value=2.0)
        self.wait_after_f2 = tk.DoubleVar(value=2.0)
        self.moicau_search_timeout = tk.IntVar(value=15)
        self.sudung_search_timeout = tk.IntVar(value=10)
        self.confidence_threshold = tk.DoubleVar(value=0.6)
        
        # Doivitri settings
        self.hold_s_time = tk.DoubleVar(value=2.0)
        self.hold_w_time = tk.DoubleVar(value=1.5)
        self.last_hold_key = "S"
        
        # F2 method
        self.f2_method = tk.StringVar(value="pydirectinput")
        
        # Configure pyautogui
        self.configure_pyautogui()
        
        # Setup UI
        self.setup_ui()
        
        # Load config
        self.load_config()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Title.TLabel', 
                       background=self.colors['bg'], 
                       foreground=self.colors['accent'], 
                       font=('Segoe UI', 18, 'bold'))
        
        style.configure('Card.TLabelFrame', 
                       background=self.colors['card'], 
                       foreground=self.colors['fg'], 
                       font=('Segoe UI', 10, 'bold'),
                       relief='flat', 
                       borderwidth=1)
        
        style.configure('Modern.TButton', 
                       background=self.colors['accent'], 
                       foreground='white', 
                       font=('Segoe UI', 10, 'bold'),
                       relief='flat',
                       borderwidth=0,
                       focuscolor='none')
        
        style.map('Modern.TButton',
                 background=[('active', '#106ebe'),
                           ('pressed', '#005a9e')])
        
        style.configure('Success.TButton', 
                       background=self.colors['success'], 
                       foreground='white', 
                       font=('Segoe UI', 11, 'bold'),
                       relief='flat',
                       borderwidth=0)
        
        style.configure('Error.TButton', 
                       background=self.colors['error'], 
                       foreground='white', 
                       font=('Segoe UI', 11, 'bold'),
                       relief='flat',
                       borderwidth=0)
    
    def check_admin_status(self):
        try:
            if os.name == 'nt':
                return ctypes.windll.shell32.IsUserAnAdmin()
            return True
        except:
            return False
    
    def configure_pyautogui(self):
        try:
            pyautogui.FAILSAFE = False
            pyautogui.PAUSE = 0.1
            test_screenshot = pyautogui.screenshot()
            if test_screenshot is None:
                raise Exception("Không thể chụp màn hình")
        except Exception as e:
            messagebox.showerror("Lỗi cấu hình", f"Lỗi khi cấu hình pyautogui: {e}")
    
    def save_config(self):
        try:
            config = {
                "images": {
                    "cauca_path": self.cauca_path,
                    "moicau_path": self.moicau_path,
                    "sudung_path": self.sudung_path,
                    "doivitri_path": self.doivitri_path
                },
                "settings": {
                    "first_count": self.first_count.get(),
                    "first_delay": self.first_delay.get(),
                    "second_count": self.second_count.get(),
                    "second_delay": self.second_delay.get(),
                    "wait_before_f2": self.wait_before_f2.get(),
                    "wait_after_f2": self.wait_after_f2.get(),
                    "moicau_search_timeout": self.moicau_search_timeout.get(),
                    "sudung_search_timeout": self.sudung_search_timeout.get(),
                    "confidence_threshold": self.confidence_threshold.get(),
                    "hold_s_time": self.hold_s_time.get(),
                    "hold_w_time": self.hold_w_time.get(),
                    "f2_method": self.f2_method.get()
                }
            }
            
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            
            messagebox.showinfo("Thành công", "Đã lưu cấu config!")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu config: {e}")
    
    def load_config(self):
        try:
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
            
            if not os.path.exists(config_path):
                return
            
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            if "images" in config:
                if config["images"]["cauca_path"] and os.path.exists(config["images"]["cauca_path"]):
                    self.cauca_path = config["images"]["cauca_path"]
                    self.cauca_label.config(text=f"✅ {os.path.basename(self.cauca_path)}", foreground=self.colors['success'])
                
                if config["images"]["moicau_path"] and os.path.exists(config["images"]["moicau_path"]):
                    self.moicau_path = config["images"]["moicau_path"]
                    self.moicau_label.config(text=f"✅ {os.path.basename(self.moicau_path)}", foreground=self.colors['success'])
                
                if config["images"]["sudung_path"] and os.path.exists(config["images"]["sudung_path"]):
                    self.sudung_path = config["images"]["sudung_path"]
                    self.sudung_label.config(text=f"✅ {os.path.basename(self.sudung_path)}", foreground=self.colors['success'])
                
                if config["images"]["doivitri_path"] and os.path.exists(config["images"]["doivitri_path"]):
                    self.doivitri_path = config["images"]["doivitri_path"]
                    self.doivitri_label.config(text=f"✅ {os.path.basename(self.doivitri_path)}", foreground=self.colors['success'])
            
            if "settings" in config:
                settings = config["settings"]
                for key, var in [
                    ("first_count", self.first_count),
                    ("first_delay", self.first_delay),
                    ("second_count", self.second_count),
                    ("second_delay", self.second_delay),
                    ("wait_before_f2", self.wait_before_f2),
                    ("wait_after_f2", self.wait_after_f2),
                    ("moicau_search_timeout", self.moicau_search_timeout),
                    ("sudung_search_timeout", self.sudung_search_timeout),
                    ("confidence_threshold", self.confidence_threshold),
                    ("hold_s_time", self.hold_s_time),
                    ("hold_w_time", self.hold_w_time),
                    ("f2_method", self.f2_method)
                ]:
                    if key in settings:
                        var.set(settings[key])
        except:
            pass
    
    def press_f2_key(self):
        try:
            method = self.f2_method.get()
            time.sleep(0.1)
            
            if method == "pydirectinput" and pydirectinput:
                pydirectinput.press('f2')
                return True
            elif method == "keyboard" and keyboard:
                keyboard.press_and_release('f2')
                return True
            else:
                pyautogui.press('f2')
                return True
        except:
            return False
    
    def hold_key_advanced(self, key, hold_time):
        try:
            if pydirectinput:
                pydirectinput.keyDown(key.lower())
                time.sleep(hold_time)
                pydirectinput.keyUp(key.lower())
            else:
                pyautogui.keyDown(key.lower())
                time.sleep(hold_time)
                pyautogui.keyUp(key.lower())
            return True
        except:
            return False
    
    def find_image_on_screen(self, template_path, confidence=None):
        if confidence is None:
            confidence = self.confidence_threshold.get()
            
        try:
            screenshot = pyautogui.screenshot()
            if screenshot is None:
                return None
                
            screenshot_np = np.array(screenshot)
            screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            
            template = cv2.imread(template_path)
            if template is None:
                return None
            
            result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= confidence:
                h, w = template.shape[:2]
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                return (center_x, center_y)
            
            return None
        except:
            return None
    
    def wait_and_find_image(self, template_path, timeout_seconds):
        image_name = os.path.basename(template_path)
        self.log_message(f"🔍 Searching for {image_name}...")
        
        start_time = time.time()
        
        while self.running and (time.time() - start_time) < timeout_seconds:
            pos = self.find_image_on_screen(template_path)
            
            if pos:
                elapsed = time.time() - start_time
                self.log_message(f"✅ Found {image_name} at {pos} ({elapsed:.1f}s)")
                return pos
            
            time.sleep(0.3)
        
        self.log_message(f"❌ {image_name} not found after {timeout_seconds}s")
        return None
    
    def press_r_sequence(self):
        try:
            self.log_message("🎯 Starting R key sequence...")
            
            # Phase 1
            for i in range(self.first_count.get()):
                if not self.running:
                    return False
                pyautogui.press('r')
                if i < self.first_count.get() - 1:
                    time.sleep(self.first_delay.get())
            
            # Phase 2
            for i in range(self.second_count.get()):
                if not self.running:
                    return False
                pyautogui.press('r')
                if i < self.second_count.get() - 1:
                    time.sleep(self.second_delay.get())
            
            self.log_message("✅ R key sequence completed")
            return True
        except Exception as e:
            self.log_message(f"❌ R key sequence error: {e}")
            return False
    
    def handle_doivitri(self):
        try:
            # Chọn phím giữ
            if self.last_hold_key == "S":
                hold_key = "W"
                hold_time = self.hold_w_time.get()
                self.last_hold_key = "W"
            else:
                hold_key = "S"
                hold_time = self.hold_s_time.get()
                self.last_hold_key = "S"
            
            # Giữ phím
            if not self.hold_key_advanced(hold_key, hold_time):
                return False
            
            time.sleep(0.5)
            
            # Ấn phím 4
            pyautogui.press('4')
            time.sleep(0.5)
            
            # Ấn F2
            if not self.press_f2_key():
                return False
            
            time.sleep(1)
            
            # Tìm moicau
            moicau_pos = self.wait_and_find_image(
                self.moicau_path, 
                self.moicau_search_timeout.get()
            )
            
            if not moicau_pos:
                return False
            
            pyautogui.rightClick(moicau_pos[0], moicau_pos[1])
            time.sleep(1)
            
            # Tìm sudung
            sudung_pos = self.wait_and_find_image(
                self.sudung_path, 
                self.sudung_search_timeout.get()
            )
            
            if not sudung_pos:
                return False
            
            pyautogui.click(sudung_pos[0], sudung_pos[1])
            
            return True
        except:
            return False
    
    def automation_cycle(self):
        try:
            self.log_message(f"🚀 Starting Cycle {self.cycle_count}")
            
            # Check doivitri
            if self.doivitri_path:
                doivitri_pos = self.find_image_on_screen(self.doivitri_path)
                if doivitri_pos:
                    self.log_message(f"⚠️ Doivitri detected at {doivitri_pos}")
                    if self.handle_doivitri():
                        self.log_message("✅ Doivitri handled successfully")
                    else:
                        return False
            
            # Wait for cauca
            cauca_pos = self.wait_and_find_image(self.cauca_path, 1200)
            if not cauca_pos or not self.running:
                return False
            
            # Press R sequence
            if not self.press_r_sequence() or not self.running:
                return False
            
            # Wait before F2
            wait_time = self.wait_before_f2.get()
            self.log_message(f"⏳ Waiting {wait_time}s before F2...")
            time.sleep(wait_time)
            
            if not self.running:
                return False
            
            # Press F2
            self.log_message("⌨️ Pressing F2...")
            if not self.press_f2_key():
                self.log_message("❌ F2 press failed")
                return False
            
            # Wait after F2
            wait_after_f2 = self.wait_after_f2.get()
            self.log_message(f"⏳ Waiting {wait_after_f2}s after F2...")
            time.sleep(wait_after_f2)
            
            if not self.running:
                return False
            
            # Find and click moicau
            moicau_pos = self.wait_and_find_image(
                self.moicau_path, 
                self.moicau_search_timeout.get()
            )
            
            if not moicau_pos or not self.running:
                return False
            
            self.log_message(f"🖱️ Right clicking moicau at {moicau_pos}")
            pyautogui.rightClick(moicau_pos[0], moicau_pos[1])
            
            time.sleep(1)
            
            # Find and click sudung
            sudung_pos = self.wait_and_find_image(
                self.sudung_path, 
                self.sudung_search_timeout.get()
            )
            
            if not sudung_pos or not self.running:
                return False
            
            self.log_message(f"🖱️ Left clicking sudung at {sudung_pos}")
            pyautogui.click(sudung_pos[0], sudung_pos[1])
            
            self.log_message(f"✅ Cycle {self.cycle_count} completed successfully")
            return True
            
        except Exception as e:
            self.log_message(f"❌ Cycle error: {str(e)}")
            return False
    
    def automation_thread(self):
        self.cycle_count = 0
        
        try:
            while self.running:
                self.cycle_count += 1
                self.total_cycles += 1
                
                # Update cycle counter
                self.root.after(0, lambda: self.cycle_label.config(
                    text=f"Cycles: {self.cycle_count} | Total: {self.total_cycles}"))
                
                success = self.automation_cycle()
                
                if not success:
                    if self.running:
                        self.log_message(f"❌ Cycle {self.cycle_count} failed")
                    break
                
                if self.running:
                    time.sleep(3)
                
        except Exception as e:
            self.log_message(f"❌ Thread error: {e}")
        finally:
            self.root.after(0, self.reset_ui_after_stop)
    
    def start_automation(self):
        # Check required images
        if not all([self.cauca_path, self.moicau_path, self.sudung_path]):
            messagebox.showerror("Error", "Please select all 3 required image files!")
            return
        
        # Check file existence
        for path, name in [(self.cauca_path, "cauca.png"), 
                          (self.moicau_path, "moicau.png"), 
                          (self.sudung_path, "sudung.png")]:
            if not os.path.exists(path):
                messagebox.showerror("Error", f"File {name} does not exist!")
                return
        
        # Check optional doivitri
        if self.doivitri_path and not os.path.exists(self.doivitri_path):
            messagebox.showerror("Error", "Doivitri.png file does not exist!")
            return
        
        # Reset state
        self.last_hold_key = "W"
        self.cycle_count = 0
        self.start_time = time.time()
        
        # Update UI
        self.running = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        
        # Log start
        self.log_message("🚀 AUTOMATION STARTED")
        self.log_message(f"Method: {self.f2_method.get()}")
        self.log_message(f"Admin: {'Yes' if self.is_admin else 'No'}")
        if self.doivitri_path:
            self.log_message("Doivitri: Configured")
        self.log_message("=" * 50)
        
        # Start thread
        self.thread = threading.Thread(target=self.automation_thread, daemon=True)
        self.thread.start()
    
    def stop_automation(self):
        self.running = False
        self.log_message("🛑 Stopping automation...")
    
    def reset_ui_after_stop(self):
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.log_message("🛑 AUTOMATION STOPPED")
        self.log_message("=" * 50)
    
    def log_message(self, message):
        timestamp = time.strftime('%H:%M:%S')
        self.status_text.insert('end', f"[{timestamp}] {message}\n")
        self.status_text.see('end')
        self.root.update()
    
    def select_image(self, image_type):
        file_path = filedialog.askopenfilename(
            title=f"Select {image_type}.png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                test_img = cv2.imread(file_path)
                if test_img is None:
                    raise Exception("Cannot read image file")
                    
                if image_type == "cauca":
                    self.cauca_path = file_path
                    self.cauca_label.config(text=f"✅ {os.path.basename(file_path)}", 
                                          foreground=self.colors['success'])
                elif image_type == "moicau":
                    self.moicau_path = file_path
                    self.moicau_label.config(text=f"✅ {os.path.basename(file_path)}", 
                                           foreground=self.colors['success'])
                elif image_type == "sudung":
                    self.sudung_path = file_path
                    self.sudung_label.config(text=f"✅ {os.path.basename(file_path)}", 
                                           foreground=self.colors['success'])
                elif image_type == "doivitri":
                    self.doivitri_path = file_path
                    self.doivitri_label.config(text=f"✅ {os.path.basename(file_path)}", 
                                             foreground=self.colors['success'])
                    
            except Exception as e:
                messagebox.showerror("Error", f"Cannot read image file: {e}")
    
    def create_card(self, parent, title):
        card = tk.Frame(parent, bg=self.colors['card'], relief='flat', bd=1)
        card.pack(fill='x', pady=(0, 15))
        
        # Card header
        header = tk.Frame(card, bg=self.colors['accent'], height=30)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        title_label = tk.Label(header, text=title, 
                              bg=self.colors['accent'], fg='white',
                              font=('Segoe UI', 10, 'bold'))
        title_label.pack(pady=8)
        
        # Card content
        content = tk.Frame(card, bg=self.colors['card'])
        content.pack(fill='both', expand=True, padx=15, pady=15)
        
        return content
    
    def create_setting_row(self, parent, label_text, variable, min_val, max_val):
        row = tk.Frame(parent, bg=self.colors['card'])
        row.pack(fill='x', pady=3)
        
        label = tk.Label(row, text=label_text, 
                        bg=self.colors['card'], fg=self.colors['fg'],
                        font=('Segoe UI', 9), width=15, anchor='w')
        label.pack(side='left')
        
        if isinstance(variable.get(), float):
            increment = 0.1
        else:
            increment = 1
            
        spinbox = tk.Spinbox(row, from_=min_val, to=max_val, increment=increment,
                           textvariable=variable, width=8, font=('Segoe UI', 9),
                           bg='white', fg='black', relief='flat', bd=1)
        spinbox.pack(side='right')
    
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'], padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Title with status
        title_text = "[F] - Auto Câu Cá GTA 5 ONLINE"
        if self.is_admin:
            title_text += " ✅"
        else:
            title_text += " ⚠️"
            
        title_label = tk.Label(header_frame, text=title_text,
                              bg=self.colors['bg'], fg=self.colors['accent'],
                              font=('Segoe UI', 16, 'bold'))
        title_label.pack()
        
        # Version info
        version_label = tk.Label(header_frame, text="Make by : Furics & Unknownengine",
                                bg=self.colors['bg'], fg=self.colors['fg'],
                                font=('Segoe UI', 9))
        version_label.pack(pady=(5, 0))
        
        # Config buttons
        config_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        config_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Button(config_frame, text="💾 Save Config", 
                  command=self.save_config, style='Modern.TButton').pack(side='left', padx=(0, 10))
        ttk.Button(config_frame, text="📂 Load Config", 
                  command=self.load_config, style='Modern.TButton').pack(side='left')
        
        # Main content in cards
        content_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        content_frame.pack(fill='both', expand=True)
        
        # Left column
        left_column = tk.Frame(content_frame, bg=self.colors['bg'])
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Right column  
        right_column = tk.Frame(content_frame, bg=self.colors['bg'])
        right_column.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Images card
        self.setup_images_card(left_column)
        
        # F2 Methods card
        self.setup_f2_methods_card(left_column)
        
        # Settings cards
        self.setup_settings_cards(right_column)
        
        # Control panel
        self.setup_control_panel(main_frame)
        
        # Status display
        self.setup_status_display(main_frame)
    
    def setup_images_card(self, parent):
        content = self.create_card(parent, "Image Selection")
        
        images = [
            ("Cauca:", "cauca"),
            ("Moicau:", "moicau"), 
            ("Sudung:", "sudung"),
            ("Doivitri:", "doivitri")
        ]
        
        for i, (label_text, img_type) in enumerate(images):
            row_frame = tk.Frame(content, bg=self.colors['card'])
            row_frame.pack(fill='x', pady=5)
            
            label = tk.Label(row_frame, text=label_text, 
                           bg=self.colors['card'], fg=self.colors['fg'],
                           font=('Segoe UI', 9), width=8, anchor='w')
            label.pack(side='left')
            
            status_label = tk.Label(row_frame, text="❌ Chưa chọn", 
                                  bg=self.colors['card'], fg=self.colors['error'],
                                  font=('Segoe UI', 9), width=20, anchor='w')
            status_label.pack(side='left', padx=(10, 10))
            
            btn = ttk.Button(row_frame, text="📁", width=3,
                           command=lambda t=img_type: self.select_image(t),
                           style='Modern.TButton')
            btn.pack(side='right')
            
            setattr(self, f"{img_type}_label", status_label)
    
    def setup_f2_methods_card(self, parent):
        content = self.create_card(parent, "F2 Method")
        
        methods = [
            ("PyDirectInput", "pydirectinput"),
            ("Keyboard", "keyboard"),
            ("PyAutoGUI", "pyautogui")
        ]
        
        for text, value in methods:
            rb = tk.Radiobutton(content, text=text, variable=self.f2_method, value=value,
                              bg=self.colors['card'], fg=self.colors['fg'],
                              selectcolor=self.colors['accent'], activebackground=self.colors['card'],
                              font=('Segoe UI', 9))
            rb.pack(anchor='w', pady=2)
    
    def setup_settings_cards(self, parent):
        # R Key settings
        r_content = self.create_card(parent, "R Key Settings")
        
        settings = [
            ("First Count:", self.first_count, 1, 100),
            ("First Delay:", self.first_delay, 0.1, 10.0),
            ("Second Count:", self.second_count, 1, 100),
            ("Second Delay:", self.second_delay, 0.1, 10.0)
        ]
        
        for label_text, var, min_val, max_val in settings:
            self.create_setting_row(r_content, label_text, var, min_val, max_val)
        
        # Timing settings
        timing_content = self.create_card(parent, "Timing Settings")
        
        timing_settings = [
            ("Wait Before F2:", self.wait_before_f2, 0.5, 10.0),
            ("Wait After F2:", self.wait_after_f2, 0.5, 10.0),
            ("Moicau Timeout:", self.moicau_search_timeout, 5, 60),
            ("Sudung Timeout:", self.sudung_search_timeout, 5, 60),
            ("Confidence:", self.confidence_threshold, 0.3, 0.9)
        ]
        
        for label_text, var, min_val, max_val in timing_settings:
            self.create_setting_row(timing_content, label_text, var, min_val, max_val)
        
        # Doivitri settings
        doivitri_content = self.create_card(parent, "Doivitri Settings")
        
        doivitri_settings = [
            ("Hold S Time:", self.hold_s_time, 0.5, 10.0),
            ("Hold W Time:", self.hold_w_time, 0.5, 10.0)
        ]
        
        for label_text, var, min_val, max_val in doivitri_settings:
            self.create_setting_row(doivitri_content, label_text, var, min_val, max_val)
    
    def setup_control_panel(self, parent):
        control_frame = tk.Frame(parent, bg=self.colors['bg'])
        control_frame.pack(fill='x', pady=(20, 10))
        
        self.cycle_label = tk.Label(control_frame, text="Cycles: 0 | Total: 0", 
                                   bg=self.colors['bg'], fg=self.colors['fg'],
                                   font=('Segoe UI', 10))
        self.cycle_label.pack(pady=(0, 10))
        
        button_frame = tk.Frame(control_frame, bg=self.colors['bg'])
        button_frame.pack()
        
        self.start_button = ttk.Button(button_frame, text="START", 
                                      command=self.start_automation,
                                      style='Success.TButton', width=20)
        self.start_button.pack(side='left', padx=(0, 15))
        
        self.stop_button = ttk.Button(button_frame, text="STOP", 
                                     command=self.stop_automation, 
                                     style='Error.TButton', width=15,
                                     state='disabled')
        self.stop_button.pack(side='left')
    
    def setup_status_display(self, parent):
        status_frame = tk.Frame(parent, bg=self.colors['card'], relief='flat', bd=1)
        status_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        header = tk.Frame(status_frame, bg=self.colors['accent'])
        header.pack(fill='x')
        
        tk.Label(header, text="Status Log", 
                bg=self.colors['accent'], fg='white',
                font=('Segoe UI', 10, 'bold'), pady=8).pack()
        
        content = tk.Frame(status_frame, bg=self.colors['card'])
        content.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.status_text = tk.Text(content, height=8, width=70, wrap='word',
                                  bg='#2d2d30', fg='#ffffff', font=('Consolas', 9),
                                  relief='flat', bd=0, insertbackground='white')
        
        scrollbar = ttk.Scrollbar(content, orient='vertical', command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        self.status_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.log_message("Tool ready! Please configure settings and select images.")
