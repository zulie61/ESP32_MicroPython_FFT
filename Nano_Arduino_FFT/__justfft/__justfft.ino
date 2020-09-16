#include<arduinoFFT.h>


#define SAMPLES  8                    
#define SAMPLING_FREQUENCY 3000 


arduinoFFT FFT = arduinoFFT();

double vReal[SAMPLES]; 
double vImag[SAMPLES]; 
unsigned int samplingPeriod;
unsigned long microseconds;

void fft(){
     microseconds = micros();
    for(int i=0; i<SAMPLES; i++)
    {
        vReal[i] = analogRead(0);
        vImag[i] = 0;
      while(micros() - microseconds < samplingPeriod){
        //empty loop
      }
      microseconds += samplingPeriod;
  }
    FFT.Windowing(vReal, SAMPLES, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
    for(int i=0; i<SAMPLES; i++){
      Serial.println(vReal[i]);
    }
    Serial.println("---------------");
    FFT.Compute(vReal, vImag, SAMPLES, FFT_FORWARD); 
    for(int i=0; i<SAMPLES; i++){
      Serial.println(vReal[i]);
    }
    Serial.println("---------------");
    FFT.ComplexToMagnitude(vReal, vImag, SAMPLES);
    for(int i=0; i<SAMPLES; i++){
      Serial.println(vReal[i]);
    }
    Serial.println("---------------");
}

void setup() {
    Serial.begin(115200); 
    samplingPeriod = round(1000000*(1.0/SAMPLING_FREQUENCY));
    pinMode(3,OUTPUT);
    fft();
}

void loop() {
 //fft();
 
 //double peak = FFT.MajorPeak(vReal, SAMPLES, SAMPLING_FREQUENCY);  
// Serial.println(peak);
// delay(100);    
//  if(Serial.available()){
//   int input = Serial.read();
//   tone(3,input*10);
//  }
}


