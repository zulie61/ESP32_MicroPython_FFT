#include<arduinoFFT.h>
#define SAMPLES 128             //採樣樣本數, 必須是 2 的冪次方倍
#define SAMPLING_FREQUENCY 3800 //(能夠顯示的最高頻率 1700/2, 因為共軛對稱的緣故)
arduinoFFT FFT = arduinoFFT();

unsigned int samplingPeriod;
unsigned long microseconds;
double peak;
double vReal[SAMPLES];
double vImag[SAMPLES];
char cmd[9] ;
double filter[100];
int ambLightMax;
int ambLightMin;
int ambLight;
int collectTimes = sizeof(filter)/sizeof(double);

void setup() {
  Serial.begin(115200);
  //Serial.setTimeout(10);
  pinMode(5,OUTPUT);
  samplingPeriod = round(1000000*(1.0/SAMPLING_FREQUENCY)); //Period 
  for(int i=0;i<sizeof(filter)/sizeof(double);i++){
    fft();
    filter[i]=peak;
    delay(10);
  }
  ambLightMax = findMax(filter,collectTimes);
  ambLightMin = findMin(filter,collectTimes);
  ambLight = (ambLightMax+ambLightMin)/2;
  Serial.print(" environment light HZ:");
  Serial.print(" MAX:");
  Serial.print(ambLightMax);
  Serial.print(" MIN:");
  Serial.print(ambLightMin);
  Serial.print("AVG:");
  Serial.print(ambLight);
  Serial.println("========================");
}

void loop() {
 if(Serial.available()){
 /*Serial.readBytes(cmd,9);
 Serial.print("input:");
 Serial.print(atoi(cmd));
 Serial.println(" HZ");
 tone(D1,atoi(cmd));*/
 int input = Serial.read();
 Serial.print("Your input");
 Serial.println(input);
 tone(5,input*10+ambLight); //x + 平均環境光 + 12x

 if( (fft()<ambLightMax-10) || (fft()>ambLightMin+10) ){
   fft();
   Serial.print(peak);
   Serial.print(" Hz");
   Serial.println("=================");
   Serial.print(ambLight+13*input-3);
   Serial.print("//////");
   Serial.println(ambLight+13*input+9);
   for(int i=0;i<127;i++){
    if((peak>=(ambLight+13*i-3)) && (peak<=(ambLight+13*i+11))){ 
      
      Serial.print("ASCII: ");
      Serial.println(i);
      Serial.println("");
    }
   }
   //delay(250);
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
    
    
    peak = FFT.MajorPeak(vReal, SAMPLES, SAMPLING_FREQUENCY);   //低於一千基音頻 0 ~128/2-21+1 = 0~44
    
    //Serial.print(peak);
    //Serial.println("Hz");
    return peak;
}
double findMax(double *filter,int collectTimes){
  double compareMax=0;
  for(int i=0;i<collectTimes;i++){
    if((filter[i]>filter[i+1])&&(filter[i]>filter[i-1])){
      if(filter[i]>compareMax){
        compareMax = filter[i];
      }
    }
  }
  return compareMax;
}
double findMin(double *filter, int collectTimes){
  double compareMin=0;
  for(int i=0;i<collectTimes;i++){
    if((filter[i]<filter[i+1])&&(filter[i]<filter[i-1])){
      if(filter[i]>compareMin){
        compareMin = filter[i];
      }
    }
  }
  return compareMin;
}
