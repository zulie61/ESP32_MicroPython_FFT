#include<Tone.h>
int incomingByte = 0;

Tone freq1;
Tone freq2;
const int DTMF_freq1[] = {1336, 1209, 1336, 1477, 1209, 1336, 1477, 1209, 1336, 1477};
const int DTMF_freq2[] = {941,  697,  697,  697,  770,  770,  770,  852,  852,  852};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("CHEAK IT OUT!!!");
  freq1.begin(11);
  freq2.begin(12);
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
    delay(300);
  }
}
