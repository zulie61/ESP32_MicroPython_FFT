from machine import Pin,PWM
import time

buzzer = PWM(Pin(25),freq=0) # 建立 PWM 物件

tones = [261,294,330,349,392,440,494] # Do、Re、Mi、Fa、So、La、Si

for tone in tones:   # 依序取出各別音高的頻率
    buzzer.freq(tone)     # 播放指定頻率的聲音
    time.sleep(0.5)          # 持續 0.5 秒
    
buzzer.deinit()              # 關閉 PWM 功能, 停止發聲