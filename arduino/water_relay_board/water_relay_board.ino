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

// Define pins
int relay01 = 2;
int relay02 = 3;

int output01 = 6;
int output02 = 7;

int buzzer = 8;

void setup(void)
{
  Serial.begin(9600);
  // Setup Radio.
  setup_radio(78); // Start radio on channel 76.
  radio.startListening(); // Get the radio to start listening.
  Serial.println("Ready!");
  
  pinMode(relay01, OUTPUT);
  digitalWrite(relay01,0);
  pinMode(relay02, OUTPUT);
  digitalWrite(relay02,0);
  
  pinMode(output01, OUTPUT);
  digitalWrite(output01,0);
  pinMode(output02, OUTPUT);
  digitalWrite(output02,0);
  
  pinMode(buzzer, OUTPUT);
  digitalWrite(buzzer,0);
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
    
    if (s=="cmd_buzzer"){
      buzzer_tone();
    }else if (s=="cmd_01_on"){
      digitalWrite(relay01, 1);
    }else if (s=="cmd_01_off"){
      digitalWrite(relay01, 0);
    }else if (s=="cmd_02_on"){
      digitalWrite(relay02, 1);
    }else if (s=="cmd_02_off"){
      digitalWrite(relay02, 0);
    }else if (s=="cmd_03_on"){
      digitalWrite(output01, 1);
    }else if (s=="cmd_03_off"){
      digitalWrite(output01, 0);
    }else if (s=="cmd_04_on"){
      digitalWrite(output02, 1);
    }else if (s=="cmd_04_off"){
      digitalWrite(output02, 0);
    }else{
      buzzer_tone();
    }

    
    
  }  
  delay(1000);
}

void buzzer_tone(){
  tone(buzzer,200);
  delay(500);
  noTone(buzzer);
  
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
