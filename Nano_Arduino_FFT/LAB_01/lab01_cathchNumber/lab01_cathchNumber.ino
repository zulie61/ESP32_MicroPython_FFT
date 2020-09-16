#include<Tone.h>
#include<arduinoFFT.h>
int incomingByte = 0;
Tone freq1;
Tone freq2;
const int DTMF_freq1[] = {1336, 1209, 1336, 1477, 1209, 1336, 1477, 1209, 1336, 1477};
const int DTMF_freq2[] = {941,  697,  697,  697,  770,  770,  770,  852,  852,  852};
#define SAMPLES 128             //採樣樣本數, 必須是 2 的冪次方倍
#define SAMPLING_FREQUENCY 3000 //(能夠顯示的最高頻率 1700/2, 因為複數對稱的緣故)Ts = Based on Nyquist, must be 2 times the highest expected frequency.
arduinoFFT FFT = arduinoFFT();   //創建 FFT 物件
unsigned int samplingPeriod;
double vReal[SAMPLES]; //實數
double vImag[SAMPLES]; //虛數
unsigned int sampling_period_us;
unsigned long microseconds;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("CHEAK IT OUT!!!");
  freq1.begin(5);
  freq2.begin(6);
  sampling_period_us = round(1000000*(1.0/SAMPLING_FREQUENCY)); //Period 
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()>0){
    incomingByte = Serial.read();
    int input = incomingByte-48;
    Serial.print("Input:");
    Serial.println(input,DEC);
    freq1.play(DTMF_freq1[input],200);
    freq2.play(DTMF_freq2[input],200);

    fft();

  }
}

void fft(){
        microseconds = micros();
    for(int i=0; i<SAMPLES; i++)
    {
       
        vReal[i] = analogRead(A0); //傅立葉實數等於測量值
        vImag[i] = 0; //虛數為零
      while(micros() - microseconds < sampling_period_us){
        //empty loop
      }
      microseconds += sampling_period_us;
  }
        //Serial.println(vReal[i]);
     /* FFT on samples*/
    FFT.Windowing(vReal, SAMPLES, FFT_WIN_TYP_HAMMING, FFT_FORWARD);  //窗函數
    FFT.Compute(vReal, vImag, SAMPLES, FFT_FORWARD);   //正傅立葉轉換
    FFT.ComplexToMagnitude(vReal, vImag, SAMPLES);
     
    /*Find peak frequency and print peak*/
    double peak = FFT.MajorPeak(vReal, SAMPLES, SAMPLING_FREQUENCY);   //基音頻
    double High_peak = FFT.HighMajorPeak(vReal, SAMPLES, SAMPLING_FREQUENCY);
    double Low_peak  = FFT.LowMajorPeak(vReal, SAMPLES, SAMPLING_FREQUENCY);
    Serial.print(High_peak);
    Serial.print(" HZ , ");
    Serial.print(Low_peak);
    Serial.println(" hz");
    delay(100);
}

