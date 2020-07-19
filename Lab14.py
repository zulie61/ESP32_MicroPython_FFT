from machine import Pin
from flag_pwm import PWM
from flag_fft import FFT
import time

def init():
    print("初始化開始")
    init_hz = []  # 欲存放初始頻率的空 list
    laser = PWM(Pin(25),freq=0)  # 建立 pwm 物件
    for i in range(127):  # 執行代表 ASCII 碼 0 ~ 126 的頻率
        laser.freq(10*i)
        time.sleep(0.1)   # 設定一點延遲時間, 防止錯誤
        
        fft = FFT(64,4000,34)   # 採樣數 64、採樣頻率4000、指定腳位34
        peak = fft.major_peak()  # 判斷該數字對應速度的聲音頻率為何
        
        print(peak)  # 將初始頻率顯示出來, 判斷是否初始化成功
        init_hz.append(peak) # 將初始頻率加入 list 內
    laser.deinit()

    threshold = [] # 欲存放閾值的空 list
    for j in range(126):
        loss = (init_hz[j] + init_hz[j+1]) / 2  # 相鄰兩項相加的平均
        threshold.append(loss)
        
    threshold.append(init_hz[126] + 100) # ASCII碼 126 初始頻率 +100
    print("初始化結束")
    return threshold

def run_judge(ascii_unm,threshold): # 主程式中重複執行的部分
    laser = PWM(Pin(25),freq=0)
    laser.freq(10*ascii_unm) # ascii碼 個別數字運轉
    time.sleep(0.1)
    fft=FFT(64,4000,34) # 採樣數 128、採樣頻率4000、指定腳位36
    peak = fft.major_peak() # 判斷該數字對應速度的聲音頻率為何
    laser.deinit()
    for i in range(127):
        if peak < threshold[i]: # 判斷落在哪一閾值內, 對應之索引便是該數字
            print(i, end ='')  # 將判斷的數字印出
            break # 停止迴圈

threshold = init()  # 取得閾值陣列

while True:
    data = input("請輸入:")
    print("您的輸入為:" + str(x))
    for i in range(len(data)):
        # ord 讓輸入轉為 ascii 碼, 型別為 int, 為了能夠依序執行, 因此再將其轉回 str
        ascii_num = ord(data[i]) # 將輸入資料轉為 ascii 碼
        run_judge(ascii_num,threshold) # 執行 run_judge() 函式
        print(end=' ') # 字與字之間加入空格
    print()