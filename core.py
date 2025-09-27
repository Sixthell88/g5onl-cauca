# Core automation functions - File này sẽ được load từ GitHub raw

async def send_status_update(self):
    """Gửi update status lên Discord"""
    try:
        if self.running:
            runtime = time.time() - self.start_time if self.start_time else 0
            hours = int(runtime // 3600)
            minutes = int((runtime % 3600) // 60)
            
            status_msg = f"""
🎣 **AUTO FISHING STATUS**
```yaml
Status: {'🟢 Running' if self.running else '🔴 Stopped'}
Cycles: {self.cycle_count}
Total: {self.total_cycles}
Runtime: {hours}h {minutes}m
Method: {self.f2_method.get()}
Admin: {'✅' if self.is_admin else '❌'}
```"""
            await self.discord.send_discord_message(status_msg)
    except:
        pass

def send_key_with_ctypes(self, key_code, scan_code=0):
    """Gửi phím trực tiếp qua ctypes Windows API"""
    try:
        KEYEVENTF_EXTENDEDKEY = 0x0001
        KEYEVENTF_KEYUP = 0x0002
        
        user32 = ctypes.windll.user32
        
        # Key down
        user32.keybd_event(key_code, scan_code, KEYEVENTF_EXTENDEDKEY, 0)
        time.sleep(0.05)
        
        # Key up
        user32.keybd_event(key_code, scan_code, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0)
        
        return True
    except Exception as e:
        return False

def send_key_with_win32api(self):
    """Gửi F2 qua win32api"""
    if win32api is None or win32con is None:
        return False
        
    try:
        VK_F2 = 0x71
        
        # Key down
        win32api.keybd_event(VK_F2, 0, 0, 0)
        time.sleep(0.05)
        
        # Key up
        win32api.keybd_event(VK_F2, 0, win32con.KEYEVENTF_KEYUP, 0)
        
        return True
    except Exception as e:
        return False

def hold_key_advanced(self, key, hold_time):
    """Giữ phím với phương pháp nâng cao"""
    method = self.f2_method.get()
    
    if method == "auto":
        methods = [
            ("pydirectinput", lambda: self.hold_with_pydirectinput(key, hold_time)),
            ("keyboard", lambda: self.hold_with_keyboard(key, hold_time)),
            ("pyautogui", lambda: self.hold_with_pyautogui(key, hold_time))
        ]
        
        for name, func in methods:
            if func():
                return True
        
        return False
    else:
        method_map = {
            "pydirectinput": lambda: self.hold_with_pydirectinput(key, hold_time),
            "keyboard": lambda: self.hold_with_keyboard(key, hold_time),
            "pyautogui": lambda: self.hold_with_pyautogui(key, hold_time)
        }
        
        if method in method_map:
            if method_map[method]():
                return True
    
    return False

def hold_with_pydirectinput(self, key, hold_time):
    """Giữ phím với pydirectinput"""
    if pydirectinput is None:
        return False
    try:
        pydirectinput.keyDown(key.lower())
        time.sleep(hold_time)
        pydirectinput.keyUp(key.lower())
        return True
    except:
        return False

def hold_with_keyboard(self, key, hold_time):
    """Giữ phím với keyboard"""
    if keyboard is None:
        return False
    try:
        keyboard.press(key.lower())
        time.sleep(hold_time)
        keyboard.release(key.lower())
        return True
    except:
        return False

def hold_with_pyautogui(self, key, hold_time):
    """Giữ phím với pyautogui"""
    try:
        pyautogui.keyDown(key.lower())
        time.sleep(hold_time)
        pyautogui.keyUp(key.lower())
        return True
    except:
        return False

def press_key_advanced(self, key):
    """Ấn phím với phương pháp nâng cao"""
    method = self.f2_method.get()
    
    if method == "auto":
        methods = [
            ("pydirectinput", lambda: pydirectinput.press(str(key)) if pydirectinput else False),
            ("keyboard", lambda: keyboard.press_and_release(str(key)) if keyboard else False),
            ("pyautogui", lambda: pyautogui.press(str(key)))
        ]
        
        for name, func in methods:
            try:
                if func():
                    return True
            except:
                pass
        
        return False
    else:
        try:
            if method == "pydirectinput" and pydirectinput:
                pydirectinput.press(str(key))
            elif method == "keyboard" and keyboard:
                keyboard.press_and_release(str(key))
            else:
                pyautogui.press(str(key))
            return True
        except:
            return False

def press_f2_key(self):
    """Ấn phím F2 với nhiều phương pháp khác nhau"""
    try:
        method = self.f2_method.get()
        
        time.sleep(0.1)
        
        if method == "auto":
            methods = [
                ("pydirectinput", self.method_pydirectinput),
                ("keyboard", self.method_keyboard),
                ("win32api", self.method_win32api),
                ("ctypes", self.method_ctypes),
                ("pyautogui_multi", self.method_pyautogui_multi)
            ]
            
            for name, func in methods:
                if func():
                    return True
                time.sleep(0.1)
            
            return False
        else:
            method_map = {
                "pydirectinput": self.method_pydirectinput,
                "keyboard": self.method_keyboard,
                "win32api": self.method_win32api,
                "ctypes": self.method_ctypes,
                "pyautogui": self.method_pyautogui_multi
            }
            
            if method in method_map:
                if method_map[method]():
                    return True
                else:
                    return False
                    
        return False
        
    except Exception as e:
        return False

def method_pydirectinput(self):
    """Phương pháp pydirectinput"""
    if pydirectinput is None:
        return False
    try:
        pydirectinput.press('f2')
        time.sleep(0.1)
        return True
    except:
        return False

def method_keyboard(self):
    """Phương pháp keyboard"""
    if keyboard is None:
        return False
    try:
        keyboard.press_and_release('f2')
        time.sleep(0.1)
        return True
    except:
        return False

def method_win32api(self):
    """Phương pháp win32api"""
    return self.send_key_with_win32api()

def method_ctypes(self):
    """Phương pháp ctypes"""
    VK_F2 = 0x71
    return self.send_key_with_ctypes(VK_F2, 0x3C)

def method_pyautogui_multi(self):
    """Phương pháp pyautogui gửi nhiều lần"""
    try:
        for _ in range(3):
            pyautogui.press('f2')
            time.sleep(0.05)
        return True
    except:
        return False

def handle_doivitri(self):
    """Xử lý khi phát hiện doivitri.png"""
    try:
        # Send Discord notification
        asyncio.run_coroutine_threadsafe(
            self.discord.send_discord_message("🔄 **DOIVITRI DETECTED!**\nĐang xử lý đổi vị trí..."),
            self.discord.client.loop
        )
        
        # Chọn phím giữ
        if self.last_hold_key == "S":
            hold_key = "W"
            hold_time = self.hold_w_time.get()
            self.last_hold_key = "W"
        else:
            hold_key = "S"
            hold_time = self.hold_s_time.get()
            self.last_hold_key = "S"
        
        # 1. Giữ phím
        if not self.hold_key_advanced(hold_key, hold_time):
            return False
        
        time.sleep(0.5)
        
        # 2. Ấn phím 4
        if not self.press_key_advanced('4'):
            pass
        
        time.sleep(0.5)
        
        # 3. Ấn F2
        if not self.press_f2_key():
            return False
        
        time.sleep(1)
        
        # 4. Tìm moicau
        moicau_pos = self.wait_and_find_image(
            self.moicau_path, 
            self.moicau_search_timeout.get()
        )
        
        if not moicau_pos:
            return False
        
        pyautogui.rightClick(moicau_pos[0], moicau_pos[1])
        
        time.sleep(1)
        
        # 5. Tìm sudung
        sudung_pos = self.wait_and_find_image(
            self.sudung_path, 
            self.sudung_search_timeout.get()
        )
        
        if not sudung_pos:
            return False
        
        pyautogui.click(sudung_pos[0], sudung_pos[1])
        
        return True
        
    except Exception as e:
        return False

def find_image_on_screen(self, template_path, confidence=None):
    """Tìm hình ảnh trên màn hình"""
    if confidence is None:
        confidence = self.confidence_threshold.get()
        
    try:
        # Take screenshot
        screenshot = None
        for attempt in range(3):
            try:
                screenshot = pyautogui.screenshot()
                if screenshot:
                    break
            except Exception:
                if attempt == 2:
                    return None
                time.sleep(0.1)
        
        if screenshot is None:
            return None
            
        # Convert to numpy array
        screenshot_np = np.array(screenshot)
        screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
        
        # Read template
        template = cv2.imread(template_path)
        if template is None:
            return None
        
        # Match template
        result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= confidence:
            h, w = template.shape[:2]
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            return (center_x, center_y)
        
        return None
        
    except Exception:
        return None

def wait_and_find_image(self, template_path, timeout_seconds):
    """Chờ và tìm hình ảnh trong khoảng thời gian nhất định"""
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
    """Thực hiện chuỗi ấn phím R"""
    try:
        self.log_message("🎯 Starting R key sequence...")
        
        # Phase 1
        self.log_message(f"Phase 1: {self.first_count.get()} presses, {self.first_delay.get()}s delay")
        for i in range(self.first_count.get()):
            if not self.running:
                return False
            
            pyautogui.press('r')
            
            if i < self.first_count.get() - 1:
                time.sleep(self.first_delay.get())
        
        # Phase 2
        self.log_message(f"Phase 2: {self.second_count.get()} presses, {self.second_delay.get()}s delay")
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

def automation_cycle(self):
    """Một chu kỳ automation hoàn chỉnh"""
    try:
        self.log_message(f"🚀 Starting Cycle {self.cycle_count}")
        
        # Send status update every 10 cycles
        if self.cycle_count % 10 == 0:
            asyncio.run_coroutine_threadsafe(
                self.send_status_update(),
                self.discord.client.loop
            )
        
        # 1. Check doivitri
        if self.doivitri_path:
            doivitri_pos = self.find_image_on_screen(self.doivitri_path)
            
            if doivitri_pos:
                self.log_message(f"⚠️ Doivitri detected at {doivitri_pos}")
                if self.handle_doivitri():
                    self.log_message("✅ Doivitri handled successfully")
                else:
                    return False
        
        # 2. Wait for cauca
        cauca_pos = self.wait_and_find_image(self.cauca_path, 1200)
        if not cauca_pos or not self.running:
            return False
        
        # 3. Press R sequence
        if not self.press_r_sequence() or not self.running:
            return False
        
        # 4. Wait before F2
        wait_time = self.wait_before_f2.get()
        self.log_message(f"⏳ Waiting {wait_time}s before F2...")
        time.sleep(wait_time)
        
        if not self.running:
            return False
        
        # 5. Press F2
        self.log_message("⌨️ Pressing F2...")
        if not self.press_f2_key():
            self.log_message("❌ F2 press failed")
            if not self.is_admin:
                self.log_message("💡 Try running as Admin")
            return False
        
        # 6. Wait after F2
        wait_after_f2 = self.wait_after_f2.get()
        self.log_message(f"⏳ Waiting {wait_after_f2}s after F2...")
        time.sleep(wait_after_f2)
        
        if not self.running:
            return False
        
        # 7. Find and click moicau
        moicau_pos = self.wait_and_find_image(
            self.moicau_path, 
            self.moicau_search_timeout.get()
        )
        
        if not moicau_pos or not self.running:
            return False
        
        self.log_message(f"🖱️ Right clicking moicau at {moicau_pos}")
        pyautogui.rightClick(moicau_pos[0], moicau_pos[1])
        
        time.sleep(1)
        
        # 8. Find and click sudung
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
    """Thread chạy automation"""
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

def start_automation_core(self):
    """Bắt đầu automation - Core function"""
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
    
    # Send Discord notification
    asyncio.run_coroutine_threadsafe(
        self.discord.send_discord_message(f"🎣 **STARTED AUTO FISHING**\nMethod: {self.f2_method.get()}\nAdmin: {'✅' if self.is_admin else '❌'}"),
        self.discord.client.loop
    )
    
    # Start thread
    self.thread = threading.Thread(target=self.automation_thread, daemon=True)
    self.thread.start()

def stop_automation_core(self):
    """Dừng automation - Core function"""
    self.running = False
    self.log_message("🛑 Stopping automation...")
    
    # Send Discord notification
    asyncio.run_coroutine_threadsafe(
        self.discord.send_discord_message(f"⏹️ **STOPPED AUTO FISHING**\nTotal cycles: {self.total_cycles}"),
        self.discord.client.loop
    )

def reset_ui_after_stop(self):
    """Reset UI sau khi dừng"""
    self.start_button.config(state='normal')
    self.stop_button.config(state='disabled')
    self.log_message("🛑 AUTOMATION STOPPED")
    self.log_message("=" * 50)
