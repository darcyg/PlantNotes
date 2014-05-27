	
/*    
      Plant Pi - Arduino ATMEGA328P-PU Code
 
      Sensor data of soil moisture, light intensity, rain intensity, temperature and humidity are sent via RF24 transceiver
      to Raspberry Pi to be recieved.
 
      The sensor pins:
 
      *   Moisture probe - analog pin 2
      *   Rain sensor - analog pin 1
      *   LDR - analog pin 0
      *   DHT11 humidity and temperature sensor - digital pin 4
 
      RF24 circuit:
      *   Digital Pin 09 - Transmitter CE
      *   Digital Pin 10 - Transmitter CSN
      *   Digital Pin 11 - Transmitter MOSI
      *   Digital Pin 12 - Transmitter MISO
      *   Digital Pin 13 - Transmitter SCK
 
      Created: 21/12/2013
      Last Edited: 29/03/14
 
      Authors: Gabriel Barnes, Jake Malley
 
      http://www.plantpi.gabrielbarnes.co.uk
 
  */
  #include <dht11.h>   //include DHT11 libary, for the humidity and temperature sensor (DHT11)
  #include <SPI.h>     //include SPI libary, allowing for communication between devices              
  #include <RF24.h>    //include the RF24 radio transceiver libary                
 
  int ldrPin = A0;     //LDR to pin analog pin 0                
  int rainPin = A1;    //Rain sensor to pin analog pin 1            
  int moistPin = A2;   //Moisture sensor to analog pin 2            
  int dht11Pin = 4;    //DHT11 sensor to digital pin 4
  dht11 DHT11;
  RF24 radio(9,10);    //RF24 radio transceiver using digital pin 9 and 10          
  String message;      
  int tempPin = (float)DHT11.temperature;
  int humiPin = (float)DHT11.humidity;
 
void setup()
{
  Serial.begin(9600);  //Begin the serial port at 9600 baud (serial port used for debugging)      
  radio_start(0x4c);     //call the radio to setup
}
void loop()
{    
  sensor_write(moistPin,"mos0",A2);  
  sensor_write(rainPin,"ran0",A1);
  sensor_write(ldrPin,"lis0",A0);
  dht_write(tempPin,"tmp0");
  dht_write(humiPin,"hue0");
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
void sensor_write(int sensor, String prefix, int sensor_id)
{                                          
  map(sensor,0,1023,0,1023);
  String sensor_out = prefix + String(analogRead(sensor_id),DEC);
  write_data(sensor_out);
  delay(5000);
}
void dht_write(int sensor, String prefix)
{                                          
  map(sensor,0,1023,0,1023);
  String sensor_out = prefix + sensor;
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

