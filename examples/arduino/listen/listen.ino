
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
