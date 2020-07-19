from machine import Pin,PWM
import time

buzzer = PWM(Pin(25),freq=0) # 建立 PWM 物件

buzzer.freq(261) # Do
time.sleep(0.5)  # 持續 0.5 秒
buzzer.freq(294) # Re
time.sleep(0.5)  # 持續 0.5 秒
buzzer.freq(330) # Mi
time.sleep(0.5)  # 持續 0.5 秒
buzzer.freq(349) # Fa
time.sleep(0.5)  # 持續 0.5 秒
buzzer.freq(392) # So
time.sleep(0.5)  # 持續 0.5 秒
buzzer.freq(440) # La
time.sleep(0.5)  # 持續 0.5 秒
buzzer.freq(494) # Si
time.sleep(0.5)  # 持續 0.5 秒

buzzer.deinit()  # 關閉 PWM 功能, 停止發聲