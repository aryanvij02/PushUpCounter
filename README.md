# Push Up Counter
A simple program using Mediapipe and OpenCV to count the number of Push-Ups done. The main goal is to ensure proper form while doing Push-Ups so as to achieve maximum effect.

You may use `base.py`'s `BasePoseDetector` in your personal projects, changing the variables as necessary. The `PoseDetector` class in `pose.py` is using mediapipe's Pose module. Refer to the image below for the different joints in the body that are detected.

![alt text](https://google.github.io/mediapipe/images/mobile/pose_tracking_full_body_landmarks.png)



## Instructions to Run

To set-up the project, go to the current directory and run the following command:
```sh
$ pip install -r requirements.txt
```

Following this, to run, simply run `counter.py` via the following function:
```sh
$ python counter.py
```

Or

```sh
$ py counter.py
```

Depending on the situation.