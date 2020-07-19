'''
RMT 參考網址：
http://docs.micropython.org/en/latest/library/esp32.html#esp32-rmt
https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/rmt.html
RMT 使用方法：
https://dev.to/codemee/esp32-rmt-pwm-3ki6
'''
import esp32
from machine import Pin
import time

class PWM():
    global channel
    channel = [None]*8
    
    def __init__(self,pin,freq=5000,duty=512):
        
        for i in range(len(channel)):
            if channel[i] == None:
                channel[i] = i
                self.pwmchannel = i
                break
            
        self.pin = pin
        self.freq_alt = freq
        self.duty_alt = duty
        
        if self.freq_alt < 35: #防止 write_pulses 的 tuple 內元素值超過
            self.freq_alt = 35
        if self.duty_alt < 2 :
            self.duty_alt = 2

        period = 1000000/self.freq_alt  #pwm 週期時間, 單位 us  ----[請看最下面註解]
        high_t = int(period*(self.duty_alt/1023)) #高電位一周期內持續時間
        low_t = int(period - high_t) #低電位持續時間 = 週期 - 高電位持續時間
        
        self.r = esp32.RMT(self.pwmchannel, pin=self.pin, clock_div=80) #預設clock_div=80, pwm 單為時間為 us
        self.r.write_pulses((high_t,low_t),start=1)

    def freq(self,freq):
        self.freq_alt = freq
        
        if self.freq_alt == 0 : # freq = 0 ---> 運算分母為 0 (error)
            self.freq_alt += 1
            
        period = 1000000/self.freq_alt  
        high_t = int(period*(self.duty_alt/1023))
        low_t = int(period - high_t)
        
        
        self.r.loop(False)
        self.r.write_pulses((high_t,low_t),start=1)
        self.r.loop(True)
        
    def duty(self,duty):
        self.duty_alt = duty
        
        if self.duty_alt < 2 : #防止 tuple 元素值超過
            self.r.loop(False)
        else:
            period = 1000000/self.freq_alt
            high_t = int(period*(self.duty_alt/1023))
            low_t = int(period - high_t)
                    
            self.r.loop(False)
            self.r.write_pulses((high_t,low_t),start=1)
            self.r.loop(True)
        

    
    def deinit(self,):  #停止rmt
        channel[self.pwmchannel] = None
        self.r.loop(False)
        self.r.deinit()

'''
若頻率設定為 500Hz, 表示 1 秒震動 500 次, 也就是 0.02 秒 1 次, 等於 2000 微秒 1 次 (此處單位為微秒),
因此週期就是 2000 微秒。若 duty cycle = 512 -> 512/1023 大約等於50 %, 則：
高電位持續 2000*50% = 1000 微秒, 低電位持續 2000 * 50% = 1000微秒 
若 duty cycle = 75 % 表示:
高電位持續 2000*75% = 1500 微秒, 低電位持續 2000 * 25% = 500 微秒
因此 週期 = 高電位持續時間 + 低電位持續時間
--------------------------------------------------------------------------------------------------
若頻率設定為 x, 表示 1 秒震動 x 次, 也就是 1/x 秒 1 次, 等於 1000000 * 1/x 微秒 1 次,
因此週期就是 1000000 * 1/x 微秒。duty cycle = y -> y/1023 大約等於 y/1023 %, 則:
高電為持續 1000000 * 1/x * y/1023, 由於 週期 = 高電位持續時間 + 低電位持續時間,
因此 低電位持續時間 = 週期 - 高電位持續時間
低電位持續 (1000000 * 1/x) - (1000000 * 1/x * y/1023)

'''
