						###### Project Info

This code is for an AWS Raspberry Pi smart camera. The device detects motion then takes an image. It uses Amazon Rekognition in order to send an email notification with Image Classification labels using its deep learning technology. The device also uploads the image capture into an S3 bucket with a timestamp image name. 

##### Requirements
- Raspberry Pi 4 w/ WiFi
- PIR motion sensor 
- Raspberry Pi V2 camera

##### Setup
1. Create a S3 bucket on AWS (default settings are valid)

2. Install AWS Command Line Interface on the Raspberry Pi using command: ***pip install awscli*** within the device terminal. When prompted enter your security credentials which can be found within your Identity and Access Managment (IAM) pannel under the "Your Security Credentials" dropdown.

3. Within the **MotionCapture.py** file enter your email credentials found on lines **15-17**

4. Line **51** is the naming convention for the photo upload to S3 Bucket which can be changed to your choosing. *(Using '/ 'can create subfolder within the bucket)*

5. Line **52** change **'/home/pi/Desktop/PiCam/test.jpeg'** to the directory your image is being saved to locally. This is the same folder in which your **MotionCapture.py** file is located. Change **'picameracapture'** within the same line to the name of your S3 bucket. 

##### Raspberry Pi Pin Setup
PIR Sensor Signal Wire - GPIO 4
PIR Sensor Power Wire - 5V power
PIR Sensor Ground Wire - Ground

*Optional*
The code was design to be implemented with a Green LED Diode conncected to GPIO 17 from a breadboard. This is optional and can be ommited from the code if need be. Omit lines 41 & 48 to do so.

**To-Do's**
- Format JSON labels to only display top 1-3 if > than certain confidence threshold. 
- Format EMAIL process to make it cleaner ~include HTML formatting 
- Adjust PIR sensitivity (might need new sensor as cannot be done physically with this model)
