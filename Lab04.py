from flag_pwm import PWM    # 使用旗標客製板本的 PWM 功能
from machine import Pin
import time

# 電話按鍵聲 0~ 9 低頻
low_hz = [941, 697, 697, 697, 770, 770, 770, 852, 852, 852]
# 電話按鍵聲 0~ 9 高頻
high_hz = [1336, 1209, 1336, 1477, 1209, 1336, 1477, 1209, 1336, 1477]

tone1 = PWM(Pin(25))      # 建立播放低頻聲音的 PWM 物件
tone2 = PWM(Pin(27))      # 建立播放高頻聲音的 PWM 物件

for i in range(10):         # 依序播放電話按鍵聲 0~9 的聲音
    tone1.freq(low_hz[i])   # 播放低頻聲音
    tone2.freq(high_hz[i])  # 播放高頻聲音
    time.sleep(0.25)        # 持續 0.25 秒

tone1.deinit()              # 停止播放低頻音的 PWM 功能
tone2.deinit()              # 停止播放高頻音的 PWM 功能