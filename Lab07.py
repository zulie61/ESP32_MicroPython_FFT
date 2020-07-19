from flag_fft import FFT 
import time

#while True:
fft = FFT(64, 4000, 34) # 建立 FFT 物件
#peak = fft.major_peak() # 判斷主頻率
#print(peak)
for i in fft.magnitude():
    print(i)
time.sleep(0.1) # 等候 0.1 秒
