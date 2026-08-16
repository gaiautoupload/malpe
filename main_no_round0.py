import pygetwindow as gw
import pyautogui
pyautogui.FAILSAFE = False
import datetime
import time
import random
import mss
import cv2
import os
import pytesseract
from PIL import ImageGrab  # 或使用 pyautogui
import numpy as np
# 若在 Windows，要設定 Tesseract 的路徑
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
# img = Image.open('chinese.jpg')
# text = pytesseract.image_to_string(img, lang='chi_tra')
# print(text)

count = 0
#腳色數量
endcount = 50
count_pass = 0 #從第幾隻腳側開始
count = count_pass
# monitor = {"top": y + 433, "left": x + 353, "width": 98, "height": 24}
def get_text_from_game_region(x, y,top,left,width,height):
    # 擷取固定畫面區域（相對視窗左上角）
    with mss.mss() as sct:
        #打粉結束檢測移動到選單
        monitor = {"top": y + top, "left": x + left, "width": width, "height": height}
        img = sct.grab(monitor)
        img_np = np.array(img)
        frame = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)  # 轉成 BGR 給 OpenCV 用

        # 顯示畫面（非必要，僅供 debug）
        cv2.imshow("OCR Region", frame)
        cv2.waitKey(1)

        # OCR：使用原始彩色圖
        custom_config = r'--oem 3 --psm 7'
        text = pytesseract.image_to_string(frame, lang='chi_tra', config=custom_config)
        clean_text = text.strip().replace(" ", "").replace("　", "")

        # print(f"[OCR] 偵測到文字：{text.strip()}")
        return clean_text


# =================設定區=================
WINDOW_TITLE = "MapleStoryM"   # 模擬器視窗標題
CHECKBOX_IMAGES = [
    r'ad_image\checkbox.png',   # 舊的白色框
    r'ad_image\checkbox2.png'   # 新的藍色框
]
AD_LOGO_IMG = r'ad_image\imagine_logo.png' # 廣告的大標題特徵 (選用，用來確認廣告出現)
LOG_FILE = r'ad_image\script_log.txt'
# ========================================

def write_log(message):
    """
    符合您要求的安全寫入 Log 方式：
    使用 try-except 區塊處理編碼，避免 with open() 後接冒號的語法問題。
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {message}\n"
    
    try:
        # 優先嘗試 utf-8
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_msg)
    except UnicodeEncodeError:
        # 若失敗則嘗試 big5 (常見於繁體中文系統)
        with open(LOG_FILE, "a", encoding="big5") as f:
            f.write(log_msg)
    except Exception as e:
        print(f"Log 寫入失敗: {e}")

def handle_ad_popup():
    """
    支援多種廣告樣式的偵測與處理
    """
    # 1. 取得遊戲視窗範圍
    region = get_window_position(WINDOW_TITLE)
    if not region:
        return False
        
    x, y, w, h = region
    
    # 2. 定義「下半部」搜尋範圍 (優化效能，只看視窗下半截)
    bottom_half_region = (x, y + int(h/2), w, int(h/2))

    # 3. 開始輪流檢查每一張廣告圖
    for img_path in CHECKBOX_IMAGES:
        try:
            # 檢查檔案是否存在，避免報錯
            if not os.path.exists(img_path):
                print(f"警告: 找不到圖片檔 {img_path}")
                continue

            # 搜尋圖片 (confidence=0.8)
            # 針對藍色背景的藍色框，grayscale=True 有時反而會讓對比度降低
            # 如果發現藍色框抓不到，可以試著把 grayscale=True 拿掉測試
            box_pos = pyautogui.locateOnScreen(img_path, region=bottom_half_region, confidence=0.8, grayscale=True)

            if box_pos:
                print(f"【偵測到廣告】樣式: {os.path.basename(img_path)}")
                
                # === 座標偏移計算 ===
                # 兩張圖的邏輯都是：框框在最左邊，文字在右邊
                # 所以我們抓圖片的 left，然後往右移一點點點擊中心
                
                # 舊的白框比較小，新的藍框看起來稍微大一點點，但 +25 應該都通用
                # 如果發現藍色框點歪了，可以把 +25 改大一點 (例如 +30)
                target_x = box_pos.left + 25 
                target_y = box_pos.top + (box_pos.height / 2)
                
                # 1. 點擊「今日不再顯示」
                pyautogui.click(target_x, target_y)
                write_log(f"已點擊廣告勾選框 ({os.path.basename(img_path)})")
                time.sleep(0.5)
                
                # 2. 關閉視窗 (嘗試按 ESC)
                pyautogui.press('esc')
                write_log("已發送 ESC 關閉廣告")
                
                # 3. 等待視窗消失 (稍微久一點，因為有動畫)
                time.sleep(1.5) 
                
                # 為了保險，有時候按一次 ESC 沒反應 (例如輸入法卡住)
                # 可以再檢查一次，如果廣告還在就再按一次 (這段是選用邏輯)
                # if pyautogui.locateOnScreen(img_path, region=bottom_half_region, confidence=0.8):
                #     pyautogui.press('esc')
                
                return True # 找到並處理了，直接結束函數，不用檢查下一張圖

        except pyautogui.ImageNotFoundException:
            continue # 這張圖沒找到，換下一張
        except Exception as e:
            print(f"檢查廣告圖片 {img_path} 時發生錯誤: {e}")

    # 迴圈跑完都沒找到
    return False
# 廣告辨識支援的圖片格式；圖片請放在 ad_image2 資料夾。
VALID_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp')

# --- 升等廣告設定 ---
AD_CONFIG_2 = {
    "folder": os.path.join(os.path.dirname(os.path.abspath(__file__)), "ad_image2"),
    "offset_x": 672,
    "offset_y": 127
}
# =========================================

def get_window_rect(title):
    try:
        windows = gw.getWindowsWithTitle(title)
        if not windows:
            return None
        win = windows[0]
        if win.isMinimized:
            win.restore()
        return (win.left, win.top, win.width, win.height)
    except Exception as e:
        print(f"找視窗時發生錯誤: {e}")
        return None

def get_images_from_folder(folder_name):
    """
    讀取指定資料夾內的所有圖片路徑
    """
    images = []
    if not os.path.exists(folder_name):
        return []
    
    for filename in os.listdir(folder_name):
        if filename.lower().endswith(VALID_EXTENSIONS):
            full_path = os.path.join(folder_name, filename)
            images.append(full_path)
    return images

def process_ad_group(win_x, win_y, search_region, config):
    """
    處理單一組廣告設定的核心邏輯
    回傳 True 代表有處理到廣告，False 代表沒事
    """
    folder = config["folder"]
    offset_x = config["offset_x"]
    offset_y = config["offset_y"]
    
    # 取得該資料夾圖片
    image_list = get_images_from_folder(folder)
    
    if not image_list:
        return False

    # Capture the requested window on every monitor before matching.
    region_x, region_y, region_width, region_height = search_region
    try:
        screen_capture = ImageGrab.grab(
            bbox=(
                region_x,
                region_y,
                region_x + region_width,
                region_y + region_height,
            ),
            all_screens=True,
        )
    except Exception as e:
        print(f"無法擷取遊戲視窗進行廣告辨識: {e}")
        return False

    # 掃描該組圖片
    for img_path in image_list:
        try:
            # 搜尋圖片
            location = pyautogui.locate(
                img_path,
                screen_capture,
                confidence=0.8,
                grayscale=True,
            )
        except pyautogui.ImageNotFoundException:
            location = None
        except Exception as e:
            print(f"廣告圖片比對失敗 ({img_path}): {e}")
            location = None

        if location:
            filename = os.path.basename(img_path)
            print(f"\n[{time.strftime('%H:%M:%S')}] 偵測到廣告類型！")
            print(f"  └─ 來源: {folder} | 圖片: {filename}")
            
            # 計算點擊座標
            target_abs_x = win_x + offset_x
            target_abs_y = win_y + offset_y
            
            print(f"  └─ 執行點擊 ({offset_x}, {offset_y}) -> 絕對座標: ({target_abs_x}, {target_abs_y})")
            pyautogui.click(target_abs_x, target_abs_y)
            
            time.sleep(0.5)
            
            print("  └─ 發送 ESC 關閉視窗...")
            pyautogui.press('esc')
            
            # 稍作休息，避免重複偵測
            time.sleep(2)
            return True # 處理成功，回傳 True

    return False

# 獲取窗口的位置和大小
def get_window_position(window_title):
    try:
        window = gw.getWindowsWithTitle(window_title)[0]
        x, y = window.left, window.top
        width, height = window.width, window.height
        # get_text_from_game_region(x,y)
        # while(1):
        #     # monitor = {"top": y + 433, "left": x + 353, "width": 98, "height": 24}
        #     re_OK = get_text_from_game_region(x, y,433,353,98,24)
        #     if re_OK=="移動至選單":
        #         print(re_OK,"eeeeeeeeeeeeee")
        #         break
        return (x, y, width, height)
    except IndexError:
        print(f"找不到標題為 '{window_title}' 的窗口")
        return None

# 顯示滑鼠在窗口內的相對位置，並在該位置進行點擊
def display_and_click_relative_position(window_title):
    try:
        while True:
            window_pos = get_window_position(window_title)
            if window_pos:
                print(f"窗口 '{window_title}' 位置: ({window_pos[0]}, {window_pos[1]}), 大小: ({window_pos[2]}x{window_pos[3]})")
                
                # 獲取滑鼠當前位置
                mouse_x, mouse_y = pyautogui.position()
                
                # 計算滑鼠相對於窗口的位置
                relative_x = mouse_x - window_pos[0]
                relative_y = mouse_y - window_pos[1]
                
                # 檢查滑鼠是否在窗口範圍內
                if 0 <= relative_x <= window_pos[2] and 0 <= relative_y <= window_pos[3]:
                    print(f"滑鼠相對位置: ({relative_x}, {relative_y})", end="\r")
                    
                    # 模擬點擊
                    # pyautogui.click(mouse_x, mouse_y)
                else:
                    print(f"滑鼠不在窗口範圍內", end="\r")

            else:
                print(f"無法獲取 '{window_title}' 的窗口位置", end="\r")
            
            time.sleep(0.5)  # 每0.5秒更新一次

    except KeyboardInterrupt:
        print("\n程序結束")
def round1():
    window_pos = get_window_position(WINDOW_TITLE)
    if not window_pos:
        print(f"找不到視窗 '{WINDOW_TITLE}'，略過 round1")
        return False

    time.sleep(random.randint(3, 5))
    while(1):
        re_OK = get_text_from_game_region(window_pos[0], window_pos[1],107,323,490-323,140-107)
        if "寵物剩餘" in re_OK:
            random_x_offset = random.randint(573, 574)
            random_y_offset = random.randint(117, 118)
            start_abs_x = window_pos[0] + random_x_offset
            start_abs_y = window_pos[1] + random_y_offset
            pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
            pyautogui.mouseDown()
            pyautogui.click()

        # monitor = {"top": y + 433, "left": x + 353, "width": 98, "height": 24}
        re_OK = get_text_from_game_region(window_pos[0], window_pos[1],433,353,98,24)
        if "寵物剩餘" not in re_OK:
            break
  

    now = datetime.datetime.now()
    # if 1<0:
    if now.hour < 20 or (now.hour == 20 and now.minute < 50):
        # ✅ 時間區間判斷：00:00 ~ 20:49 才執行
        #選單
        random_x_offset = random.randint(770, 789)
        random_y_offset = random.randint(38, 56)
        start_abs_x = window_pos[0] + random_x_offset
        start_abs_y = window_pos[1] + random_y_offset
        pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
        pyautogui.mouseDown()
        pyautogui.click()
        # time.sleep(random.randint(3, 5))


        #公會
        random_x_offset = random.randint(657, 712)
        random_y_offset = random.randint(307, 341)
        start_abs_x = window_pos[0] + random_x_offset
        start_abs_y = window_pos[1] + random_y_offset
        pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
        pyautogui.mouseDown()
        pyautogui.click()

        #榮譽站
        time.sleep(random.randint(2, 3))
        random_x_offset = random.randint(694, 741)
        random_y_offset = random.randint(305, 337)
        start_abs_x = window_pos[0] + random_x_offset
        start_abs_y = window_pos[1] + random_y_offset
        pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
        pyautogui.mouseDown()
        pyautogui.click()
        #榮譽站-確認(上一場確認輸贏)
        random_x_offset = random.randint(420, 425)
        random_y_offset = random.randint(434, 436)
        start_abs_x = window_pos[0] + random_x_offset
        start_abs_y = window_pos[1] + random_y_offset
        pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
        pyautogui.mouseDown()
        pyautogui.click()
        #榮譽站-確認
        random_x_offset = random.randint(420, 425)
        random_y_offset = random.randint(434, 436)
        start_abs_x = window_pos[0] + random_x_offset
        start_abs_y = window_pos[1] + random_y_offset
        pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
        pyautogui.mouseDown()
        pyautogui.click()
        #榮譽站-入場/開打
        random_x_offset = random.randint(330, 343)
        random_y_offset = random.randint(458, 461)
        start_abs_x = window_pos[0] + random_x_offset
        start_abs_y = window_pos[1] + random_y_offset
        pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
        pyautogui.mouseDown()
        pyautogui.click()
        random_x_offset = random.randint(330, 343)
        random_y_offset = random.randint(458, 461)
        start_abs_x = window_pos[0] + random_x_offset
        start_abs_y = window_pos[1] + random_y_offset
        pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
        pyautogui.mouseDown()
        pyautogui.click()
        time.sleep(random.randint(90, 100))

    #選單
    random_x_offset = random.randint(770, 789)
    random_y_offset = random.randint(38, 56)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    # time.sleep(random.randint(3, 5))

    #公會
    random_x_offset = random.randint(657, 712)
    random_y_offset = random.randint(307, 341)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()

    #領獎勵
    random_x_offset = random.randint(700, 730)
    random_y_offset = random.randint(108, 119)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #公會-按X
    random_x_offset = random.randint(773, 789)
    random_y_offset = random.randint(56, 74)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #選單-按X
    random_x_offset = random.randint(770, 789)
    random_y_offset = random.randint(38, 56)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()


    #信箱
    random_x_offset = random.randint(608, 634)
    random_y_offset = random.randint(35, 56)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #信箱-個人
    random_x_offset = random.randint(420, 460)
    random_y_offset = random.randint(123, 139)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #信箱-個人-接受
    random_x_offset = random.randint(563, 653)
    random_y_offset = random.randint(428, 454)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #信箱-個人-確認
    random_x_offset = random.randint(326, 479)
    random_y_offset = random.randint(360, 388)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #信箱-X
    random_x_offset = random.randint(649, 653)
    random_y_offset = random.randint(73, 75)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()


    #選單
    random_x_offset = random.randint(770, 789)
    random_y_offset = random.randint(38, 56)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()


    #快速內容
    random_x_offset = random.randint(660, 711)
    random_y_offset = random.randint(195, 228)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    # time.sleep(random.randint(3, 5))



    #菁英地成
    random_x_offset = random.randint(32, 132)
    random_y_offset = random.randint(177, 285)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #菁英地成-快速移動
    random_x_offset = random.randint(680, 760)
    random_y_offset = random.randint(450, 460)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #菁英地成-確定
    random_x_offset = random.randint(440, 540)
    random_y_offset = random.randint(370, 380)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    print("菁英地成")
    while(1):
        re_OK = get_text_from_game_region(window_pos[0], window_pos[1],255,512,608-512,283-255)
        if "再次挑戰" in re_OK:

            #菁英地成-再次挑戰
            random_x_offset = random.randint(512, 608)
            random_y_offset = random.randint(255, 283)
            start_abs_x = window_pos[0] + random_x_offset
            start_abs_y = window_pos[1] + random_y_offset
            pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
            pyautogui.mouseDown()
            pyautogui.click()

        # monitor = {"top": y + 433, "left": x + 353, "width": 98, "height": 24}
        re_OK = get_text_from_game_region(window_pos[0], window_pos[1],410,360,90,30)
        if "移動至選單" in re_OK:

            #菁英地成-移動至選單
            random_x_offset = random.randint(360, 360+90)
            random_y_offset = random.randint(410, 410+30)
            start_abs_x = window_pos[0] + random_x_offset
            start_abs_y = window_pos[1] + random_y_offset
            pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
            pyautogui.mouseDown()
            pyautogui.click()

            break
    time.sleep(random.randint(3, 5))
    #菁英地城-返回
    random_x_offset = random.randint(18, 40)
    random_y_offset = random.randint(60, 75)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    # 213 268 
    # 264 282
    #每日地城
    random_x_offset = random.randint(165, 270)
    random_y_offset = random.randint(146, 289)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    # time.sleep(random.randint(3, 5))
    #每日地城-進入
    random_x_offset = random.randint(680, 782)
    random_y_offset = random.randint(439, 461)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    # time.sleep(random.randint(3, 5))
    #每日地城-確認
    random_x_offset = random.randint(425, 565)
    random_y_offset = random.randint(357, 369)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()

    #每日地城2-確認
    random_x_offset = random.randint(449, 528)
    random_y_offset = random.randint(437, 461)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()



    print("每日地城")
    #每日地城-滑鼠移動
    random_x_offset = random.randint(743, 750)
    random_y_offset = random.randint(47, 49)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    start_time = time.time()
    while(1):
        # monitor = {"top": y + 433, "left": x + 353, "width": 98, "height": 24}
        re_OK = get_text_from_game_region(window_pos[0], window_pos[1],398,364,452-364,423-398)
        if re_OK=="移動至選單":

            #每日地城-移動到選單
            random_x_offset = random.randint(354, 454)
            random_y_offset = random.randint(392, 414)
            start_abs_x = window_pos[0] + random_x_offset
            start_abs_y = window_pos[1] + random_y_offset
            pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
            pyautogui.mouseDown()
            pyautogui.click()
            time.sleep(random.randint(3, 5))

            break
        re_OK = get_text_from_game_region(window_pos[0], window_pos[1],270,370,455-370,290-270)
        if re_OK=="移動至選單":
            print("每日地城-失敗")
            #每日地城-移動到選單
            random_x_offset = random.randint(354, 454)
            random_y_offset = random.randint(392, 414)
            start_abs_x = window_pos[0] + random_x_offset
            start_abs_y = window_pos[1] + random_y_offset
            pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
            pyautogui.mouseDown()
            pyautogui.click()
            time.sleep(random.randint(3, 5))

            break
        # 條件2：超過 80 秒自動中止
        if time.time() - start_time > 200:
            print("超過80秒，自動跳出迴圈")
            break



    # time.sleep(random.randint(1, 3))
    #每日地城-X
    random_x_offset = random.randint(776, 789)
    random_y_offset = random.randint(58, 70)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    

    # #包包
    # random_x_offset = random.randint(743, 750)
    # random_y_offset = random.randint(47, 49)
    # start_abs_x = window_pos[0] + random_x_offset
    # start_abs_y = window_pos[1] + random_y_offset
    # pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    # pyautogui.mouseDown()
    # pyautogui.click()
    # #搜尋
    # random_x_offset = random.randint(772, 779)
    # random_y_offset = random.randint(116, 125)
    # start_abs_x = window_pos[0] + random_x_offset
    # start_abs_y = window_pos[1] + random_y_offset
    # pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    # pyautogui.mouseDown()
    # pyautogui.click()
    # time.sleep(random.uniform(0.5, 1.2))
    # #點打字區域
    # random_x_offset = random.randint(490, 545)
    # random_y_offset = random.randint(156, 160)
    # start_abs_x = window_pos[0] + random_x_offset
    # start_abs_y = window_pos[1] + random_y_offset
    # pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    # pyautogui.mouseDown()
    # pyautogui.click()
    # # 等待畫面反應
    # time.sleep(random.uniform(0.5, 1.2))
    # # === 輸入 "GP" ===
    # pyautogui.write('GP', interval=0.1)  # 模擬輸入，每個字母間隔0.1秒
    # #搜尋
    # random_x_offset = random.randint(772, 776)
    # random_y_offset = random.randint(156, 162)
    # start_abs_x = window_pos[0] + random_x_offset
    # start_abs_y = window_pos[1] + random_y_offset
    # pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 2))
    # pyautogui.mouseDown()
    # pyautogui.click()
    # # 等待畫面反應
    # time.sleep(random.uniform(0.5, 1.2))
    # while(1):
    #     # monitor = {"top": y + 433, "left": x + 353, "width": 98, "height": 24}
    #     re_OK = get_text_from_game_region(window_pos[0], window_pos[1],398,487,558-98,418-398)
    #     print(re_OK)
    #     count_0=0
    #     if "GP交換" in re_OK:
    #         #點搜尋
    #         random_x_offset = random.randint(777, 784)
    #         random_y_offset = random.randint(401, 414)
    #         start_abs_x = window_pos[0] + random_x_offset
    #         start_abs_y = window_pos[1] + random_y_offset
    #         pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    #         pyautogui.mouseDown()
    #         pyautogui.click()
    #         #點
    #         random_x_offset = random.randint(496, 510)
    #         random_y_offset = random.randint(212, 220)
    #         start_abs_x = window_pos[0] + random_x_offset
    #         start_abs_y = window_pos[1] + random_y_offset
    #         pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    #         pyautogui.mouseDown()
    #         pyautogui.click()
    #         #點使用
    #         random_x_offset = random.randint(630, 743)
    #         random_y_offset = random.randint(442, 449)
    #         start_abs_x = window_pos[0] + random_x_offset
    #         start_abs_y = window_pos[1] + random_y_offset
    #         pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    #         pyautogui.mouseDown()
    #         pyautogui.click()
    #         #點返回
    #         random_x_offset = random.randint(772, 780)
    #         random_y_offset = random.randint(155, 160)
    #         start_abs_x = window_pos[0] + random_x_offset
    #         start_abs_y = window_pos[1] + random_y_offset
    #         pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    #         pyautogui.mouseDown()
    #         pyautogui.click()

    #         #搜尋
    #         random_x_offset = random.randint(772, 779)
    #         random_y_offset = random.randint(116, 125)
    #         start_abs_x = window_pos[0] + random_x_offset
    #         start_abs_y = window_pos[1] + random_y_offset
    #         pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    #         pyautogui.mouseDown()
    #         pyautogui.click()
    #         # 等待畫面反應
    #         time.sleep(random.uniform(0.5, 1.2))
    #         #點打字區域
    #         random_x_offset = random.randint(490, 545)
    #         random_y_offset = random.randint(156, 160)
    #         start_abs_x = window_pos[0] + random_x_offset
    #         start_abs_y = window_pos[1] + random_y_offset
    #         pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    #         pyautogui.mouseDown()
    #         pyautogui.click()
    #         # === 輸入 "GP" ===
    #         pyautogui.write('GP', interval=0.1)  # 模擬輸入，每個字母間隔0.1秒
    #         #搜尋
    #         random_x_offset = random.randint(772, 776)
    #         random_y_offset = random.randint(156, 162)
    #         start_abs_x = window_pos[0] + random_x_offset
    #         start_abs_y = window_pos[1] + random_y_offset
    #         pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 2))
    #         pyautogui.mouseDown()
    #         pyautogui.click()
    #         # 等待畫面反應
    #         time.sleep(random.uniform(2, 5))
    #         count_0+=1
    #     if count_0>=10:
    #         break
    #     if not "GP交換" in re_OK:
    #         #點X
    #         random_x_offset = random.randint(779, 790)
    #         random_y_offset = random.randint(70, 72)
    #         start_abs_x = window_pos[0] + random_x_offset
    #         start_abs_y = window_pos[1] + random_y_offset
    #         pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 2))
    #         pyautogui.mouseDown()
    #         pyautogui.click()
    #         # 等待畫面反應
    #         time.sleep(random.uniform(0.5, 1.2))
    #         break



    #選單
    random_x_offset = random.randint(-5, 5)
    random_y_offset = random.randint(-5, 5)
    start_abs_x = window_pos[0] + random_x_offset+ 783
    start_abs_y = window_pos[1] + random_y_offset+ 52
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #課題
    random_x_offset = random.randint(526, 560)
    random_y_offset = random.randint(211, 228)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #課題-全部領取
    random_x_offset = random.randint(722, 730)
    random_y_offset = random.randint(450, 469)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #課題-確認
    # 升等後可能跳出廣告：最多檢查 5 秒。
    # 找到後會點擊指定位置並按 ESC，接著繼續原本的課題流程。
    ad_check_deadline = time.time() + 5
    while time.time() < ad_check_deadline:
        rect = get_window_rect(WINDOW_TITLE)
        if not rect:
            print(f"找不到視窗 '{WINDOW_TITLE}'，略過廣告檢查")
            break

        win_x, win_y, win_w, win_h = rect
        search_region = (win_x, win_y, win_w, win_h)

        if process_ad_group(win_x, win_y, search_region, AD_CONFIG_2):
            refreshed_window_pos = get_window_position(WINDOW_TITLE)
            if refreshed_window_pos:
                window_pos = refreshed_window_pos
            time.sleep(1)
            pyautogui.press('space')
            break

        time.sleep(0.5)
    #課題-全部領取
    # Confirm only after advertisement detection and handling.
    random_x_offset = random.randint(348, 455)
    random_y_offset = random.randint(350, 379)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    random_x_offset = random.randint(722, 730)
    random_y_offset = random.randint(450, 469)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #課題-確認2
    # 升等後可能跳出廣告：最多檢查 5 秒。
    # 找到後會點擊指定位置並按 ESC，接著繼續原本的課題流程。
    ad_check_deadline = time.time() + 5
    while time.time() < ad_check_deadline:
        rect = get_window_rect(WINDOW_TITLE)
        if not rect:
            print(f"找不到視窗 '{WINDOW_TITLE}'，略過廣告檢查")
            break

        win_x, win_y, win_w, win_h = rect
        search_region = (win_x, win_y, win_w, win_h)

        if process_ad_group(win_x, win_y, search_region, AD_CONFIG_2):
            refreshed_window_pos = get_window_position(WINDOW_TITLE)
            if refreshed_window_pos:
                window_pos = refreshed_window_pos
            time.sleep(1)
            pyautogui.press('space')
            break

        time.sleep(0.5)
    #課題-X
    # Confirm the second action only after advertisement detection and handling.
    random_x_offset = random.randint(348, 455)
    random_y_offset = random.randint(319, 343)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    random_x_offset = random.randint(780, 786)
    random_y_offset = random.randint(61, 73)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #腳色變更清單
    random_x_offset = random.randint(632, 633)
    random_y_offset = random.randint(445, 446)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
def round0():
    window_pos = get_window_position(WINDOW_TITLE)
    if not window_pos:
        print(f"找不到視窗 '{WINDOW_TITLE}'，略過 round0")
        return False

    now = datetime.datetime.now()

    # if 1<0:
    if now.hour < 20 or (now.hour == 20 and now.minute < 50):
        # ✅ 時間區間判斷：00:00 ~ 20:49 才執行
        #選單
        random_x_offset = random.randint(770, 789)
        random_y_offset = random.randint(38, 56)
        start_abs_x = window_pos[0] + random_x_offset
        start_abs_y = window_pos[1] + random_y_offset
        pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
        pyautogui.mouseDown()
        pyautogui.click()
        # time.sleep(random.randint(3, 5))

        #公會
        random_x_offset = random.randint(657, 712)
        random_y_offset = random.randint(307, 341)
        start_abs_x = window_pos[0] + random_x_offset
        start_abs_y = window_pos[1] + random_y_offset
        pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
        pyautogui.mouseDown()
        pyautogui.click()

        #榮譽站
        time.sleep(random.randint(2, 3))
        random_x_offset = random.randint(694, 741)
        random_y_offset = random.randint(305, 337)
        start_abs_x = window_pos[0] + random_x_offset
        start_abs_y = window_pos[1] + random_y_offset
        pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
        pyautogui.mouseDown()
        pyautogui.click()
        #榮譽站-確認(上一場確認輸贏)
        random_x_offset = random.randint(420, 425)
        random_y_offset = random.randint(434, 436)
        start_abs_x = window_pos[0] + random_x_offset
        start_abs_y = window_pos[1] + random_y_offset
        pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
        pyautogui.mouseDown()
        pyautogui.click()
        #榮譽站-確認
        random_x_offset = random.randint(420, 425)
        random_y_offset = random.randint(434, 436)
        start_abs_x = window_pos[0] + random_x_offset
        start_abs_y = window_pos[1] + random_y_offset
        pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
        pyautogui.mouseDown()
        pyautogui.click()
        #榮譽站-入場/開打
        random_x_offset = random.randint(330, 343)
        random_y_offset = random.randint(458, 461)
        start_abs_x = window_pos[0] + random_x_offset
        start_abs_y = window_pos[1] + random_y_offset
        pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
        pyautogui.mouseDown()
        pyautogui.click()
        random_x_offset = random.randint(330, 343)
        random_y_offset = random.randint(458, 461)
        start_abs_x = window_pos[0] + random_x_offset
        start_abs_y = window_pos[1] + random_y_offset
        pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
        pyautogui.mouseDown()
        pyautogui.click()
        time.sleep(random.randint(90, 100))

    #選單
    random_x_offset = random.randint(770, 789)
    random_y_offset = random.randint(38, 56)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    # time.sleep(random.randint(3, 5))
    #公會
    random_x_offset = random.randint(657, 712)
    random_y_offset = random.randint(307, 341)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()

    #領獎勵
    random_x_offset = random.randint(700, 730)
    random_y_offset = random.randint(108, 119)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #公會-按X
    random_x_offset = random.randint(773, 789)
    random_y_offset = random.randint(56, 74)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #選單-按X
    random_x_offset = random.randint(770, 789)
    random_y_offset = random.randint(38, 56)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()


    #信箱
    random_x_offset = random.randint(608, 634)
    random_y_offset = random.randint(35, 56)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #信箱-個人
    random_x_offset = random.randint(420, 460)
    random_y_offset = random.randint(123, 139)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #信箱-個人-接受
    random_x_offset = random.randint(563, 653)
    random_y_offset = random.randint(428, 454)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #信箱-個人-確認
    random_x_offset = random.randint(326, 479)
    random_y_offset = random.randint(360, 388)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #信箱-X
    random_x_offset = random.randint(649, 653)
    random_y_offset = random.randint(73, 75)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()

    # #包包
    # random_x_offset = random.randint(743, 750)
    # random_y_offset = random.randint(47, 49)
    # start_abs_x = window_pos[0] + random_x_offset
    # start_abs_y = window_pos[1] + random_y_offset
    # pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    # pyautogui.mouseDown()
    # pyautogui.click()
    # #搜尋
    # random_x_offset = random.randint(772, 779)
    # random_y_offset = random.randint(116, 125)
    # start_abs_x = window_pos[0] + random_x_offset
    # start_abs_y = window_pos[1] + random_y_offset
    # pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    # pyautogui.mouseDown()
    # pyautogui.click()
    # time.sleep(random.uniform(0.5, 1.2))
    # #點打字區域
    # random_x_offset = random.randint(490, 545)
    # random_y_offset = random.randint(156, 160)
    # start_abs_x = window_pos[0] + random_x_offset
    # start_abs_y = window_pos[1] + random_y_offset
    # pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    # pyautogui.mouseDown()
    # pyautogui.click()
    # # 等待畫面反應
    # time.sleep(random.uniform(0.5, 1.2))
    # # === 輸入 "GP" ===
    # pyautogui.write('GP', interval=0.1)  # 模擬輸入，每個字母間隔0.1秒
    # #搜尋
    # random_x_offset = random.randint(772, 776)
    # random_y_offset = random.randint(156, 162)
    # start_abs_x = window_pos[0] + random_x_offset
    # start_abs_y = window_pos[1] + random_y_offset
    # pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 2))
    # pyautogui.mouseDown()
    # pyautogui.click()
    # # 等待畫面反應
    # time.sleep(random.uniform(0.5, 1.2))
    # while(1):
    #     # monitor = {"top": y + 433, "left": x + 353, "width": 98, "height": 24}
    #     re_OK = get_text_from_game_region(window_pos[0], window_pos[1],398,487,558-98,418-398)
    #     print(re_OK)
    #     if "GP交換" in re_OK:
    #         #點搜尋
    #         random_x_offset = random.randint(777, 784)
    #         random_y_offset = random.randint(401, 414)
    #         start_abs_x = window_pos[0] + random_x_offset
    #         start_abs_y = window_pos[1] + random_y_offset
    #         pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    #         pyautogui.mouseDown()
    #         pyautogui.click()
    #         #點
    #         random_x_offset = random.randint(496, 510)
    #         random_y_offset = random.randint(212, 220)
    #         start_abs_x = window_pos[0] + random_x_offset
    #         start_abs_y = window_pos[1] + random_y_offset
    #         pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    #         pyautogui.mouseDown()
    #         pyautogui.click()
    #         #點使用
    #         random_x_offset = random.randint(630, 743)
    #         random_y_offset = random.randint(442, 449)
    #         start_abs_x = window_pos[0] + random_x_offset
    #         start_abs_y = window_pos[1] + random_y_offset
    #         pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    #         pyautogui.mouseDown()
    #         pyautogui.click()
    #         #點返回
    #         random_x_offset = random.randint(772, 780)
    #         random_y_offset = random.randint(155, 160)
    #         start_abs_x = window_pos[0] + random_x_offset
    #         start_abs_y = window_pos[1] + random_y_offset
    #         pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    #         pyautogui.mouseDown()
    #         pyautogui.click()

    #         #搜尋
    #         random_x_offset = random.randint(772, 779)
    #         random_y_offset = random.randint(116, 125)
    #         start_abs_x = window_pos[0] + random_x_offset
    #         start_abs_y = window_pos[1] + random_y_offset
    #         pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    #         pyautogui.mouseDown()
    #         pyautogui.click()
    #         # 等待畫面反應
    #         time.sleep(random.uniform(0.5, 1.2))
    #         #點打字區域
    #         random_x_offset = random.randint(490, 545)
    #         random_y_offset = random.randint(156, 160)
    #         start_abs_x = window_pos[0] + random_x_offset
    #         start_abs_y = window_pos[1] + random_y_offset
    #         pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    #         pyautogui.mouseDown()
    #         pyautogui.click()
    #         # === 輸入 "GP" ===
    #         pyautogui.write('GP', interval=0.1)  # 模擬輸入，每個字母間隔0.1秒
    #         #搜尋
    #         random_x_offset = random.randint(772, 776)
    #         random_y_offset = random.randint(156, 162)
    #         start_abs_x = window_pos[0] + random_x_offset
    #         start_abs_y = window_pos[1] + random_y_offset
    #         pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 2))
    #         pyautogui.mouseDown()
    #         pyautogui.click()
    #         # 等待畫面反應
    #         time.sleep(random.uniform(2, 5))
    #     if not "GP交換" in re_OK:
    #         #點X
    #         random_x_offset = random.randint(779, 790)
    #         random_y_offset = random.randint(70, 72)
    #         start_abs_x = window_pos[0] + random_x_offset
    #         start_abs_y = window_pos[1] + random_y_offset
    #         pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 2))
    #         pyautogui.mouseDown()
    #         pyautogui.click()
    #         # 等待畫面反應
    #         time.sleep(random.uniform(0.5, 1.2))
    #         break




    #選單
    random_x_offset = random.randint(770, 789)
    random_y_offset = random.randint(38, 56)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()


    #快速內容
    random_x_offset = random.randint(660, 711)
    random_y_offset = random.randint(195, 228)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    # time.sleep(random.randint(3, 5))



    #菁英地成
    random_x_offset = random.randint(32, 132)
    random_y_offset = random.randint(177, 285)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #菁英地成-快速移動
    random_x_offset = random.randint(680, 760)
    random_y_offset = random.randint(450, 460)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #菁英地成-確定
    random_x_offset = random.randint(440, 540)
    random_y_offset = random.randint(370, 380)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    print("菁英地成")
    while(1):
        # re_OK = get_text_from_game_region(window_pos[0], window_pos[1],255,512,608-512,283-255)
        # if "再次挑戰" in re_OK:

        #     #菁英地成-再次挑戰
        #     random_x_offset = random.randint(512, 608)
        #     random_y_offset = random.randint(255, 283)
        #     start_abs_x = window_pos[0] + random_x_offset
        #     start_abs_y = window_pos[1] + random_y_offset
        #     pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
        #     pyautogui.mouseDown()
        #     pyautogui.click()

        # monitor = {"top": y + 433, "left": x + 353, "width": 98, "height": 24}
        re_OK = get_text_from_game_region(window_pos[0], window_pos[1],410,360,90,30)
        if "移動至選單" in re_OK:

            #菁英地成-移動至選單
            random_x_offset = random.randint(360, 360+90)
            random_y_offset = random.randint(410, 410+30)
            start_abs_x = window_pos[0] + random_x_offset
            start_abs_y = window_pos[1] + random_y_offset
            pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
            pyautogui.mouseDown()
            pyautogui.click()

            break
    time.sleep(random.randint(3, 5))

    # #菁英地成2
    # random_x_offset = random.randint(595, 628)
    # random_y_offset = random.randint(121, 157)
    # start_abs_x = window_pos[0] + random_x_offset
    # start_abs_y = window_pos[1] + random_y_offset
    # pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    # pyautogui.mouseDown()
    # pyautogui.click()
    # #菁英地成2-快速移動
    # random_x_offset = random.randint(630, 760)
    # random_y_offset = random.randint(450, 460)
    # start_abs_x = window_pos[0] + random_x_offset
    # start_abs_y = window_pos[1] + random_y_offset
    # pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    # pyautogui.mouseDown()
    # pyautogui.click()
    # #菁英地成2-確定
    # random_x_offset = random.randint(440, 540)
    # random_y_offset = random.randint(370, 380)
    # start_abs_x = window_pos[0] + random_x_offset
    # start_abs_y = window_pos[1] + random_y_offset
    # pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    # pyautogui.mouseDown()
    # pyautogui.click()
    # print("菁英地成2")
    # while(1):
    #     re_OK = get_text_from_game_region(window_pos[0], window_pos[1],255,512,608-512,283-255)
    #     if re_OK=="再次挑戰":

    #         #菁英地成-再次挑戰
    #         random_x_offset = random.randint(512, 608)
    #         random_y_offset = random.randint(255, 283)
    #         start_abs_x = window_pos[0] + random_x_offset
    #         start_abs_y = window_pos[1] + random_y_offset
    #         pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    #         pyautogui.mouseDown()
    #         pyautogui.click()

    #     # monitor = {"top": y + 433, "left": x + 353, "width": 98, "height": 24}
    #     re_OK = get_text_from_game_region(window_pos[0], window_pos[1],433,353,98,24)
    #     if re_OK=="移動至選單":

    #         #菁英地成-移動至選單
    #         random_x_offset = random.randint(353, 353+98)
    #         random_y_offset = random.randint(433, 433+24)
    #         start_abs_x = window_pos[0] + random_x_offset
    #         start_abs_y = window_pos[1] + random_y_offset
    #         pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    #         pyautogui.mouseDown()
    #         pyautogui.click()

    #         break
    # time.sleep(random.randint(3, 5))
    #菁英地城-返回
    random_x_offset = random.randint(18, 40)
    random_y_offset = random.randint(60, 75)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    # 213 268 
    # 264 282
    #每日地城
    random_x_offset = random.randint(165, 270)
    random_y_offset = random.randint(146, 289)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()

    # time.sleep(random.randint(3, 5))
    #每日地城-進入
    random_x_offset = random.randint(660, 782)
    random_y_offset = random.randint(439, 461)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    # time.sleep(random.randint(3, 5))
    #每日地城-確認
    random_x_offset = random.randint(425, 565)
    random_y_offset = random.randint(357, 369)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    print("每日地城")
    #每日地城-滑鼠移動
    random_x_offset = random.randint(743, 750)
    random_y_offset = random.randint(47, 49)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    start_time = time.time()
    while(1):
        # monitor = {"top": y + 433, "left": x + 353, "width": 98, "height": 24}
        re_OK = get_text_from_game_region(window_pos[0], window_pos[1],398,364,452-364,423-398)
        if re_OK=="移動至選單":

            #每日地城-移動到選單
            random_x_offset = random.randint(354, 454)
            random_y_offset = random.randint(392, 414)
            start_abs_x = window_pos[0] + random_x_offset
            start_abs_y = window_pos[1] + random_y_offset
            pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
            pyautogui.mouseDown()
            pyautogui.click()
            time.sleep(random.randint(3, 5))

            break
        re_OK = get_text_from_game_region(window_pos[0], window_pos[1],270,370,455-370,290-270)
        if re_OK=="移動至選單":
            print("每日地城-失敗")
            #每日地城-移動到選單
            random_x_offset = random.randint(354, 454)
            random_y_offset = random.randint(392, 414)
            start_abs_x = window_pos[0] + random_x_offset
            start_abs_y = window_pos[1] + random_y_offset
            pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
            pyautogui.mouseDown()
            pyautogui.click()
            time.sleep(random.randint(3, 5))

            break
        # 條件2：超過 80 秒自動中止
        if time.time() - start_time > 200:
            print("超過80秒，自動跳出迴圈")
            break



    # time.sleep(random.randint(1, 3))
    #每日地城2
    random_x_offset = random.randint(43, 104)
    random_y_offset = random.randint(290, 311)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()

    #每日地城2-進入
    random_x_offset = random.randint(660, 782)
    random_y_offset = random.randint(439, 461)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    # time.sleep(random.randint(3, 5))
    #每日地城2-確認
    random_x_offset = random.randint(449, 528)
    random_y_offset = random.randint(437, 461)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    print("每日地城2")
    #每日地城2-滑鼠移動
    random_x_offset = random.randint(743, 750)
    random_y_offset = random.randint(47, 49)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    start_time = time.time()
    while(1):
        # monitor = {"top": y + 433, "left": x + 353, "width": 98, "height": 24}
        re_OK = get_text_from_game_region(window_pos[0], window_pos[1],397,362,456-362,422-397)
        if re_OK=="移動至選單":

            #每日地城2-移動到選單
            random_x_offset = random.randint(362, 456)
            random_y_offset = random.randint(397, 422)
            start_abs_x = window_pos[0] + random_x_offset
            start_abs_y = window_pos[1] + random_y_offset
            pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
            pyautogui.mouseDown()
            pyautogui.click()
            time.sleep(random.randint(3, 5))

            break
        re_OK = get_text_from_game_region(window_pos[0], window_pos[1],397,362,456-362,422-397)
        if re_OK=="移動至選單":
            print("每日地城-失敗")
            #每日地城-移動到選單
            random_x_offset = random.randint(362, 456)
            random_y_offset = random.randint(397, 422)
            start_abs_x = window_pos[0] + random_x_offset
            start_abs_y = window_pos[1] + random_y_offset
            pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
            pyautogui.mouseDown()
            pyautogui.click()
            time.sleep(random.randint(3, 5))

            break
        # 條件2：超過 80 秒自動中止
        if time.time() - start_time > 200:
            print("超過80秒，自動跳出迴圈")
            break
    #菁英地城-返回
    random_x_offset = random.randint(18, 40)
    random_y_offset = random.randint(60, 75)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    
    #武林到場
    random_x_offset = random.randint(598, 670)
    random_y_offset = random.randint(365, 438)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #武林到場
    random_x_offset = random.randint(650, 750)
    random_y_offset = random.randint(444, 466)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #武林到場
    random_x_offset = random.randint(445, 540)
    random_y_offset = random.randint(438, 460)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    print("武林到場")
    while(1):
        re_OK = get_text_from_game_region(window_pos[0], window_pos[1],429,355,455-355,455-429)
        if re_OK=="移動至選單":

            #武林到場-再次挑戰
            random_x_offset = random.randint(355, 455)
            random_y_offset = random.randint(429, 455)
            start_abs_x = window_pos[0] + random_x_offset
            start_abs_y = window_pos[1] + random_y_offset
            pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
            pyautogui.mouseDown()
            pyautogui.click()
            time.sleep(random.randint(3, 5))
            break
    #武林到場-返回
    random_x_offset = random.randint(320, 356)
    random_y_offset = random.randint(431, 454)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    time.sleep(random.randint(3, 5))
    #武林到場-返回
    random_x_offset = random.randint(18, 40)
    random_y_offset = random.randint(60, 75)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    time.sleep(random.randint(3, 5))

    #次元
    random_x_offset = random.randint(603, 670)
    random_y_offset = random.randint(182, 277)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    time.sleep(random.randint(3, 5))
    #次元
    random_x_offset = random.randint(700, 750)
    random_y_offset = random.randint(450, 460)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #次元
    random_x_offset = random.randint(480, 500)
    random_y_offset = random.randint(380, 390)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    print("次元")
    while(1):
        re_OK = get_text_from_game_region(window_pos[0], window_pos[1],400,360,455-360,430-400)
        if re_OK=="移動至選單":

            #次元-移動至選單
            random_x_offset = random.randint(390, 400)
            random_y_offset = random.randint(405, 420)
            start_abs_x = window_pos[0] + random_x_offset
            start_abs_y = window_pos[1] + random_y_offset
            pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
            pyautogui.mouseDown()
            pyautogui.click()
            time.sleep(random.randint(3, 5))
            break


    #次元X
    random_x_offset = random.randint(776, 789)
    random_y_offset = random.randint(58, 70)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    time.sleep(random.randint(1, 2))
    

    



    #選單
    random_x_offset = random.randint(-5, 5)
    random_y_offset = random.randint(-5, 5)
    start_abs_x = window_pos[0] + random_x_offset+ 783
    start_abs_y = window_pos[1] + random_y_offset+ 52
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #課題
    random_x_offset = random.randint(526, 560)
    random_y_offset = random.randint(211, 228)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #課題-全部領取
    random_x_offset = random.randint(722, 730)
    random_y_offset = random.randint(450, 469)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #課題-確認
    ad_check_deadline = time.time() + 5
    while time.time() < ad_check_deadline:
        rect = get_window_rect(WINDOW_TITLE)
        if not rect:
            print(f"找不到視窗 '{WINDOW_TITLE}'，略過廣告檢查")
            break

        win_x, win_y, win_w, win_h = rect
        search_region = (win_x, win_y, win_w, win_h)

        if process_ad_group(win_x, win_y, search_region, AD_CONFIG_2):
            refreshed_window_pos = get_window_position(WINDOW_TITLE)
            if refreshed_window_pos:
                window_pos = refreshed_window_pos
            time.sleep(1)
            pyautogui.press('space')
            break

        time.sleep(0.5)
    #課題-全部領取
    # Confirm only after advertisement detection and handling.
    random_x_offset = random.randint(348, 455)
    random_y_offset = random.randint(350, 379)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    random_x_offset = random.randint(722, 730)
    random_y_offset = random.randint(450, 469)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #課題-確認2
    ad_check_deadline = time.time() + 5
    while time.time() < ad_check_deadline:
        rect = get_window_rect(WINDOW_TITLE)
        if not rect:
            print(f"找不到視窗 '{WINDOW_TITLE}'，略過廣告檢查")
            break

        win_x, win_y, win_w, win_h = rect
        search_region = (win_x, win_y, win_w, win_h)

        if process_ad_group(win_x, win_y, search_region, AD_CONFIG_2):
            refreshed_window_pos = get_window_position(WINDOW_TITLE)
            if refreshed_window_pos:
                window_pos = refreshed_window_pos
            time.sleep(1)
            pyautogui.press('space')
            break

        time.sleep(0.5)
    #課題-X
    # Confirm the second action only after advertisement detection and handling.
    random_x_offset = random.randint(348, 455)
    random_y_offset = random.randint(319, 343)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    random_x_offset = random.randint(780, 786)
    random_y_offset = random.randint(61, 73)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #腳色變更清單
    random_x_offset = random.randint(632, 633)
    random_y_offset = random.randint(445, 446)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()


# 使用示例
# display_and_click_relative_position("MapleStoryM")
# window_pos = get_window_position("MapleStoryM")
# round1()

window_pos = get_window_position("MapleStoryM")
# if window_pos:
#     print(f"窗口 '{window_title}' 位置: ({window_pos[0]}, {window_pos[1]}), 大小: ({window_pos[2]}x{window_pos[3]})")


random_x_offset = random.randint(-5, 5)
random_y_offset = random.randint(-5, 5)
start_abs_x = window_pos[0] + random_x_offset+ 30
start_abs_y = window_pos[1] + random_y_offset+ 15
pyautogui.click(start_abs_x, start_abs_y)
time.sleep(random.randint(1, 5))

# round0()

while(1):
    window_pos = get_window_position("MapleStoryM")

    time.sleep(random.randint(3, 5))
    # for i in range(int(count/2)):
    #     # print('滑',i+1,int(count/2))
    #     start_abs_x = window_pos[0] + 530
    #     start_abs_y = window_pos[1] + 187
    #     end_abs_x = window_pos[0] + 525
    #     end_abs_y = window_pos[1] + 204

    #     # 模擬按下
    #     # pyautogui.mouseDown()
    #     pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    #     pyautogui.mouseDown()
    #     # pyautogui.mouseDown(start_abs_x, start_abs_y)
    #     # 模擬拖動
    #     pyautogui.moveTo(end_abs_x, end_abs_y, duration=1)  # 可以調整 duration 來控制移動速度
    #     # 釋放滑鼠
    #     pyautogui.mouseUp(end_abs_x, end_abs_y)
    count+=1
    #右邊
    random_x_offset = random.randint(505, 559)
    random_y_offset = random.randint(187, 188)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()


    time.sleep(random.randint(3, 5))
    random_x_offset = random.randint(507, 626)
    random_y_offset = random.randint(435, 456)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    time.sleep(random.randint(10, 13))
    round1()

    print(count)
    if count>=endcount:
        break

    time.sleep(random.randint(3, 5))
    # for i in range(int(count/2)):
    #     print('滑',i+1,int(count/2))
    #     start_abs_x = window_pos[0] + 531
    #     start_abs_y = window_pos[1] + 317
    #     end_abs_x = window_pos[0] + 525
    #     end_abs_y = window_pos[1] + 204

    #     # 模擬按下
    #     # pyautogui.mouseDown()
    #     pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    #     pyautogui.mouseDown()
    #     # pyautogui.mouseDown(start_abs_x, start_abs_y)
    #     # 模擬拖動
    #     pyautogui.moveTo(end_abs_x, end_abs_y, duration=1)  # 可以調整 duration 來控制移動速度
    #     # 釋放滑鼠
    #     pyautogui.mouseUp(end_abs_x, end_abs_y)
    # count+=1
    #左邊
    random_x_offset = random.randint(238, 360)
    random_y_offset = random.randint(264, 273)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()

    time.sleep(random.randint(3, 5))
    random_x_offset = random.randint(507, 626)
    random_y_offset = random.randint(435, 456)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    time.sleep(random.randint(10, 13))
    round1()

    



    # 模擬點擊
    # pyautogui.click(mouse_x, mouse_y)
    print(count)
    if count>=endcount:
        break






# round1()



# 示例: 點擊標題為 "My App" 的窗口內的相對位置
# click_in_window("MapleStoryM", 100, 200, 0.5)
