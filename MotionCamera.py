from gpiozero import LED
from gpiozero import MotionSensor
from picamera import PiCamera
import datetime
import boto3
import time
import smtplib
import json
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

#email credentials
me = "insertyouremailhere"
my_password = r"insertyouremailpasswordhere"
you = "insertemailtosendpictureandtag"

#msg = MIMEMultipart('alternative')
'''
msg['Subject'] = "Alert Motion Detected!"
msg['From'] = me
msg['To'] = you
'''

s3 = boto3.client('s3')
#s3.upload_file('/home/pi/Desktop/PiCam/test.jpeg','picameracapture',timestamp_string)
rekog = boto3.client('rekognition')
#creates client for AWS rekognition

#Setup for email


camera = PiCamera()

camera.start_preview() #min 2 seconds before able to use camera
time.sleep(5)

#camera.capture("test.jpg")

green_led = LED(17)
pir = MotionSensor(4)
green_led.off()

while True:
        pir.wait_for_motion()
        print("Motion Detected")
        green_led.on()
        camera.capture("test.jpeg")
        timestamp = datetime.datetime.now()
        timestamp_string = timestamp.strftime("%y %m %d %H:%M:%S.jpeg")
        s3.upload_file('/home/pi/Desktop/PiCam/test.jpeg','picameracapture',timestamp_string)
        #uploads to AWS s3 bucket with times instead of "test.jpg"
        photo = timestamp_string

        fileObj = s3.get_object(Bucket = "picameracapture", Key = photo)
        file_content = fileObj["Body"].read()
        response = rekog.detect_labels(Image = {"S3Object": {"Bucket": "picameracapture","Name":photo}}, MaxLabels=1,MinConfidence=70)
        msg_json = json.dumps(response)

        msg = MIMEMultipart()
        text = MIMEText(msg_json)
        msg.attach(text)
        image = MIMEImage(file_content)
        msg.attach(image)
        msg['Subject'] = "Alert Motion Detected!"
        msg['From'] = me
        msg['To'] = you
        s = smtplib.SMTP_SSL('smtp.gmail.com')
        s.login(me,my_password)
        s.sendmail(me,you,str(msg))
        s.quit()

        pir.wait_for_no_motion()
        green_led.off()
        print("Motion Stopped")
