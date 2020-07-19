from flag_fft import FFT
import time

# 電話按鍵聲 0~ 9 低頻閾值
low_loss = [740, 740, 740, 800, 800, 800, 900, 900, 900, 1000]
# 電話按鍵聲 0~ 9 高頻閾值
high_loss = [1269, 1395, 1600, 1269, 1395, 1600, 1269, 1395, 1600, 1395]

'''收集判斷的按鍵, 將判斷數字的次數儲存至 list 內'''
def which_num(occur):
    for j in range(10):
        fft = FFT(64,3000,34) # 執行一次
        low_peak = fft.interval_majorPeak(13,23) # 判斷低頻區間的主頻率
        high_peak = fft.interval_majorPeak(23,33) # 判斷高頻區間的主頻率
        for i in range(10): # 判斷低頻與高頻落在哪個區間內
            if low_peak < low_loss[i]: # 篩選位於哪個低頻閾值
                if high_peak < high_loss[i]: # 篩選出的低頻閾值中, 高頻聲音為何者
                    occur[i] += 1 # 判斷出的數字出現次數 + 1
                    break
    print((occur.index(max(occur))+1)%10)  # 輸出判斷最多次的按鍵聲號碼

def judge(mean_mag):
    low_exist = False # 判斷是否存在電話按鍵聲的低頻
    high_exist = False # 判斷是否存在電話按鍵聲的低頻
    fft = FFT(64,3000,34)
    magnitude = fft.magnitude() # 取得頻率強度
    low_sum = sum(magnitude[13:22])  # 低頻區間的強度總和
    high_sum = sum(magnitude[23:32]) # 高頻區間的強度總和
    
    # 低頻與高頻平均強度是否大於環境頻率平均強度的1.4倍
    if (low_sum/9 > mean_mag*1.5) and (high_sum/9 > mean_mag*1.5): 
    
        for i in range(9):
            # 收集低頻區間連續兩個的頻率強度
            low_conti = magnitude[13+i] + magnitude[14+i]
            # 收集高頻區間連續兩個的頻率強度
            high_conti = magnitude[23+i] + magnitude[21 +i] 
            
            # 連續強度是否佔低頻區間的 30 %以上
            if (low_conti > low_sum*0.4): 
                low_exist = True 
                
            # 連續強度是否佔高頻區間的 30 %以上
            if (high_conti > high_sum*0.4):
                high_exist = True 
                
            #確認出現電話按鍵聲, 執行 which_num 函式
            if (low_exist == True) and (high_exist == True) :
                occur = [0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ]  # 重置儲存次數陣列
                which_num(occur)
                break


fft = FFT(64, 3000, 34)
#將第 0 項、第 1 項頻率強度刪除
magnitude = fft.magnitude()[13:32] 
#將該次 FFT 的平均強度加入 mean_mag
mean_mag = sum(magnitude)/len(magnitude) 

while True:
    judge(mean_mag)