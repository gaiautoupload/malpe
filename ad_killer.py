import pyautogui
import pygetwindow as gw
import time
import os
import traceback
from PIL import Image, ImageGrab

# 防止滑鼠移到角落時觸發錯誤
pyautogui.FAILSAFE = False

# ================= 設定區 =================
WINDOW_TITLE = "MapleStoryM"

# 支援的圖片格式
VALID_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp')

# --- 廣告設定 1 (原本的) ---
AD_CONFIG_1 = {
    "folder": "ad_image",
    "offset_x": 223,
    "offset_y": 372
}

# --- 廣告設定 2 (新增的) ---
AD_CONFIG_2 = {
    "folder": "ad_image2",
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
            with Image.open(img_path) as image_file:
                needle_image = image_file.convert("RGB")
            location = pyautogui.locate(
                needle_image,
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

def ad_monitor_loop():
    print(f"=== 雙重廣告攔截器已啟動 ===")
    print(f"監控目標: {WINDOW_TITLE}")
    print(f"設定 1: 資料夾 '{AD_CONFIG_1['folder']}' -> 點擊 ({AD_CONFIG_1['offset_x']}, {AD_CONFIG_1['offset_y']})")
    print(f"設定 2: 資料夾 '{AD_CONFIG_2['folder']}' -> 點擊 ({AD_CONFIG_2['offset_x']}, {AD_CONFIG_2['offset_y']})")
    print("--------------------------------")

    while True:
        try:
            # 1. 抓視窗位置
            rect = get_window_rect(WINDOW_TITLE)
            if not rect:
                print(f"找不到視窗 '{WINDOW_TITLE}'，等待 5 秒...", end='\r')
                time.sleep(5)
                continue

            win_x, win_y, win_w, win_h = rect
            search_region = (win_x, win_y, win_w, win_h)
            
            # 2. 依序檢查兩組廣告設定
            # 如果第一組抓到了，就不會抓第二組 (因為 process_ad_group 回傳 True 就會跑 continue)
            
            # --- 檢查第一組 ---
            if process_ad_group(win_x, win_y, search_region, AD_CONFIG_1):
                continue 
            
            # --- 檢查第二組 ---
            if process_ad_group(win_x, win_y, search_region, AD_CONFIG_2):
                continue

            # 都沒抓到，稍微休息
            time.sleep(1)

        except KeyboardInterrupt:
            print("\n使用者手動停止程式。")
            break
        except Exception as e:
            print(f"\n[嚴重錯誤] {e}")
            traceback.print_exc()
            time.sleep(3) 

if __name__ == "__main__":
    # 自動建立資料夾檢查
    for folder in [AD_CONFIG_1["folder"], AD_CONFIG_2["folder"]]:
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
                print(f"已自動建立資料夾: {folder}")
            except:
                pass
    
    ad_monitor_loop()
