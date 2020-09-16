#include<arduinoFFT.h>
#define SAMPLES 128             //採樣樣本數, 必須是 2 的冪次方倍
#define SAMPLING_FREQUENCY 3000 //(能夠顯示的最高頻率 1700/2, 因為共軛對稱的緣故)
arduinoFFT FFT = arduinoFFT();

unsigned int samplingPeriod;
unsigned long microseconds;
double peak;
double vReal[SAMPLES];
double vImag[SAMPLES];;

double count;
int realpeak[127];

void setup() {
  Serial.begin(115200);
  //Serial.setTimeout(10);
  pinMode(5,OUTPUT);
  samplingPeriod = round(1000000*(1.0/SAMPLING_FREQUENCY)); //Period 

  for(int i=30;i<127;i++){
    tone(5,i*10);
    //delay(100);
    fft();
    realpeak[i] = peak;
    //Serial.print(count);
    //Serial.println("%");
    //count += 0.78;
    
    //Serial.print(i);
    //Serial.print("=====");
    Serial.println(peak);
  }
}

void loop() {
 if(Serial.available()){
   int input = Serial.read();
   Serial.print("Your input");
   Serial.println(input);
   tone(5,input*10,100);
   fft();
 
   for(int i=30;i<127;i++){
    if((peak>=(realpeak[i] -3)) && (peak<=(realpeak[i] +3))){ 
      
      Serial.print("predict: ");
      Serial.println(i);
      //Serial.println("");
    }
   }
  }

}

double fft(){
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
    
    
    peak = FFT.MajorPeak(vReal, SAMPLES, SAMPLING_FREQUENCY); 

    return peak;
}

