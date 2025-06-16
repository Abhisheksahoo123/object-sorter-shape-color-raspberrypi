import cv2
import numpy as np
import sys
import sys
from adafruit_servokit import ServoKit
import time
sys.path.append('/usr/lib/python3/dist-packages')
from picamera2 import Picamera2

# Initialize camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)}))
picam2.start()

# Define color ranges in HSV
color_ranges = {
    "Red": [(0, 100, 100), (10, 255, 255)],
    "Green": [(40, 70, 70), (80, 255, 255)],
    "Blue": [(100, 150, 0), (140, 255, 255)],
    "Yellow": [(20, 100, 100), (30, 255, 255)]
}

last_base = 105
last_shoulder = 145
last_arm = 125
last_wrist = 35
last_claw = 140
last_pos=0

# Initialize ServoKit with 16 channels (PCA9685)
kit = ServoKit(channels=16)


# Check if arguments were provided

def move_servo(channel, start_angle, end_angle, step=1, delay=0.1):
    last_value = 0
    if start_angle < end_angle:
        step = abs(step)  # Ensure positive
    else:
        step = -abs(step)  # Ensure negative

    for angle in range(start_angle, end_angle + step, step):
        if 0 <= angle <= 180:
            kit.servo[channel].angle = angle
            print(F"Moving to {angle}")
            time.sleep(delay)
            last_value = angle

    return last_value

def moveTo(pos):
    global last_base,last_shoulder,last_arm,last_wrist,last_claw,last_pos
    
    if(pos == 1):
        base=10
        shoulder=95
        arm=125
        wrist=30
        claw=60

    elif(pos == 5):
        base=10
        shoulder=95
        arm=125
        wrist=30
        claw=140
   
    elif(pos == 2):
        base=55
        shoulder=145
        arm=125
        wrist=30
        claw=140

    elif(pos == 3):
        base=111
        shoulder=145
        arm=125
        wrist=30
        claw=140
        
    elif(pos == 4):
        base=165
        shoulder=145
        arm=125
        wrist=30
        claw=140

    if(last_pos != 1):
    
        print("Last Servo: " + str(last_base))
        move_servo(0,last_base,base,1)
        last_base = base
        move_servo(1,last_shoulder,shoulder,1)
        last_shoulder = shoulder
        move_servo(2,last_arm,arm,1)
        last_arm = arm
        move_servo(3,last_wrist,wrist,1)
        last_wrist = wrist
        move_servo(4,last_claw,claw,1)
        last_claw = claw

    elif(last_pos == 1):
        last_shoulder = move_servo(1,last_shoulder,shoulder,1)
        last_shoulder = shoulder
        last_base = move_servo(0,last_base,base,1)
        last_base = base
        last_arm = move_servo(2,last_arm,arm,1)
        last_arm = arm
        last_wrist = move_servo(3,last_wrist,wrist,1)
        last_wrist = wrist
        last_claw = move_servo(4,last_claw,claw,1)
        last_claw = claw

    last_pos=pos


while True:
    # Capture frame
    frame = picam2.capture_array()

    # Blur and convert to HSV color space
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    for color_name, (lower, upper) in color_ranges.items():
        # Create mask for each color
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 500:  # Ignore tiny blobs
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(frame, color_name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                if(color_name == "Red"):
                  moveTo(1)
                  time.sleep(1)
                  moveTo(2)
                  break;
                
                elif(color_name == "Green"):
        
                  moveTo(1)
                  time.sleep(1)
                  moveTo(3)
                  break;
                
                elif(color_name == "Blue"):
             
                  moveTo(1)
                  time.sleep(1)
                  moveTo(4)
                  break;
                

        
    # Show the frame
    cv2.imshow("LEGO Block Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
