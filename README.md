# ESP32_MicroPython_FFT
使用 ESP32 控制板與 Python 實作快速傅立葉轉換 (Fast Fourier Transform, FFT)
重點實驗：電話按鍵竊聽器、風速傳訊器、雷射傳訊器

由淺至深實驗, 從不會到精通：

LAB01：閃爍 LED
 說明：首次使用 ESP32 控制板與 Python 程式語言, 建立基本觀念。

LAB02：播放聲音
 說明：使用 PWM 控制頻率使喇叭播放 Do、Re、Mi...
 
LAB03：播放聲音(使用 list、for loop)
 說明：學習使用 list、for loop 讓播放聲音輕鬆又快速
 
LAB04：合成聲音
 說明：由於 MicroPython_ESP32 內建 PWM 無法同時播放 2 個頻率, 因此匯入客製化 flag_pwm 模組仿照原 PWM 功能同時播放多頻聲音
 
LAB05：撥打電話
 說明：使用 input() 函式輸入電話號碼, 喇叭播放對應電話按鍵聲頻率, 仿照撥打電話
 
LAB06：看見聲音
 說明：使用麥克風模組, 接收其 ADC 值, 藉由互動裝置輸出值, 並從繪圖器見識聲波樣貌
 
LAB07：初探 FFT
 說明：匯入自製模組 flag_fft 使用 FFT 觀察環境音頻

LAB08：判斷電話按鍵聲
說明：使用喇叭造電話按鍵聲, 由麥克風接收後判斷按鍵數字

LAB09：電話按鍵竊聽器
說明：自動化判斷環境中是否有出現電話按鍵聲, 並輸出該按鍵數字

LAB10：控制馬達運轉
 說明：調整 duty cycle 控制馬達轉速

LAB11：監聽風速頻率
 說明：將馬達裝上風扇, 藉由轉速控制風速, 觀察風速造成的生音頻率

LAB12：風速傳訊器：
 說明：將傳入訊息轉換為 ASCII 碼, 給定數字 0 ~ 9 指定 ducy cycle, 使用風扇運轉每個訊息的 ASCII 碼並接收與判斷
 
LAB13：感受光亮變化：
 說明：讀取光敏電阻 ADC 值, 感受光亮變化

LAB14：雷射傳訊器：
 說明：使用雷射模組迅速閃爍 ASCII 碼 (使用 PWM)
 
模組：
**flag_pwm：
  說明：使用 RAM 仿造 PWM 功能

**flag_fft：
 [1] 採樣 -> Window Function -> FFT 演算法 
 [2] 輸出頻率強度 list
 [3] 使用 beat frequency 分析主頻率
 [4] 輸出指定頻率區間主頻率
 
