from flag_pwm import PWM
from machine import Pin
import time

# 電話按鍵聲 0~ 9 低頻
low_hz = [941, 697, 697, 697, 770, 770, 770, 852, 852, 852]
# 電話按鍵聲 0~ 9 高頻
high_hz = [1336, 1209, 1336, 1477, 1209, 1336, 1477, 1209, 1336, 1477]

while True:
    tone1 = PWM(Pin(25)) # 建立播放低頻聲音的 PWM 物件
    tone2 = PWM(Pin(27)) # 建立播放低頻聲音的 PWM 物件
    
    nums = input('按鍵聲:')
    
    if nums.isdigit():                        # 判斷是否為數字
        for num in nums:                        # 一一取出個別數字
            tone1.freq(low_hz[int(num)])  # 依照數字播放按鍵低頻音
            tone2.freq(high_hz[int(num)]) # 依照數字播放按鍵高頻音
            time.sleep(0.5)                  # 持續 0.5 秒
        tone1.duty(0)                         # 停止播放低頻音
        tone2.duty(0)                         # 停止播放高頻音
        
    tone1.deinit()         # 停止播放低頻音的 PWM 功能
    tone2.deinit()         # 停止播放高頻音的 PWM 功能