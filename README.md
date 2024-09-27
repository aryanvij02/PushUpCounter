# PushUpCounter
A simple program using Mediapipe and OpenCV to count the number of Push Ups done. The main goal is to ensure proper form while doing Push Ups so as to achieve maximum effect. 

You may use the BasicPoseModule in your personal projects, changing the variables as necessary. The Pose Module is using mediapipe's Pose module. Refer to the image below for the different joints in the body that are detected.

![alt text](https://google.github.io/mediapipe/images/mobile/pose_tracking_full_body_landmarks.png)

Proper Push-ups
---

I love reading the Hacker News site. Amazing projects & discussions. 

Recently there was a link to https://aryanvij02.medium.com/push-ups-with-python-mediapipe-open-a544bd9b4351

This is exactly the type of project I love to read about there: inspiring, smart, fun. 

This is the script from that blog post. I've refactored it a bit to help my understanding. But all the clever stuff & getting it to work is due to the original 
author:  [Aryan Vij](https://aryanvij02.medium.com/)

[Original Github repo](https://github.com/aryanvij02/PushUpCounter)


Installation & getting started
----
On my mac using Python 3.10
```
pip install -r requirements.txt should work
python PushUpCounter.py
```

To stop: hit 'Q'
