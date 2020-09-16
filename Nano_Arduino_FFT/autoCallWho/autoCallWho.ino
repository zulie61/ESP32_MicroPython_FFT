#include<arduinoFFT.h>
#define SAMPLES 64             //採樣樣本數, 必須是 2 的冪次方倍
#define SAMPLING_FREQUENCY 3000 //(能夠顯示的最高頻率 1700/2, 因為複數對稱的緣故)Ts = Based on Nyquist, must be 2 times the highest expected frequency.
arduinoFFT FFT = arduinoFFT();   //創建 FFT 物件
unsigned int samplingPeriod;
double vReal[SAMPLES]; //實數
double vImag[SAMPLES]; //虛數
unsigned int sampling_period_us;
unsigned long microseconds;

int low_frq[]={740,740,740,800,800,800,900,900,900,1000};
int high_frq[]={1269,1395,1500,1269,1395,1500,1269,1395,1500,1395};
int occur[]={0,0,0,0,0,0,0,0,0,0};
int index=0;
int maxnum=0;
int judgenum=0;

void setup() {
  Serial.begin(9600);
  Serial.println("CHEAK IT OUT!!!");
  sampling_period_us = round(1000000*(1.0/SAMPLING_FREQUENCY)); //Period 
}

void loop() {
  fft();
  startup();
}

void fft(){                  //執行一次 fft
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
}

void startup(){    
  int low=0;
  int high=0;
  int startlow=0;
  int starthigh=0;

    for(int i=0;i<10;i++){
      low += vReal[13+i];
      high += vReal[23+i];
    }
  for(int i=0;i<10;i++){           
  if((vReal[13+i]+vReal[14+i])>low*3/5 && (vReal[13+i]+vReal[14+i])>15){    //low區間裡是否有連續兩個值相加 佔60%以上, 且此兩值加總大於15,若出現一次 startlow +1
      startlow+=1;
    }
  if((vReal[23+i]+vReal[24+i])>high*3/5 && (vReal[23+i]+vReal[24+i])>15){   //high區間裡是否有連續兩個值相加 佔60%以上, 且此兩值加總大於15, 若出現一次 starthigh +1
      starthigh+=1;
    }
  }
  if(startlow>0&&starthigh>0){    //low、high區間都有出現的話, 那麼表示現在有電話聲---->開始收集練續8次FFT的值來判斷究竟是什麼號碼
    for(int i=0;i<10;i++){
      fft();
      getAppearTimes();
    }
    findMaxIndex();
   // Serial.println(judgenum);
        for (int i = 0; i <= 9; i++) {
      Serial.print(occur[i]) ;
    }
    Serial.println("=========");
    for(int i=0;i<10;i++){
    occur[i]=0;
    }
  }
}

void getAppearTimes(){
  double low_peak  = FFT.AdjustMajorPeak(vReal, SAMPLES, SAMPLING_FREQUENCY,13,23);
  double high_peak = FFT.AdjustMajorPeak(vReal, SAMPLES, SAMPLING_FREQUENCY,23,33);
  Serial.println(high_peak);
  //Serial.println(low_peak);

  for(int i=0;i<10;i++){
    if( low_peak < low_frq[i]){
    if( high_peak < high_frq[i]){
     // Serial.println(String(high_peak)+String(",")+String(low_peak));
        occur[i]+=1; 
        break;
      }
    }
  }
}
void findMaxIndex(){         //找出數值最大的那個索引
  maxnum=occur[0];  
  index = 0;
  for(int i=1;i<10;i++){
    if(occur[i]>maxnum){
      index=i;
      maxnum=occur[i];
    }
  }
  judgenum = (index+1)%10;
}


