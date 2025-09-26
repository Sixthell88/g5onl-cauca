# fishing_core.py - Core functions for Auto Fishing Tool
import time
import pyautogui
import threading

def perform_fishing_cycle(tool_instance):
    """Core fishing cycle logic"""
    try:
        # Check doivitri if configured
        if tool_instance.doivitri_path:
            tool_instance.log_message("🔍 Kiểm tra doivitri.png...")
            doivitri_pos = tool_instance.find_image_on_screen(tool_instance.doivitri_path)
            
            if doivitri_pos:
                tool_instance.log_message(f"⚠️ Phát hiện doivitri tại {doivitri_pos}")
                if tool_instance.handle_doivitri():
                    tool_instance.log_message("📌 Tiếp tục chu kỳ sau doivitri...")
                else:
                    return False
        
        # Wait for cauca
        tool_instance.log_message("1️⃣ Chờ cauca.png xuất hiện...")
        cauca_pos = tool_instance.wait_and_find_image(tool_instance.cauca_path, 1200)
        if not cauca_pos or not tool_instance.running:
            return False
        
        # Press R sequence
        tool_instance.log_message("2️⃣3️⃣ Thực hiện chuỗi ấn phím R...")
        if not tool_instance.press_r_sequence() or not tool_instance.running:
            return False
        
        # Wait before F2
        wait_time = tool_instance.wait_before_f2.get()
        tool_instance.log_message(f"4️⃣ Chờ {wait_time}s trước khi ấn F2...")
        time.sleep(wait_time)
        
        if not tool_instance.running:
            return False
        
        # Press F2
        if not tool_instance.press_f2_key():
            tool_instance.log_message("❌ Không thể ấn F2")
            return False
        
        # Wait after F2
        wait_after_f2 = tool_instance.wait_after_f2.get()
        tool_instance.log_message(f"6️⃣ Chờ {wait_after_f2}s sau F2...")
        time.sleep(wait_after_f2)
        
        if not tool_instance.running:
            return False
        
        # Find and click moicau
        tool_instance.log_message("7️⃣ Tìm moicau.png...")
        moicau_pos = tool_instance.wait_and_find_image(
            tool_instance.moicau_path, 
            tool_instance.moicau_search_timeout.get(),
            " sau F2"
        )
        
        if not moicau_pos or not tool_instance.running:
            return False
        
        tool_instance.log_message(f"🖱️ Click phải vào moicau tại {moicau_pos}")
        pyautogui.rightClick(moicau_pos[0], moicau_pos[1])
        
        time.sleep(1)
        
        # Find and click sudung
        tool_instance.log_message("8️⃣ Tìm sudung.png...")
        sudung_pos = tool_instance.wait_and_find_image(
            tool_instance.sudung_path, 
            tool_instance.sudung_search_timeout.get(),
            " trong menu"
        )
        
        if not sudung_pos or not tool_instance.running:
            return False
        
        tool_instance.log_message(f"🖱️ Click trái vào sudung tại {sudung_pos}")
        pyautogui.click(sudung_pos[0], sudung_pos[1])
        
        tool_instance.log_message("✅ === HOÀN THÀNH CHU KỲ ===")
        return True
        
    except Exception as e:
        tool_instance.log_message(f"❌ Lỗi trong chu kỳ: {str(e)}")
        return False

def validate_core():
    """Validate core functions are loaded"""
    return True
