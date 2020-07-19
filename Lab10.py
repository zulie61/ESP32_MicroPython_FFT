from flag_pwm import PWM
from machine import Pin
import time

while True:
    motor = PWM(Pin(25),duty=0) # 建立運轉馬達的 PWM 物件
    
    speed = int(input("指定 duty 為："))
    
    print("開始運轉")
    motor.duty(speed) # 運轉指定 duty 值的速度
    time.sleep(1) # 持續 1 秒

    motor.deinit() # 停止運轉馬達的 PWM 功能
    print("結束運轉, 待馬達完全停止再繼續輸入")