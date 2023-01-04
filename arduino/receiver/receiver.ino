#include <SPI.h>
#include <RF24.h>
 
const uint64_t pipe = 0xE8E8F0F0E1LL;
const uint64_t pipe2 = 0xE8E8F0F0E2LL; 
RF24 radio(8,9);
float temperature[3];
 
void setup(){
  Serial.begin(9600);
  radio.begin();                    
  radio.setAutoAck(1);              
  radio.setDataRate(RF24_1MBPS); 
  radio.setChannel(10);
//  radio.openReadingPipe(1,pipe2); 
//  radio.openReadingPipe(2,pipe2);  
//  radio.startListening();
}
 
void loop(){
  radio.openReadingPipe(1,pipe); 
  radio.startListening();
  while (!radio.available());
    radio.read(temperature, sizeof(temperature));
    Serial.print("!TEMP1:");
    Serial.print(temperature[0]);
    Serial.print("#");
    Serial.print("!HUMI1:");
    Serial.print(temperature[1]);
    Serial.print("#");
    Serial.print("!SOLAR1:");
    Serial.print(temperature[2]);
    Serial.print("#");
    Serial.println();
//  }
  radio.stopListening();

  radio.openReadingPipe(2,pipe2); 
  radio.startListening();
  while (!radio.available());
    radio.read(temperature, sizeof(temperature));
    Serial.print("!TEMP2:");
    Serial.print(temperature[0]);
    Serial.print("#");
    Serial.print("!HUMI2:");
    Serial.print(temperature[1]);
    Serial.print("#");
    Serial.print("!SOLAR2:");
    Serial.print(temperature[2]);
    Serial.print("#");
    Serial.println();
//  }
  radio.stopListening();
}
