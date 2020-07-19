import math
import time
from machine import Pin,ADC

class FFT():
    def __init__(self,samples,samplingFrequency,pin):
        global vReal, vImag
        self.samples = samples #設定採樣數
        vReal = [0]*self.samples #設定儲存資料陣列
        vImag = [0]*self.samples #設定儲存資料陣列

        self.samplingFrequency = samplingFrequency #設定採樣頻率
        self.pin = pin #設定讀取資料腳位
        
        '''設定讀取腳位'''
        adc = ADC(Pin(pin)) 
        adc.width(ADC.WIDTH_10BIT)  # 設定ADC解析度
        adc.atten(ADC.ATTN_11DB)    # 設定最大電壓為3.6V
           
       #data -> windowing function (hamming) -> fft kernel -> get magnitude
        '''採樣資料'''
        microseconds = time.ticks_us()
        samplingPeriod = round(1000000*(1.0/self.samplingFrequency))
        for  i in range(self.samples):
            vReal[i] = adc.read() #收集感測器資料
            #vImag[i]=0 , 第10行已建立
            while  (time.ticks_us() - microseconds) < samplingPeriod :
                pass  #確保採樣時間固定, 每 1/採樣頻率 秒收集一次資料
            microseconds += samplingPeriod
            
        '''窗函數'''
        samplesMinusOne = self.samples - 1.0
        for i in range(self.samples>>1):
             indexMinusOne = i/1.0
             ratio = indexMinusOne / samplesMinusOne
             weighingFactor = 0.54 - (0.46 * math.cos(2*math.pi * ratio))  #HAMMING窗函數
             vReal[i] *= weighingFactor  #採樣資料逐一乘上窗函數
             vReal[self.samples - (i + 1)] *= weighingFactor
             
        '''對資料進行FFT'''

        j = 0
        for  i in range(self.samples):
            if j > i :
                vReal[i],vReal[j] = vReal[j],vReal[i]
                vImag[i],vImag[j] = vImag[j],vImag[i]
            m = self.samples>>1
            while j >= m and m >0 :
                j -= m
                m >>=1
            j+=m
        
        mmax = 1
        while self.samples >mmax:
            istep = mmax << 1
            theta = -2.0*math.pi/istep
            wtemp = math.sin(0.5*theta)
            wpr = -2.0*wtemp*wtemp
            wpi = math.sin(theta)
            wr = 1.0
            wi = 0.0
            for m in range(mmax):
                for i in range(m,self.samples,istep):
                    j = i +mmax
                    tempr = wr * vReal[j] - wi * vImag[j]
                    tempi = wr * vImag[j] + wi * vReal[j]
                    vReal[j] = vReal[i] - tempr
                    vImag[j] = vImag[i] - tempi
                    vReal[i] += tempr
                    vImag[i] += tempi
                wtemp = wr
                wr = wr*wpr -wi*wpi +wr
                wi = wi*wpr + wtemp*wpi + wi
            mmax = istep
        
        
        
        '''轉換為頻率強度'''
        for i in range(self.samples):
            vReal[i] = math.sqrt((vReal[i])**2 + (vImag[i])**2)
        #print(vReal.shape())
    
    def magnitude(self):
        return vReal[0:self.samples>>1]

    def major_peak(self): #主頻率
        
        vReal2 = vReal[2:self.samples>>1]
        
        #IndexOfMaxY = np.argmax(vReal2)+2  #第一項為直流分量, 不參考
        IndexOfMaxY = vReal2.index(max(vReal2))+2  #第一項為直流分量, 不參考
        '''運算主頻率'''
        try:
            delta = 0.5 * ((vReal[IndexOfMaxY-1] - vReal[IndexOfMaxY+1]) / (vReal[IndexOfMaxY-1] - (2.0 * vReal[IndexOfMaxY]) + vReal[IndexOfMaxY+1]))

        
            if IndexOfMaxY == (self.samples >> 1):
                interpolatedX = ((IndexOfMaxY + delta)  * self.samplingFrequency) / (self.samples)
            else:
                interpolatedX = ((IndexOfMaxY + delta)  * self.samplingFrequency) / (self.samples-1)
            return interpolatedX
        
        except ZeroDivisionError:
            pass

    
    def interval_majorPeak(self,start,end): #區間主頻律
        self.start = start
        self.end = end
        vReal2 = vReal[self.start:self.end]
        IndexOfMaxY = vReal2.index(max(vReal2)) + self.start
        
        '''運算主頻率'''
        try:
            delta = 0.5 * ((vReal[IndexOfMaxY-1] - vReal[IndexOfMaxY+1]) / (vReal[IndexOfMaxY-1] - (2.0 * vReal[IndexOfMaxY]) + vReal[IndexOfMaxY+1]))

        
            if IndexOfMaxY == (self.samples >> 1):
                interpolatedX = ((IndexOfMaxY + delta)  * self.samplingFrequency) / (self.samples)
            else:
                interpolatedX = ((IndexOfMaxY + delta)  * self.samplingFrequency) / (self.samples-1)
            return interpolatedX
        
        except ZeroDivisionError:
            pass
    