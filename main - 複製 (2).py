import pygetwindow as gw
import pyautogui
pyautogui.FAILSAFE = False
import datetime
import time
import random
import mss
import cv2
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
endcount = 26
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
    time.sleep(random.randint(3, 5))
    
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
    random_x_offset = random.randint(629, 782)
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
    

    #包包
    random_x_offset = random.randint(743, 750)
    random_y_offset = random.randint(47, 49)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #搜尋
    random_x_offset = random.randint(772, 779)
    random_y_offset = random.randint(116, 125)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    time.sleep(random.uniform(0.5, 1.2))
    #點打字區域
    random_x_offset = random.randint(490, 545)
    random_y_offset = random.randint(156, 160)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    # 等待畫面反應
    time.sleep(random.uniform(0.5, 1.2))
    # === 輸入 "GP" ===
    pyautogui.write('GP', interval=0.1)  # 模擬輸入，每個字母間隔0.1秒
    #搜尋
    random_x_offset = random.randint(772, 776)
    random_y_offset = random.randint(156, 162)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 2))
    pyautogui.mouseDown()
    pyautogui.click()
    # 等待畫面反應
    time.sleep(random.uniform(0.5, 1.2))
    while(1):
        # monitor = {"top": y + 433, "left": x + 353, "width": 98, "height": 24}
        re_OK = get_text_from_game_region(window_pos[0], window_pos[1],398,487,558-98,418-398)
        print(re_OK)
        count_0=0
        if "GP交換" in re_OK:
            #點搜尋
            random_x_offset = random.randint(777, 784)
            random_y_offset = random.randint(401, 414)
            start_abs_x = window_pos[0] + random_x_offset
            start_abs_y = window_pos[1] + random_y_offset
            pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
            pyautogui.mouseDown()
            pyautogui.click()
            #點
            random_x_offset = random.randint(496, 510)
            random_y_offset = random.randint(212, 220)
            start_abs_x = window_pos[0] + random_x_offset
            start_abs_y = window_pos[1] + random_y_offset
            pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
            pyautogui.mouseDown()
            pyautogui.click()
            #點使用
            random_x_offset = random.randint(630, 743)
            random_y_offset = random.randint(442, 449)
            start_abs_x = window_pos[0] + random_x_offset
            start_abs_y = window_pos[1] + random_y_offset
            pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
            pyautogui.mouseDown()
            pyautogui.click()
            #點返回
            random_x_offset = random.randint(772, 780)
            random_y_offset = random.randint(155, 160)
            start_abs_x = window_pos[0] + random_x_offset
            start_abs_y = window_pos[1] + random_y_offset
            pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
            pyautogui.mouseDown()
            pyautogui.click()

            #搜尋
            random_x_offset = random.randint(772, 779)
            random_y_offset = random.randint(116, 125)
            start_abs_x = window_pos[0] + random_x_offset
            start_abs_y = window_pos[1] + random_y_offset
            pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
            pyautogui.mouseDown()
            pyautogui.click()
            # 等待畫面反應
            time.sleep(random.uniform(0.5, 1.2))
            #點打字區域
            random_x_offset = random.randint(490, 545)
            random_y_offset = random.randint(156, 160)
            start_abs_x = window_pos[0] + random_x_offset
            start_abs_y = window_pos[1] + random_y_offset
            pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
            pyautogui.mouseDown()
            pyautogui.click()
            # === 輸入 "GP" ===
            pyautogui.write('GP', interval=0.1)  # 模擬輸入，每個字母間隔0.1秒
            #搜尋
            random_x_offset = random.randint(772, 776)
            random_y_offset = random.randint(156, 162)
            start_abs_x = window_pos[0] + random_x_offset
            start_abs_y = window_pos[1] + random_y_offset
            pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 2))
            pyautogui.mouseDown()
            pyautogui.click()
            # 等待畫面反應
            time.sleep(random.uniform(2, 5))
            count_0+=1
        if count_0>=10:
            break
        if not "GP交換" in re_OK:
            #點X
            random_x_offset = random.randint(779, 790)
            random_y_offset = random.randint(70, 72)
            start_abs_x = window_pos[0] + random_x_offset
            start_abs_y = window_pos[1] + random_y_offset
            pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 2))
            pyautogui.mouseDown()
            pyautogui.click()
            # 等待畫面反應
            time.sleep(random.uniform(0.5, 1.2))
            break



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
    random_x_offset = random.randint(348, 455)
    random_y_offset = random.randint(350, 379)
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
    #課題-確認2
    random_x_offset = random.randint(348, 455)
    random_y_offset = random.randint(319, 343)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #課題-X
    random_x_offset = random.randint(780, 786)
    random_y_offset = random.randint(61, 73)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #腳色變更清單
    random_x_offset = random.randint(695, 715)
    random_y_offset = random.randint(428, 453)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
def round0():
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

    #包包
    random_x_offset = random.randint(743, 750)
    random_y_offset = random.randint(47, 49)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #搜尋
    random_x_offset = random.randint(772, 779)
    random_y_offset = random.randint(116, 125)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    time.sleep(random.uniform(0.5, 1.2))
    #點打字區域
    random_x_offset = random.randint(490, 545)
    random_y_offset = random.randint(156, 160)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    # 等待畫面反應
    time.sleep(random.uniform(0.5, 1.2))
    # === 輸入 "GP" ===
    pyautogui.write('GP', interval=0.1)  # 模擬輸入，每個字母間隔0.1秒
    #搜尋
    random_x_offset = random.randint(772, 776)
    random_y_offset = random.randint(156, 162)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 2))
    pyautogui.mouseDown()
    pyautogui.click()
    # 等待畫面反應
    time.sleep(random.uniform(0.5, 1.2))
    while(1):
        # monitor = {"top": y + 433, "left": x + 353, "width": 98, "height": 24}
        re_OK = get_text_from_game_region(window_pos[0], window_pos[1],398,487,558-98,418-398)
        print(re_OK)
        if "GP交換" in re_OK:
            #點搜尋
            random_x_offset = random.randint(777, 784)
            random_y_offset = random.randint(401, 414)
            start_abs_x = window_pos[0] + random_x_offset
            start_abs_y = window_pos[1] + random_y_offset
            pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
            pyautogui.mouseDown()
            pyautogui.click()
            #點
            random_x_offset = random.randint(496, 510)
            random_y_offset = random.randint(212, 220)
            start_abs_x = window_pos[0] + random_x_offset
            start_abs_y = window_pos[1] + random_y_offset
            pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
            pyautogui.mouseDown()
            pyautogui.click()
            #點使用
            random_x_offset = random.randint(630, 743)
            random_y_offset = random.randint(442, 449)
            start_abs_x = window_pos[0] + random_x_offset
            start_abs_y = window_pos[1] + random_y_offset
            pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
            pyautogui.mouseDown()
            pyautogui.click()
            #點返回
            random_x_offset = random.randint(772, 780)
            random_y_offset = random.randint(155, 160)
            start_abs_x = window_pos[0] + random_x_offset
            start_abs_y = window_pos[1] + random_y_offset
            pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
            pyautogui.mouseDown()
            pyautogui.click()

            #搜尋
            random_x_offset = random.randint(772, 779)
            random_y_offset = random.randint(116, 125)
            start_abs_x = window_pos[0] + random_x_offset
            start_abs_y = window_pos[1] + random_y_offset
            pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
            pyautogui.mouseDown()
            pyautogui.click()
            # 等待畫面反應
            time.sleep(random.uniform(0.5, 1.2))
            #點打字區域
            random_x_offset = random.randint(490, 545)
            random_y_offset = random.randint(156, 160)
            start_abs_x = window_pos[0] + random_x_offset
            start_abs_y = window_pos[1] + random_y_offset
            pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
            pyautogui.mouseDown()
            pyautogui.click()
            # === 輸入 "GP" ===
            pyautogui.write('GP', interval=0.1)  # 模擬輸入，每個字母間隔0.1秒
            #搜尋
            random_x_offset = random.randint(772, 776)
            random_y_offset = random.randint(156, 162)
            start_abs_x = window_pos[0] + random_x_offset
            start_abs_y = window_pos[1] + random_y_offset
            pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 2))
            pyautogui.mouseDown()
            pyautogui.click()
            # 等待畫面反應
            time.sleep(random.uniform(2, 5))
        if not "GP交換" in re_OK:
            #點X
            random_x_offset = random.randint(779, 790)
            random_y_offset = random.randint(70, 72)
            start_abs_x = window_pos[0] + random_x_offset
            start_abs_y = window_pos[1] + random_y_offset
            pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 2))
            pyautogui.mouseDown()
            pyautogui.click()
            # 等待畫面反應
            time.sleep(random.uniform(0.5, 1.2))
            break




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
    random_x_offset = random.randint(629, 782)
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
    random_x_offset = random.randint(629, 782)
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
    time.sleep(random.randint(1, 2))
    #次元
    random_x_offset = random.randint(650, 750)
    random_y_offset = random.randint(444, 466)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #次元
    random_x_offset = random.randint(445, 540)
    random_y_offset = random.randint(380, 411)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    print("次元")
    while(1):
        re_OK = get_text_from_game_region(window_pos[0], window_pos[1],363,360,455-360,387-363)
        if re_OK=="移動至選單":

            #次元-移動至選單
            random_x_offset = random.randint(360, 455)
            random_y_offset = random.randint(363, 387)
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
    random_x_offset = random.randint(348, 455)
    random_y_offset = random.randint(350, 379)
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
    #課題-確認2
    random_x_offset = random.randint(348, 455)
    random_y_offset = random.randint(319, 343)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #課題-X
    random_x_offset = random.randint(780, 786)
    random_y_offset = random.randint(61, 73)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()
    #腳色變更清單
    random_x_offset = random.randint(695, 715)
    random_y_offset = random.randint(428, 453)
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

round0()

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