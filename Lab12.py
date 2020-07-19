from machine import Pin
from flag_pwm import PWM
from flag_fft import FFT
import time

def init():
    print("初始化開始")
    init_hz = []  # 欲存放初始頻率的空 list
    motor = PWM(Pin(25),duty=0) # 建立運轉馬達的 PWM 物件
    for i in range(10):  # 執行代表數字'0'~'9'的速度
        motor.duty(400 + 50*i) 
        time.sleep(1)   # 穩定轉速
         
        fft = FFT(64,4000,34)   # 採樣數 64、採樣頻率4000、指定腳位34
        peak = fft.major_peak()  # 判斷該數字對應速度的聲音頻率為何
        
        print(peak)  # 將初始頻率顯示出來, 判斷是否初始化成功
        init_hz.append(peak) # 將初始頻率加入 list 內
        
        motor.duty(0)  # 暫停運轉
        time.sleep(1)  # 穩定停止
    motor.deinit()  # 停止運轉馬達的 PWM 功能

    threshold = [] # 欲存放閾值的空 list
    for j in range(9):
        conti_ave = (init_hz[j] + init_hz[j+1]) / 2  # 相鄰兩項相加的平均
        threshold.append(conti_ave) # 加入閾值串列內

    threshold.append(init_hz[9] + 100) # 數字'9'的頻率 + 100
    print("初始化結束")
    return threshold # 回傳閾值陣列
     

def run_judge(ascii_unm,threshold): # 主程式中重複執行的部分
    motor = PWM(Pin(25),duty=0)
    motor.duty(400 + 50*ascii_unm) # ascii碼 個別數字運轉
    time.sleep(1) # 穩定轉速
    fft=FFT(64,4000,34) # 採樣數 128、採樣頻率4000、指定腳位34
    peak = fft.major_peak() # 判斷該數字對應速度的聲音頻率為何
    motor.duty(0) # 停止運轉
    motor.deinit()
    time.sleep(1) # 穩定停止
    
    for i in range(10):
        if peak < threshold[i]: # 判斷落在哪一閾值內, 對應之索引便是該數字
            print(i, end ='')  # 將判斷的數字印出
            break # 停止迴圈

for i in range(3,0,-1):  # 倒數三秒警示
    print(i)
    time.sleep(1)

threshold = init() # 取得閾值陣列

while True:
    data = input("請輸入:")
    print("您的輸入為:" + data)
    for i in range(len(data)):
        # ord 讓輸入轉為 ascii 碼, 型別為 int, 為了能夠依序執行, 因此再將其轉回 str 
        ascii_num = str(ord(data[i]))   
        for j in range(len(ascii_num)): # 轉為 str 後才可以使用 len 函式來看長度
            run_judge(int(ascii_num[j]),threshold)  # 轉回 int 作為運轉馬達的引數
        print(end=' ') # 字與字之間加入空格
    print()