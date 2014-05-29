/*     
      Plant Notes - Arduino sensor board transmitter

      Sensor data of soil moisture, light intensity, rain intensity, temperature and humidity are sent via RF24 transceiver
      to Raspberry Pi to be recieved.

      The sensor pins:

      *   Moisture probe - analog pin 2
      *   Rain sensor - analog pin 1
      *   LDR - analog pin 0
      *   DHT11 humidity and temperature sensor - digital pin 4

      Created: 21/12/2013
      Last Edited: 28/05/14

      Author: Gabriel Barnes, Jake Malley

      http://www.plantnotes.co.uk

  */
#include <SPI.h>              
#include <RF24.h>
#include <DHT22.h> 

int ldrPin = A0;               
int rainPin = A1;               
int moistPin = A2;
int dhtPin = 7;
DHT22 myDHT22(dhtPin);
int tempPin = (float)myDHT22.getTemperatureC();
int huePin = (float)myDHT22.getHumidity();
RF24 radio(9,10);          


void setup()
{
  Serial.begin(9600); 
  radio_start(0x4c);
}

void loop()
{     
  sensor_write(moistPin,"mos0");  
  sensor_write(rainPin,"ran0");
  sensor_write(ldrPin,"lis0");
  write_data(String("hue0" + huePin));
  write_data(String("temp0" + tempPin));
}

void radio_start(int channel)
{   
  radio.begin();              
  radio.setPALevel(RF24_PA_MAX);
  radio.setChannel(76);
  radio.openWritingPipe(0xF0F0F0F0E1LL);
  radio.enableDynamicPayloads();
  radio.powerUp();
}

void sensor_write(int sensor, String prefix)
{                                          
  map(sensor,0,1023,0,1023);
  String sensor_out = prefix + String(analogRead(sensor),DEC);
  write_data(sensor_out);
  delay(5000);
}

void write_data(String data)
{                          
  char outBuffer[32]= "";                            //Create the char 'outBuffer' allowing a max payload of 32 characters
  data.toCharArray(outBuffer, 32);                   //Convert string message to the char array of outBuffer
  radio.write(outBuffer, strlen(outBuffer));         //Transmit outBuffer
  Serial.println(data);                              //Serial print data (debug)
}





