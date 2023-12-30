# LEDarcade64
 A collection of classes and functions for animated text and graphics on an Adafruit LED Matrix.

This version is a fork of the original LEDarcade from DATAGOD, but it adds new functionalities and adapt it for a 64x64 RGB LED Matrix.
In my particular case I'm using two chained 64x64 panels to reach a 128x64 total Matrix.

## What it can do
LEDArcade has many classes, functions, pre-defined sprites that are used to do the following:

- draw a sprite
- move a sprite
- make a sprite float across the screen
- raw animated sprites floating across the screen
- draw text of multiple sizes
- scroll text left or right at various speeds
- multiple ways to clear the screen (zooming in / zooming out / fading)
- scroll the screen around a large map, displaying only a section of the map in a window

## Requirements
<BR>Raspberry Pi 3 and up
<BR>Adafruit LED Matrix (64x32)
<BR>Adafruit RGB Hat
<BR>hzeller's RBG LED Matrix code: https://github.com/hzeller/rpi-rgb-led-matrix


## Usage
Modify the test.py script to contain the messages you want to display.  Then execute by issuing the comand:
 ~~~
 sudo python3 test.py
 ~~~
 
 ## Retro Arcade Games
 There are 5 old school arcade games you can play on your LED Matrix:
 
~~~
sudo python3 DotInvaders.py
sudo python3 Defender.py
sudo python3 Outbreak.py
sudo python3 SpaceDot.py
sudo python3 Tron.py
~~~
 
 ## Rotating Arcade Games
 Run the following to put your clock into a mode that will cycle through all the available games.
 
 ~~~
 sudo python3 arcade.py
 ~~~

 ## Flight LED panel
 My favorite: Displays the closest aircraft to specified coordinates and shows all of its data and info using FlightRadar24 API.
 Edit _FlightConfig.ini_ to set some necessary parameters.
 
 KEYBOARD SHORTCUTS:  
'U' - Update Flights list  
'N' - Show Next Flight in the list  

 ~~~
 sudo python3 flight.py
 ~~~
