# PYNQ_Cube
This repository holds all of the necessary files required to run the cube solving application on the pynq board.

demo:
https://www.youtube.com/watch?v=i2_RQxWd3Mc

# Instructions
RGB LED 4 (LD4): Direction to rotate the face of the cube 90 degrees. Green for clockwise. Red for counterclockwise.

RGB LED 5 (LD5): Color of face to rotate. These colors are based on the middle square of each face. Since the color orange is not
                 supported, magenta is used for orange.   
                 This LED flashing indicates that the face should be rotated 180 degrees.

Switch 0 (SW0): Toggle this switch to move through the steps backward from current move.

Switch 1 (SW1): Toggle this switch to move through the steps automatically.

Buttons 0-3 (BTN0-3): Press on a button to move to next step. If moving automatically, pressing a button changes the speed at which the moves
                      are shown. Button 3 is the slowest at 3 seconds per move, followed by 2 seconds, followed by 1 second, followed by half
                      a second at button 0.
                      
LEDs 0-3 (LD0-3): These LEDs show the current progress of the move list. As the user advances through the steps the LEDs light up from 3 to 0.
                  When on the final step, these LEDs flash.
