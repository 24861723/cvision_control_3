"""
CVision Control
Author: Stellenbosch University A.I Society
Website: https://ai-society-su.com/ 

Project Notes for Dev Team:
 
All the commented code is for debugging purposes and can be removed. Below are some
challenge ideas for the dev team to implement. The challenges are optional, but will 
definitely help you learn more about how the code works.

Challenge 1: Implement a bar that shows the brighness level. 
Hint: You can use the same logic as the volume bar. 

Challenge 2: Design a better UI to enhance the user experience.

Remember to have fun and happy coding!

You can reach out to the George Mtombeni, the technical officer at the A.I Society for any questions about the project.

Project Insights:

The HandTrackingModule.py file is a module that is used to detect hands and track the landmarks(24 points) of the hand. 
The codebase uses these detected points and their location on the screen to control the volume and brightness of the system. 
The rectangles and circles drawn on the screen are a way to show the user the current volume and brightness levels. 
"""

import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc

def main():
    ################################ 
    wCam, hCam = 640, 480
    ################################

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    pTime = 0

    detector = htm.handDetector(detectionCon=1)

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # volume.GetMasterVolumeLevel()
    
    # get the brightness for the primary monitor
    brightness = sbc.get_brightness(display=0)

    volRange = volume.GetVolumeRange()
    minVol = volRange[0]
    maxVol = volRange[1]
    vol = volRange[1] * (1 / 2)     # default volume percentage (50%)
    volBar = 275
    volPer = 50      # default volume percentage (50%)
    
    brightness_counter = 0      # to prevent spamming brightness
    
    vol_drag_flag = False
    brightness_drag_flag = False
    fingers_touching = False
    
    # motion flags
    vol_ball_moving_flag = False
    brightness_ball_moving_flag = False
    
    vol_ball_x = int(wCam * (2 / 8)) + int(wCam * (2 / 8))      # ball intially drawn at center of bar
    vol_ball_y = int(hCam * (10 / 14))
    vol_ball_radius = 8
    vol_bar_start = (int(wCam * (2 / 8)), vol_ball_y) #pt1
    vol_bar_end = (int(wCam - wCam * (2 / 8)), vol_ball_y) #pt2
    
    
    brightness_ball_x = int(wCam * (2 / 8)) + int(wCam * (2 / 8))      # ball intially drawn at center of bar
    brightness_ball_y = vol_ball_y - 100
    brightness_ball_radius = vol_ball_radius
    brightness_bar_start = (int(wCam * (2 / 8)), brightness_ball_y) #pt1
    brightness_bar_end = (int(wCam - wCam * (2 / 8)), brightness_ball_y) #pt2   
    
    frame_center_x = int(wCam * (3.5 / 8))
    fram_center_y = int(hCam * (1 / 2))
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        
        # if len(lmList[0]) != 0:
            # print(lmList[0][4])        # should thumb coordinate (it does)
                
        # Draw volume bar backround line
        cv2.line(img, vol_bar_start, vol_bar_end, (255, 0, 255), 3)        

        # Draw brightness bar backround line
        cv2.line(img, brightness_bar_start, brightness_bar_end, (255, 0, 255), 3) 
                    
        lmList = lmList[0]
        
        # when hand is on screen
        if len(lmList) != 0:
            # print(lmList[4], lmList[8])

            x1, y1 = lmList[4][1], lmList[4][2]         # thumb
            x2, y2 = lmList[8][1], lmList[8][2]         # index
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2     # midpoint

            # cv2.circle(img, (x1, y1), 8, (255, 0, 0), cv2.FILLED)
            # cv2.circle(img, (x2, y2), 8, (255, 0, 0), cv2.FILLED)
            # cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            # cv2.circle(img, (cx, cy), 8, (255, 0, 0), cv2.FILLED)

            length = math.hypot(x2 - x1, y2 - y1)   # distance between index and thumb
            
            # print(length)

            # Hand range 50 - 300
            # Volume Range -65 - 0

            # vol = np.interp(length, [50, 300], [minVol, maxVol])
            # volBar = np.interp(length, [50, 300], [400, 150])
            # volPer = np.interp(length, [50, 300], [0, 100])
            # print(int(length), vol)
            # volume.SetMasterVolumeLevel(vol, None)
            
            # draw volume bar ball:
            # cv2.circle(img, (vol_ball_x, vol_ball_y), vol_ball_radius, (255, 175, 0), cv2.FILLED)   MAYBE BRING THIS BACK LATER

            if length < 50:
                fingers_touching = True     # user fingers are touching
            else:
                fingers_touching = False
            
            # dragging volume ball
            if (vol_ball_x - 20 <= cx <= vol_ball_x + 20) and (vol_ball_y - 15 <= cy <= vol_ball_y + 15) and length < 50:
                vol_drag_flag = True
            else:
                vol_drag_flag = False
                
            # dragging brightness ball
            if (brightness_ball_x - 20 <= cx <= brightness_ball_x + 20) and (brightness_ball_y - 15 <= cy <= brightness_ball_y + 15) and length < 50:
                brightness_drag_flag = True
            else:
                brightness_drag_flag = False 
            
            if fingers_touching and vol_drag_flag and brightness_drag_flag != True:
                vol_ball_moving_flag = True
                vol_ball_x = cx  # update volume ball x coordindate
                
            elif fingers_touching and brightness_drag_flag and vol_drag_flag != True:
                brightness_ball_moving_flag = True
                brightness_ball_x = cx  # update brightness ball x coordindate

            if vol_ball_moving_flag and fingers_touching and brightness_ball_moving_flag != True:
                vol_ball_x = cx  # keep moving if user is still touching fingers

            if brightness_ball_moving_flag and fingers_touching and vol_ball_moving_flag != True:
                brightness_ball_x = cx  # keep moving if user is still touching fingers
            
            if vol_ball_moving_flag and fingers_touching != True:
                vol_ball_moving_flag = False # user has separated finger

            if brightness_ball_moving_flag and fingers_touching != True:
                brightness_ball_moving_flag = False  # user has separated finger
                
            # enforce ball boundaries
            if brightness_ball_x < brightness_bar_start[0]:
                brightness_ball_x = brightness_bar_start[0]
            elif vol_ball_x < brightness_bar_start[0]:
                vol_ball_x = brightness_bar_start[0]
            if brightness_ball_x > brightness_bar_end[0]:
                brightness_ball_x = brightness_bar_end[0]
            if vol_ball_x > brightness_bar_end[0]:
                vol_ball_x = brightness_bar_end[0] 
                
            
              
            volBar = np.interp(vol_ball_x, [int(wCam * (2 / 8)), int(wCam - wCam * (2 / 8))], [400, 150])
            volPer = np.interp(vol_ball_x, [int(wCam * (2 / 8)), int(wCam - wCam * (2 / 8))], [0, 100])
            vol = np.interp(vol_ball_x, [int(wCam * (2 / 8)), int(wCam - wCam * (2 / 8))], [minVol, maxVol])

            brightnessBar = np.interp(brightness_ball_x, [int(wCam * (2 / 8)), int(wCam - wCam * (2 / 8))], [400, 150])
            brightnessPer = np.interp(brightness_ball_x, [int(wCam * (2 / 8)), int(wCam - wCam * (2 / 8))], [0, 100])
            brightness = np.interp(brightness_ball_x, [int(wCam * (2 / 8)), int(wCam - wCam * (2 / 8))], [0, 100])
            brightness = int(brightness)
            
            # set system volume
            volume.SetMasterVolumeLevel(vol, None)
            
            print(brightness, brightness_counter)
            
            # set master brightness
            if brightness_counter % 2 == 0:   # only set the brightness 3 times per second (avoids spamming brightness)
                sbc.set_brightness(brightness, display=0)
        
            
        # when no hand is on the screen

        cv2.putText(img, 'Volume', (frame_center_x, vol_ball_y - 20), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                    1, (255, 0, 0), 3)

        cv2.putText(img, 'Brightness', (frame_center_x, brightness_ball_y - 20), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                    1, (255, 0, 0), 3)

        if vol_drag_flag:
            cv2.circle(img, (vol_ball_x, vol_ball_y), vol_ball_radius, (0, 255, 0), cv2.FILLED)     # draw green circle while dragging
        
        else :
            cv2.circle(img, (vol_ball_x, vol_ball_y), vol_ball_radius, (255, 175, 0), cv2.FILLED)     # draw blue circle when not dragging


        if brightness_drag_flag:
            cv2.circle(img, (brightness_ball_x, brightness_ball_y), brightness_ball_radius, (0, 255, 0), cv2.FILLED)     # draw green circle while dragging
        
        else :
            cv2.circle(img, (brightness_ball_x, brightness_ball_y), brightness_ball_radius, (255, 175, 0), cv2.FILLED)     # draw blue circle when not dragging
        
        
        # for rectancles: (topx, topy), (botx, boty)
        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                    1, (255, 0, 0), 3)
        cv2.putText(img, 'Volume', (40, 135), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                    1, (255, 0, 0), 3)


        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                    1, (255, 0, 0), 3)

        brightness_counter += 1
        if brightness_counter == 1000:
            brightness_counter = 0
            
        cv2.imshow("Img", img)
        if cv2.waitKey(100) == ord('q'): # updates every 100 ms
            break

    # Release the webcam and destroy all active windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()