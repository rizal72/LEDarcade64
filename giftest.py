
import os
os.system('cls||clear')

import time
import sys

import LEDarcade as LED
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix, RGBMatrixOptions


LED.TheMatrix.brightness = 50
print("GIF TEST")

while(1==1):
  LED.TheMatrix.Clear()

  
  LED.DisplayGIF('./images/policefist.gif',128,64,6,0.06)
  LED.DisplayGIF('./images/storm.gif',128,64,6,0.06)
  LED.DisplayGIF('./images/minioncrying2.gif',128,64,2,0.06)
  LED.DisplayGIF('./images/minioneyes.gif',128,64,6,0.06)
  LED.DisplayGIF('./images/minionredalert.gif',128,64,6,0.06)
  LED.TheMatrix.Clear()
  LED.DisplayGIF('./images/marioprincesskiss.gif',64,64,1,0.06)
  
  LED.TheMatrix.Clear()
  LED.DisplayGIF('./images/samusbounce.gif',64,64,15,0.09)
  LED.DisplayGIF('./images/minions.gif',128,64,15,0.06)
  LED.TheMatrix.Clear()
  LED.DisplayGIF('./images/samus.gif',64,64,20,0.06)
  
  LED.DisplayGIF('./images/homer_marge2.gif',128,64,5,0.04)
  LED.DisplayGIF('./images/runningman2.gif',128,64,1,0.04)
  LED.DisplayGIF('./images/arcade1.gif',128,64,25,0.12)
  LED.DisplayGIF('./images/arcade2.gif',128,64,25,0.12)
  LED.TheMatrix.Clear()
  LED.DisplayGIF('./images/mario.gif',64,64,15,0.05)
  LED.DisplayGIF('./images/homer_marge.gif',128,64,5,0.04)
  LED.DisplayGIF('./images/fishburger.gif',128,64,2,0.04)
  LED.TheMatrix.Clear()
  LED.DisplayGIF('./images/ghosts.gif',128,64,10,0.04)



print("TEST COMPLETE")



