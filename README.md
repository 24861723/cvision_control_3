# cvision_control_3
 CVision Control, a program that allows the user to control system brightness and volume using hand gestures. The code is made for members of the Stellenbosch University A.I Society, but is available to the public. All contributions are welcome.


The HandTrackingModule.py file is a module that is used to detect hands and track the landmarks(24 points) of the hand. 
The codebase uses these detected points and their location on the screen to control the volume and brightness of the system. 
The rectangles and circles drawn on the screen are a way to show the user the current volume and brightness levels. 

 The image below shows the current user interface. There are two challenges detailed in the source code, one of which is to improve the user interface.
 
![image](https://github.com/24861723/cvision_control_3/assets/140675599/7e0edb76-ad78-4f7c-b56a-90123ce1810b)


Below are all the project dependencies required to run the code:

1. **OpenCV (cv2)**:
    - Install OpenCV for computer vision:
      ```
      pip install opencv-python
      ```

2. **NumPy**:
    - Install NumPy for numerical computations:
      ```
      pip install numpy
      ```

3. **pycaw**:
    - Install pycaw for audio control on Windows:
      ```
      pip install pycaw
      ```

4. **screen_brightness_control**:
    - Install screen-brightness-control to adjust monitor brightness:
      ```
      pip install screen-brightness-control
      ```
After all dependecies are installed, you can run the gestureControl.py file.

You can reach out me [George Mtombeni](https://www.linkedin.com/in/george-mtombeni-04948b211), the technical officer at the A.I Society, for any questions about the project. Also connect with me on LinkedIn :)
