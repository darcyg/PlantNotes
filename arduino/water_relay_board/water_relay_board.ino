/*     
      Plant Notes - Arduino water / relay board

      Switches relays on / off depending on commands send over radio.

      Created: 27/05/14
      Last Edited: 02/06/14

      Author: Gabriel Barnes, Jake Malley

      http://www.plantnotes.co.uk

*/
#include <SPI.h>
#include "RF24.h"

RF24 radio(9,10); 
const uint64_t pipes[2] = { 0xF0F0F0F0E2LL, 0xF0F0F0F0E1LL };
char payload[32];

void setup(void)
{
  Serial.begin(9600);
  // Setup Radio.
  setup_radio(78); // Start radio on channel 76.
  radio.startListening(); // Get the radio to start listening.
  Serial.println("Ready!");
  delay(1000); 
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  digitalWrite(2,LOW);
  digitalWrite(3,LOW);
  digitalWrite(4,LOW);
}

void loop(void)
{

  while (radio.available()) {
    unsigned char length = radio.getDynamicPayloadSize();
    radio.read(payload, length);
    payload[length] = 0;  // Don't print the rest of the buffer
    
    // Convert it into a string.
    String s = "";
    for (int i=0;i<length;i++){
     s = s + payload[i]; 
    }
    Serial.println(s);
    
    if (s=="cmd_01_on"){
      digitalWrite(2,HIGH);
    }
    if (s=="cmd_02_on"){
      digitalWrite(3,HIGH); 
    }
    if (s=="cmd_03_on"){
      digitalWrite(4,HIGH);
    }
    if (s=="cmd_01_off"){
      digitalWrite(2,LOW);
    }
    if (s=="cmd_02_off"){
      digitalWrite(3,LOW); 
    }
    if (s=="cmd_03_off"){
      digitalWrite(4,LOW);
    }

    
    
  }  
  delay(1000);
}

void setup_radio(int channel){
  radio.begin();
  radio.enableDynamicPayloads();
  radio.setDataRate(RF24_1MBPS);
  radio.setPALevel(RF24_PA_MAX);
  radio.setChannel(channel);
  radio.setRetries(15,15);
  radio.openWritingPipe(pipes[0]); 
  radio.openReadingPipe(1,pipes[1]); 
}
