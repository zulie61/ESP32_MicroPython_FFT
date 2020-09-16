#include<arduinoFFT.h>

#define SAMPLES 64             //採樣樣本數, 必須是 2 的冪次方倍
#define SAMPLING_FREQUENCY 7000 //(能夠顯示的最高頻率 7000/2)Ts = Based on Nyquist, must be 2 times the highest expected frequency.
arduinoFFT FFT = arduinoFFT();   //創建 FFT 物件

double vReal[SAMPLES]; //實數
double vImag[SAMPLES]; //虛數
unsigned int samplingPeriod;
unsigned long microseconds;

void fft(){
     microseconds = micros();
    for(int i=0; i<SAMPLES; i++)
    {
       
        vReal[i] = analogRead(A0); //傅立葉實數等於測量值
        vImag[i] = 0; //虛數為零
      while(micros() - microseconds < samplingPeriod){
        //empty loop 讓採樣頻率與運算的頻率要求相等
      }
      microseconds += samplingPeriod;
  }
    FFT.Windowing(vReal, SAMPLES, FFT_WIN_TYP_HAMMING, FFT_FORWARD);  //窗函數
    FFT.Compute(vReal, vImag, SAMPLES, FFT_FORWARD);   //正傅立葉轉換
    FFT.ComplexToMagnitude(vReal, vImag, SAMPLES);
}

void setup() {
    Serial.begin(115200); //設定鮑率
    samplingPeriod = round(1000000*(1.0/SAMPLING_FREQUENCY)); //Period 
}

void loop() {
 fft();
 double peak1 = FFT.MajorPeak(vReal, SAMPLES, SAMPLING_FREQUENCY);      //全體主頻率
 Serial.println(peak1);
 delay(100);
}

