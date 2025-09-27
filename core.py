# core.py - Chỉ upload file nhỏ này lên GitHub
import pyautogui
import cv2
import numpy as np
import time
import os

class AutomationCore:
    """Core automation engine - Required for tool to work"""
    
    VERSION = "1.0.0"
    VALID = True
    
    @staticmethod
    def verify():
        """Verify core is valid"""
        return AutomationCore.VALID
    
    @staticmethod
    def find_image_on_screen(template_path, confidence=0.6):
        """Core image detection"""
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
    
    @staticmethod
    def press_r_sequence(first_count, first_delay, second_count, second_delay):
        """Core R key sequence"""
        try:
            # Phase 1
            for i in range(first_count):
                pyautogui.press('r')
                if i < first_count - 1:
                    time.sleep(first_delay)
            
            # Phase 2
            for i in range(second_count):
                pyautogui.press('r')
                if i < second_count - 1:
                    time.sleep(second_delay)
            
            return True
        except:
            return False
    
    @staticmethod
    def press_f2_key(method="pydirectinput"):
        """Core F2 press"""
        try:
            time.sleep(0.1)
            
            if method == "pydirectinput":
                try:
                    import pydirectinput
                    pydirectinput.press('f2')
                    return True
                except:
                    pass
            
            if method == "keyboard":
                try:
                    import keyboard
                    keyboard.press_and_release('f2')
                    return True
                except:
                    pass
            
            # Fallback to pyautogui
            pyautogui.press('f2')
            return True
            
        except:
            return False
    
    @staticmethod
    def hold_key(key, hold_time):
        """Core key holding"""
        try:
            try:
                import pydirectinput
                pydirectinput.keyDown(key.lower())
                time.sleep(hold_time)
                pydirectinput.keyUp(key.lower())
                return True
            except:
                pyautogui.keyDown(key.lower())
                time.sleep(hold_time)
                pyautogui.keyUp(key.lower())
                return True
        except:
            return False
    
    @staticmethod
    def automation_cycle(params):
        """Core automation cycle"""
        try:
            # Check doivitri if configured
            if params.get('doivitri_path'):
                doivitri_pos = AutomationCore.find_image_on_screen(
                    params['doivitri_path'],
                    params.get('confidence', 0.6)
                )
                
                if doivitri_pos:
                    # Handle doivitri
                    hold_key = params.get('hold_key', 'S')
                    hold_time = params.get('hold_time', 2.0)
                    
                    AutomationCore.hold_key(hold_key, hold_time)
                    time.sleep(0.5)
                    pyautogui.press('4')
                    time.sleep(0.5)
                    AutomationCore.press_f2_key(params.get('f2_method', 'pydirectinput'))
                    time.sleep(1)
                    
                    # Click moicau
                    moicau_pos = AutomationCore.wait_and_find(
                        params['moicau_path'],
                        params.get('moicau_timeout', 15),
                        params.get('confidence', 0.6)
                    )
                    if moicau_pos:
                        pyautogui.rightClick(moicau_pos[0], moicau_pos[1])
                        time.sleep(1)
                    
                    # Click sudung
                    sudung_pos = AutomationCore.wait_and_find(
                        params['sudung_path'],
                        params.get('sudung_timeout', 10),
                        params.get('confidence', 0.6)
                    )
                    if sudung_pos:
                        pyautogui.click(sudung_pos[0], sudung_pos[1])
            
            # Wait for cauca
            cauca_pos = AutomationCore.wait_and_find(
                params['cauca_path'],
                1200,
                params.get('confidence', 0.6)
            )
            
            if not cauca_pos:
                return False
            
            # Press R sequence
            if not AutomationCore.press_r_sequence(
                params.get('first_count', 20),
                params.get('first_delay', 0.5),
                params.get('second_count', 12),
                params.get('second_delay', 0.9)
            ):
                return False
            
            # Wait before F2
            time.sleep(params.get('wait_before_f2', 2.0))
            
            # Press F2
            if not AutomationCore.press_f2_key(params.get('f2_method', 'pydirectinput')):
                return False
            
            # Wait after F2
            time.sleep(params.get('wait_after_f2', 2.0))
            
            # Find and click moicau
            moicau_pos = AutomationCore.wait_and_find(
                params['moicau_path'],
                params.get('moicau_timeout', 15),
                params.get('confidence', 0.6)
            )
            
            if not moicau_pos:
                return False
            
            pyautogui.rightClick(moicau_pos[0], moicau_pos[1])
            time.sleep(1)
            
            # Find and click sudung
            sudung_pos = AutomationCore.wait_and_find(
                params['sudung_path'],
                params.get('sudung_timeout', 10),
                params.get('confidence', 0.6)
            )
            
            if not sudung_pos:
                return False
            
            pyautogui.click(sudung_pos[0], sudung_pos[1])
            
            return True
            
        except Exception as e:
            return False
    
    @staticmethod
    def wait_and_find(template_path, timeout_seconds, confidence=0.6):
        """Wait and find image"""
        start_time = time.time()
        
        while (time.time() - start_time) < timeout_seconds:
            pos = AutomationCore.find_image_on_screen(template_path, confidence)
            if pos:
                return pos
            time.sleep(0.3)
        
        return None
