#!/usr/bin/python
# PlantNotes.py
# Author: Jake Malley
# 27/05/14
#
# LCD Modules
#
# Based on work from:
# Author : Matt Hawkins
# Site   : http://www.raspberrypi-spy.co.uk
#

# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V
# 16: LCD Backlight GND

# Imports
import RPi.GPIO as GPIO
import time

# LCD Class
class LCD(object):
"""
Class for displaying text to HD44780 LCD display.
"""

    # Device constants.
    LCD_WIDTH = 16
    LCD_CHR = True
    LCD_CMD = False

    LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
    LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line 

    # Timing constants
    E_PULSE = 0.00005
    E_DELAY = 0.00005


    def __init__(self, rs_pin=23, e_pin=24, data_pins=(4,17,27,22)):
        """Constructor."""
        
        # Setup Pin values.
        self.LCD_RS = rs_pin
        self.LCD_E = e_pin
        
        self.LCD_D4 = data_pins[0]
        self.LCD_D5 = data_pins[1]
        self.LCD_D6 = data_pins[2]
        self.LCD_D7 = data_pins[3]
        
        GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
        GPIO.setup(self.LCD_E, GPIO.OUT)  # E
        GPIO.setup(self.LCD_RS, GPIO.OUT) # RS
        GPIO.setup(self.LCD_D4, GPIO.OUT) # DB4
        GPIO.setup(self.LCD_D5, GPIO.OUT) # DB5
        GPIO.setup(self.LCD_D6, GPIO.OUT) # DB6
        GPIO.setup(self.LCD_D7, GPIO.OUT) # DB7
        
        self.__setup__()
        
    def display(line1 = None, line2 = None):
        """Updates text to display."""
        
        if not line1 == None:
            self.__byte__(self.LCD_LINE_1, self.LCD_CMD)
            self.__string__(line1)
        if not line2 == None:
            self.__byte__(self.LCD_LINE_2, self.LCD_CMD)
            self.__string__(line2)

    # Private Methods.
    def __byte__(bits, mode):
        """
        Send byte to data pins
        bits = data
        mode = True  for character
               False for command
        """

        GPIO.output(self.LCD_RS, mode) # RS

        # High bits
        GPIO.output(self.LCD_D4, False)
        GPIO.output(self.LCD_D5, False)
        GPIO.output(self.LCD_D6, False)
        GPIO.output(self.LCD_D7, False)
        if bits&0x10==0x10:
            GPIO.output(self.LCD_D4, True)
        if bits&0x20==0x20:
            GPIO.output(self.LCD_D5, True)
        if bits&0x40==0x40:
            GPIO.output(self.LCD_D6, True)
        if bits&0x80==0x80:
            GPIO.output(self.LCD_D7, True)

        # Toggle 'Enable' pin
        time.sleep(self.E_DELAY)    
        GPIO.output(self.LCD_E, True)  
        time.sleep(self.E_PULSE)
        GPIO.output(self.LCD_E, False)  
        time.sleep(self.E_DELAY)      

        # Low bits
        GPIO.output(self.LCD_D4, False)
        GPIO.output(self.LCD_D5, False)
        GPIO.output(self.LCD_D6, False)
        GPIO.output(self.LCD_D7, False)
        if bits&0x01==0x01:
            GPIO.output(self.LCD_D4, True)
        if bits&0x02==0x02:
            GPIO.output(self.LCD_D5, True)
        if bits&0x04==0x04:
            GPIO.output(self.LCD_D6, True)
        if bits&0x08==0x08:
            GPIO.output(self.LCD_D7, True)

        # Toggle 'Enable' pin
        time.sleep(self.E_DELAY)    
        GPIO.output(self.LCD_E, True)  
        time.sleep(self.E_PULSE)
        GPIO.output(self.LCD_E, False)  
        time.sleep(self.E_DELAY)
    
    def __string__(message):
        """Send string to display."""
        message = message.ljust(self.LCD_WIDTH," ")  

        for i in range(self.LCD_WIDTH):
            self.__byte__(ord(message[i]),self.LCD_CHR)
            
    def __setup__():
        """Initialise display."""
        self.__byte__(0x33,self.LCD_CMD)
        self.__byte__(0x32,self.LCD_CMD)
        self.__byte__(0x28,self.LCD_CMD)
        self.__byte__(0x0C,self.LCD_CMD)  
        self.__byte__(0x06,self.LCD_CMD)
        self.__byte__(0x01,self.LCD_CMD)  

		
if __name__ == "__main__":
    LCD_DISPLAY = LCD()
    LCD_DISPLAY.display("Hello", "World")

