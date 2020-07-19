from machine import Pin,ADC
import time

adc = ADC(Pin(34))    # 設定進行 ADC 的腳位
adc.atten(ADC.ATTN_11DB)    # 設定最大電壓為3.6V

while True:
    print(adc.read()) # 讀取 ADC 值
    time.sleep(0.05)  # 等候 0.05 秒