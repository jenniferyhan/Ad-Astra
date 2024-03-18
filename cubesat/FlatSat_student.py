"""
The Python code you will write for this module should read
acceleration data from the IMU. When a reading comes in that surpasses
an acceleration threshold (indicating a shake), your Pi should pause,
trigger the camera to take a picture, then save the image with a
descriptive filename. You may use GitHub to upload your images automatically,
but for this activity it is not required.

The provided functions are only for reference, you do not need to use them. 
You will need to complete the take_photo() function and configure the VARIABLES section
"""

#AUTHOR: 
#DATE:


#import libraries
import time
import board
from PIL import Image
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
from git import Repo
from picamera2 import Picamera2, Preview


#VARIABLES
THRESHOLD = 20      #Any desired value from the accelerometer
REPO_PATH = "/home/pi/Ad-Astra"     #Your github repo path: ex. /home/pi/FlatSatChallenge
FOLDER_PATH = "/cubesat"  #Your image folder path in your GitHub repo: ex. /Images

#imu and camera initialization
i2c = board.I2C()
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)
picam2 = Picamera2()


def git_push():
    """
    This function is complete. Stages, commits, and pushes new images to your GitHub repo.
    """
    try:
        repo = Repo(REPO_PATH)
        origin = repo.remote('origin')
        print('added remote')
        origin.pull()
        print('pulled changes')
        repo.git.add(REPO_PATH + FOLDER_PATH)
        repo.index.commit('New Photo')
        print('made the commit')
        origin.push()
        print('pushed changes')
    except:
        print('Couldn\'t upload to git')


def img_gen(name):
    """
    This function is complete. Generates a new image name.

    Parameters:
        name (str): your name ex. MasonM
    """
    t = time.strftime("_%H%M%S")
    imgname = (f'{REPO_PATH}/{FOLDER_PATH}/{name}{t}.jpg')
    return imgname


def take_photo():
    """
    This function is NOT complete. Takes a photo when the FlatSat is shaken.
    Replace psuedocode with your own code.
    """


    while True:
        accelx, accely, accelz = accel_gyro.acceleration
        acceleration = accelx ** 2 + accely ** 2 + accelz ** 2
        magnitude = acceleration ** (1/2)
        

        if magnitude > THRESHOLD:

            picam2.configure(picam2.create_preview_configuration({"format": "RGB888"}))
            min_exp, max_exp, default_exp = picam2.camera_controls["AfPause"]

            name = "bangT"
            photo_name = img_gen(name)
            
            picam2.start()
            time.sleep(3)

            image = picam2.capture_array("main")
            print("picture done")
            return image
            
            
            

            # git_push()

        

        #CHECKS IF READINGS ARE ABOVE THRESHOLD
            #PAUSE
            #name = ""     #First Name, Last Initial  ex. MasonM
            #TAKE PHOTO
            #PUSH PHOTO TO GITHUB
        
        #PAUSE
def process_images(before, after):
    befored = dict()
    befored["Area1"] = 0
    befored["Area2"] = 0
    befored["Area3"] = 0
    befored["Area4"] = 0


    for i in range(len(befored)):
        for j in range(len(befored[0])):
            #area 1
            temp = sum(befored[i][j])
            if i <= 239 and j <= 319:
                befored["Area1"] += 1
            #area2
            elif i > 240 and j <= 319:
                befored["Area2"] += 1
            #area3
            elif i <= 239 and j > 320:
                befored["Area3"] += 1
            #area4
            else:
                befored["Area4"] += 1

    return befored

def main():
    image_before = take_photo()
    image_after = ""

    print(process_images(image_before, image_after))

if __name__ == '__main__':
    # print("Hello World!")
    main()