#include<arduinoFFT.h>
//#include <FlagMotor.h>

#define SAMPLES 128             //採樣樣本數, 必須是 2 的冪次方倍
#define SAMPLING_FREQUENCY 3000 //(能夠顯示的最高頻率 1700/2, 因為共軛對稱的緣故)

arduinoFFT FFT = arduinoFFT();

unsigned int samplingPeriod;
unsigned long microseconds;

double vReal[SAMPLES];
double vImag[SAMPLES];

void setup() {
    Serial.begin(9600); //設定鮑率
    samplingPeriod = round(1000000*(1.0/SAMPLING_FREQUENCY)); //Period 
    pinMode(5,OUTPUT);
}
void loop() 
{
  if(Serial.available()>0){
    int input = Serial.read()-48;
    analogWrite(5,70 + 18*input);
    delay(300);
  microseconds = micros();
    for(int i=0; i<SAMPLES; i++)
    {
       
        vReal[i] = analogRead(A0); //傅立葉實數等於測量值
        vImag[i] = 0; //虛數為零
      while(micros() - microseconds < samplingPeriod){
        //empty loop
      }
      microseconds += samplingPeriod;
  }
    FFT.Windowing(vReal, SAMPLES, FFT_WIN_TYP_HAMMING, FFT_FORWARD);  //窗函數
    FFT.Compute(vReal, vImag, SAMPLES, FFT_FORWARD);   //正傅立葉轉換
    FFT.ComplexToMagnitude(vReal, vImag, SAMPLES);  
    double peak = FFT.MajorPeak(vReal, SAMPLES, SAMPLING_FREQUENCY);   //低於一千基音頻 0 ~128/2-21+1 = 0~44
    Serial.print("input: ");
    Serial.print(input);
    Serial.print(" peak: ");
    Serial.println(peak);
    analogWrite(5,0);
    delay(1000);
  }
}


