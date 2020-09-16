
#include<arduinoFFT.h>
int incomingByte = 0;

const int DTMF_freq1[] = {1336, 1209, 1336, 1477, 1209, 1336, 1477, 1209, 1336, 1477};
const int DTMF_freq2[] = {941,  697,  697,  697,  770,  770,  770,  852,  852,  852};
#define SAMPLES 64             //採樣樣本數, 必須是 2 的冪次方倍
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
  sampling_period_us = round(1000000*(1.0/SAMPLING_FREQUENCY)); //Period 
  pinMode(D5,OUTPUT);
  pinMode(D6,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()>0){
    incomingByte = Serial.read();
    int input = incomingByte-48;
    Serial.print("Input:");
    Serial.println(input,DEC);
    tone(D5,DTMF_freq1[input],500);
    tone(D6,DTMF_freq2[input],500);
    //analogWrite(D3,DTMF_freq1[input]);
    //analogWrite(D5,DTMF_freq2[input]);
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

    FFT.Windowing(vReal, SAMPLES, FFT_WIN_TYP_HAMMING, FFT_FORWARD);  //窗函數
    FFT.Compute(vReal, vImag, SAMPLES, FFT_FORWARD);   //正傅立葉轉換
    FFT.ComplexToMagnitude(vReal, vImag, SAMPLES);

    double High_peak = FFT.HighMajorPeak(vReal, SAMPLES, SAMPLING_FREQUENCY);
    double Low_peak  = FFT.LowMajorPeak(vReal, SAMPLES, SAMPLING_FREQUENCY);
    Serial.print(High_peak);
    Serial.print(" HZ , ");
    Serial.print(Low_peak);
    Serial.println(" hz");
    delay(100);
    judge(High_peak,Low_peak);
    //analogWrite(D3,0);
    //analogWrite(D5,0);
  }
}
void judge(double High_peak,double Low_peak){
  if(High_peak<1269){
    if(Low_peak<740){
      Serial.println("1");
    }
    else if(740<=Low_peak && Low_peak<800){
      Serial.println("4");
    }
    else{
      Serial.println("7");
    }
  }
  else if (1270<=High_peak && High_peak<1395){
    if(Low_peak<740){
      Serial.println("2");
    }
    else if(740<=Low_peak && Low_peak<800){
      Serial.println("5");
    }
    else if(800<=Low_peak && Low_peak<900){
      Serial.println("8");
    }
    else{
      Serial.println("0");
    }
  }
  else{
    if(Low_peak<740){
      Serial.println("3");
    }
    else if(740<=Low_peak && Low_peak<800){
      Serial.println("6");
    }
    else{
      Serial.println("9");
    }
  }
}
