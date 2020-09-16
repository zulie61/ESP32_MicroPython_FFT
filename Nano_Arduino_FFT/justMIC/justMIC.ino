

void setup() {
  Serial.begin(115200);
  uint8_t result = 0;
  while (((64 >> result) & 1) != 1) result++;
  Serial.println(result);
}

void loop() {
  //Serial.println(analogRead(A0));
  //delay(100);
}
