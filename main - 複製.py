import pygetwindow as gw
import pyautogui
import time
import random

count = 0
#腳色數量
endcount = 26
count_pass = 0 #從第幾隻腳側開始
count = count_pass


# 獲取窗口的位置和大小
def get_window_position(window_title):
    try:
        window = gw.getWindowsWithTitle(window_title)[0]
        x, y = window.left, window.top
        width, height = window.width, window.height
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
    #按X
    random_x_offset = random.randint(773, 789)
    random_y_offset = random.randint(56, 74)
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

    time.sleep(random.randint(60, 70))
    #每日地城-移動到選單
    random_x_offset = random.randint(354, 454)
    random_y_offset = random.randint(392, 414)
    start_abs_x = window_pos[0] + random_x_offset
    start_abs_y = window_pos[1] + random_y_offset
    pyautogui.moveTo(start_abs_x, start_abs_y, duration=random.randint(1, 3))
    pyautogui.mouseDown()
    pyautogui.click()

    time.sleep(random.randint(1, 3))
    #每日地城-X
    random_x_offset = random.randint(776, 789)
    random_y_offset = random.randint(58, 70)
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
    random_x_offset = random.randint(420, 647)
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
    random_x_offset = random.randint(-5, 5)
    random_y_offset = random.randint(-5, 5)
    start_abs_x = window_pos[0] + random_x_offset+ 783
    start_abs_y = window_pos[1] + random_y_offset+ 52
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
display_and_click_relative_position("MapleStoryM")

window_pos = get_window_position("MapleStoryM")
# if window_pos:
#     print(f"窗口 '{window_title}' 位置: ({window_pos[0]}, {window_pos[1]}), 大小: ({window_pos[2]}x{window_pos[3]})")


random_x_offset = random.randint(-5, 5)
random_y_offset = random.randint(-5, 5)
start_abs_x = window_pos[0] + random_x_offset+ 30
start_abs_y = window_pos[1] + random_y_offset+ 15
pyautogui.click(start_abs_x, start_abs_y)
time.sleep(random.randint(1, 5))



while(1):
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