import pygame
import pygame.joystick
from pygame.locals import *

def main():
   pygame.init()
   print(pygame.joystick.get_count())
   j = pygame.joystick.Joystick(0)
   j.init()
   while(True):
      events = pygame.event.get()
      for e in events:
         try:
            x = e.axis
            if x is not None:
               if not x == 2:
                  print("%s" % e)
         except Exception as ex:
            print("%s" % e)

if __name__ == "__main__":
   main()

