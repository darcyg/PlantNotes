PlantNotes - Raspberry Pi
==========


Downloading the necessary packages
----------------------------------
Get the packages you need ```sudo apt-get update``` Followed by ```sudo apt-get install build-essentials python2-dev ic2-tools```. However you may need to install ```python2.7-dev``` or ```python3.3-dev``` (Depending on which version of python you intend to use. We've tested it with python 2.7 although jonathongrigg has used python 3.3)

Then add the user ```pi``` to the group ```i2c``` with the command ```sudo adduser pi i2c```.

Allow use of SPI
----------------
To allow us to use the SPI bus on the Pi we must comment out the following lines in the ```/etc/modprobe.d/raspi-blacklist.conf``` file. Firstly open it with ```sudo nano /etc/modprobe.d/raspi-blacklist.conf``` and comment out the two lines ```spi-bcm2708``` and ```i2c-bcm2708```.

Reboot
------
Reboot your Pi ```sudo reboot```.

Installing Cython
-----------------
First download the cython files or clone from GitHub ```git clone https://github.com/cython/cython```
From the downloaded cython folder (once extracted if you downloaded it from their website) run ```python setup.py install``` or ```python3 setup.py install``` for python 3 users (It may take a while so be patient). 
Build librf24
-------------
Change directory to ```librf24```, then ```make``` followed by ```sudo make install```.

Build pyRF24
------------
Change directory to ```pyRF24```, then ```sudo python setup.py build_ext --inplace``` or for python 3 ```sudo python3 setup.py build_ext --inplace```

Using pyRf24
------------
To use the pyRF24 library ```from pyRF24 import pyRF24```. Look through the examples for details on how to send / receive.
Make sure to run programs as root or with sudo.


