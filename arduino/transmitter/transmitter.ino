#include <SPI.h>
#include <RF24.h>
#include <DHT.h>
 
const uint64_t pipe = 0xE8E8F0F0E2LL;
RF24 radio(8,9); 
const int DHTPIN = 2;      
const int DHTTYPE = DHT11;
const int solar_in = 5;
const int solar_out = 6;
float h = 0.0;
float t = 0.0;
float temperature[3];

DHT dht(DHTPIN, DHTTYPE);
void read_dht(void);
void read_solar(void);
 
void setup(){ 
  //============================================================Module NRF24
  Serial.begin(9600);
  radio.begin();                   
  radio.setAutoAck(1);               
  radio.setRetries(1,1);             
  radio.setDataRate(RF24_1MBPS);  
  radio.setPALevel(RF24_PA_MAX);    
  radio.setChannel(10);            
  radio.openWritingPipe(pipe);
  dht.begin();
  pinMode(solar_in, INPUT);
  pinMode(solar_out, OUTPUT);
}
 
void loop(){
  read_solar();
}

void read_dht(void) {
  h = dht.readHumidity();    
  t = dht.readTemperature(); 
  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read");
    return;
  }
  Serial.println(t);
  Serial.println(h);
  temperature[0] = t;
  temperature[1] = h;
  
}

void read_solar(void) {
  for (int i = 0; i < 255; i++) {
    analogWrite(solar_out, i);
    read_dht();
    temperature[2] = 4.5 + analogRead(solar_in) * (5.4 - 4.5) / 1023;
    radio.write(temperature, sizeof(temperature));
    delay(1000);
  }

  for (int i = 255; i > 0; i--) {
    analogWrite(solar_out, i);
    read_dht();
    temperature[2] = 4.5 + analogRead(solar_in) * (5.4 - 4.5) / 1023;
    radio.write(temperature, sizeof(temperature));
    delay(1000);
  }
}
