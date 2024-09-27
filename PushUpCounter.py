# import cv2
# import numpy as np
# import PoseModule as pm

# def setup_camera(file_path=None):
#     """Initializes the video capture object."""
#     # If a file_path is provided, open the file. Otherwise, open the default camera.
#     if file_path is not None:
#         return cv2.VideoCapture(file_path)
#     else:
#         return cv2.VideoCapture(0)


# def update_feedback_and_count(elbow, shoulder, hip, direction, count, form):
#     """Determines the feedback message and updates the count based on the angles."""
#     feedback = "Fix Form"
#     if elbow > 160 and shoulder > 40 and hip > 160:
#         form = 1
#     if form == 1:
#         if elbow <= 90 and hip > 160:
#             feedback = "Up"
#             if direction == 0:
#                 count += 0.5
#                 direction = 1
#         elif elbow > 160 and shoulder > 40 and hip > 160:
#             feedback = "Down"
#             if direction == 1:
#                 count += 0.5
#                 direction = 0
#         else:
#             feedback = "Fix Form"
#     return feedback, count, direction, form

# def draw_ui(img, per, bar, count, feedback, form):
#     """Draws the UI elements on the image."""
#     if form == 1:
#         cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
#         cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
#         cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

#     cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
#     cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
    
#     cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
#     cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

# # Update your main function to include the path to your MP4 file
# def main():
#     # Provide the path to your MP4 file here
#     mp4_file_path = '/Users/aryanvij/Downloads/The Perfect Push Up _ Do it right!.mp4'
#     cap = setup_camera(mp4_file_path)
#     detector = pm.poseDetector()
#     count = 0
#     direction = 0
#     form = 0

#     while cap.isOpened():
#         ret, img = cap.read()
#         if not ret:
#             break  # If no frames are returned, stop the loop
#         img = detector.findPose(img, False)
#         lmList = detector.findPosition(img, False)

#         if len(lmList) != 0:
#             elbow = detector.findAngle(img, 11, 13, 15)
#             shoulder = detector.findAngle(img, 13, 11, 23)
#             hip = detector.findAngle(img, 11, 23, 25)
#             per = np.interp(elbow, (90, 160), (0, 100))
#             bar = np.interp(elbow, (90, 160), (380, 50))
#             feedback, count, direction, form = update_feedback_and_count(elbow, shoulder, hip, direction, count, form)
#             draw_ui(img, per, bar, count, feedback, form)
#             print(count)
        
#         cv2.imshow('Pushup Counter', img)
#         if cv2.waitKey(10) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()





import cv2
import numpy as np
import PoseModule as pm

def setup_camera():
    """Initializes the video capture object."""
    return cv2.VideoCapture(0)

def get_video_dimensions(cap):
    """Returns the dimensions of the video frame."""
    width = cap.get(3)  # float `width`
    height = cap.get(4)  # float `height`
    return width, height

def update_feedback_and_count(elbow, shoulder, hip, direction, count, form):
    """Determines the feedback message and updates the count based on the angles."""
    feedback = "Fix Form"
    if elbow > 160 and shoulder > 40 and hip > 160:
        form = 1
    if form == 1:
        if elbow <= 90 and hip > 160:
            feedback = "Up"
            if direction == 0:
                count += 0.5
                direction = 1
        elif elbow > 160 and shoulder > 40 and hip > 160:
            feedback = "Down"
            if direction == 1:
                count += 0.5
                direction = 0
        else:
            feedback = "Fix Form"
    return feedback, count, direction, form

def draw_ui(img, per, bar, count, feedback, form):
    """Draws the UI elements on the image."""
    if form == 1:
        cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
        cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
    
    cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
    cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

def main():
    cap = setup_camera()
    detector = pm.poseDetector()
    count = 0
    direction = 0
    form = 0

    while cap.isOpened():
        ret, img = cap.read()
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)

        if len(lmList) != 0:
            elbow = detector.findAngle(img, 11, 13, 15)
            shoulder = detector.findAngle(img, 13, 11, 23)
            hip = detector.findAngle(img, 11, 23, 25)
            per = np.interp(elbow, (90, 160), (0, 100))
            bar = np.interp(elbow, (90, 160), (380, 50))
            feedback, count, direction, form = update_feedback_and_count(elbow, shoulder, hip, direction, count, form)
            draw_ui(img, per, bar, count, feedback, form)
            print(count)
        
        cv2.imshow('Pushup Counter', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


import cv2
import numpy as np
import PoseModule as pm
from enum import Enum


class Status(Enum):
    NOT_STARTED = 0
    STARTED = 1


LEFT_KNEE = 25
LEFT_HIP = 23
LEFT_WRIST = 15
LEFT_ELBOW = 13
LEFT_SHOULDER = 11

cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
count = 0
up_direction = True
feedback = "Fix Form"


def in_start_pose():
    return elbow_angle > 160 and shoulder_angle > 40 and hip_angle > 160


def draw_bar():
    cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
    cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(percent_pushup)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)


def draw_counter():
    # Pushup counter
    cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)


def draw_feedback_msg():
    # Feedback
    cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
    cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)


def get_elbow_angle_range_as_a_percentage():
    return np.interp(elbow_angle, (90, 160), (0, 100))


def get_elbow_angle_range_as_score():
    return np.interp(elbow_angle, (90, 160), (380, 50))


def is_pushup_accurate():
    return elbow_angle <= 90 and hip_angle > 160


def is_pushup_started():
    return percent_pushup == 0


def is_pushup_completed():
    return percent_pushup == 100


def can_we_detect_any_pose(lmList):
    return len(lmList) != 0


def change_direction():
    return not up_direction


def increment_score(count):
    count += 0.5
    return count


def check_for_user_quits():
    if cv2.waitKey(10) & 0xFF == ord('q'):
        raise InterruptedError()


def clean_up():
    cap.release()
    cv2.destroyAllWindows()


while cap.isOpened():
    ret, img = cap.read()  # 640 x 480
    width, height = cap.get(3), cap.get(4)
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    if can_we_detect_any_pose(lmList):
        elbow_angle = detector.findAngle(img, LEFT_SHOULDER, LEFT_ELBOW, LEFT_WRIST)
        shoulder_angle = detector.findAngle(img, LEFT_ELBOW, LEFT_SHOULDER, LEFT_HIP)
        hip_angle = detector.findAngle(img, LEFT_SHOULDER, LEFT_HIP, LEFT_KNEE)
        # Percentage of success of pushup
        percent_pushup: int = get_elbow_angle_range_as_a_percentage()
        # Bar to show Pushup progress
        bar: int = get_elbow_angle_range_as_score()
        # Check to ensure right form before starting the program
        form: Status = Status.STARTED if in_start_pose() else Status.NOT_STARTED
        # Check for full range of motion for the pushup
        if form == Status.STARTED:
            if is_pushup_started():
                if is_pushup_accurate():
                    feedback = "Up"
                    change_direction()
                    count = increment_score(count)
                else:
                    feedback = "Fix Form"
            if is_pushup_completed():
                if in_start_pose():
                    feedback = "Down"
                    change_direction()
                    count = increment_score(count)
                else:
                    feedback = "Fix Form"
        print(count)
        # Draw Bar
        if form == Status.STARTED:
            draw_bar()
        draw_counter()
        draw_feedback_msg()

    cv2.imshow('Pushup counter', img)
    check_for_user_quits()

clean_up()
