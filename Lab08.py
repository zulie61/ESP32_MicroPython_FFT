from flag_fft import FFT
from flag_pwm import PWM
from machine import Pin
import time

# 電話按鍵聲 0~ 9 低頻
low_hz = [941, 697, 697, 697, 770, 770, 770, 852, 852, 852]
# 電話按鍵聲 0~ 9 高頻
high_hz = [1336, 1209, 1336, 1477, 1209, 1336, 1477, 1209, 1336, 1477]
# 電話按鍵聲 0~ 9 低頻閾值
low_loss = [740, 740, 740, 800, 800, 800, 900, 900, 900, 1000]
# 電話按鍵聲 0~ 9 高頻閾值
high_loss = [1269, 1395, 1600, 1269, 1395, 1600, 1269, 1395, 1600, 1395]


def which_num():
    fft = FFT(128, 3000, 34) # 執行一次
    low_peak = fft.interval_majorPeak(13, 23) # 判斷低頻的主頻率
    high_peak = fft.interval_majorPeak(23, 33) # 判斷高頻的主頻率

    for i in range(10): # 判斷低頻與高頻落在哪個區間內
        if low_peak < low_loss[i]: # 篩選位於哪個低頻閾值
            if high_peak < high_loss[i]: # 篩選出的低頻閾值中, 高頻聲音為何者
                print((i + 1) % 10) # 輸出按鍵聲的號碼
                break
while True:
    tone1 = PWM(Pin(25)) # 建立播放低頻聲音的 PWM 物件
    tone2 = PWM(Pin(27)) # 建立播放高頻聲音的 PWM 物件
    
    num = input('按鍵聲:') # 輸入按鍵號碼
    
    if num.isdigit(): # 判斷是否為數字
        for i in range(len(num)): # 將輸入數字依序播放
            tone1.freq(low_hz[int(num[i])]) # 播放低頻聲音
            tone2.freq(high_hz[int(num[i])]) # 播放高頻聲音
            time.sleep(0.25) # 持續 0.25 秒
            which_num() # 判斷此聲音屬於何按鍵聲
        tone1.duty(0) # 停止播放低頻音
        tone2.duty(0) # 停止播放高頻音
        
    tone1.deinit() # 停止播放低頻音的 PWM 功能
    tone2.deinit() # 停止播放高頻音的 PWM 功能