import cv2
import mediapipe as mp
import numpy as np
import json
from LandmarkAngleHelper import LandmarkAngleHelper, Joint

class PoseVisualizer:
    def __init__(self, mode='All'):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.helper = LandmarkAngleHelper()
        self.visibility_threshold = 0.9  # 90% visibility threshold
        self.mode = mode
        self.frame_data = []

    def process_frame(self, frame):
        image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
        results = self.pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            self.helper.set_landmarks(results.pose_landmarks.landmark)
            self.draw_pose(image, results.pose_landmarks)
            left_visibility, right_visibility = self.calculate_side_visibility(results.pose_landmarks)
            self.draw_visibility_diagram(image, left_visibility, right_visibility)
            angles = self.draw_angles(image, left_visibility, right_visibility)
            self.save_frame_data(angles)

        return image

    def draw_angles(self, image, left_visibility, right_visibility):
        show_left = left_visibility >= self.visibility_threshold * right_visibility
        show_right = right_visibility >= self.visibility_threshold * left_visibility

        angles = {}
        if self.mode == 'Squat':
            if show_left:
                angles.update({
                    # 'LeftShoulder': self.helper.left_shoulder_angle(),
                    'LeftKnee': self.helper.left_knee_angle(),
                })
            if show_right:
                angles.update({
                    # 'RightShoulder': self.helper.right_shoulder_angle(),
                    'RightKnee': self.helper.right_knee_angle(),
                })
            angles['Hip'] = self.helper.hip_angle()
        else:  # 'All' mode
            if show_left:
                angles.update({
                    'LeftElbow': self.helper.left_elbow_angle(),
                    'LeftKnee': self.helper.left_knee_angle(),
                    'LeftShoulder': self.helper.left_shoulder_angle(),
                })
            if show_right:
                angles.update({
                    'RightElbow': self.helper.right_elbow_angle(),
                    'RightKnee': self.helper.right_knee_angle(),
                    'RightShoulder': self.helper.right_shoulder_angle(),
                })
            angles['Hip'] = self.helper.hip_angle()

        for joint, angle in angles.items():
            if angle is not None:
                # Use the correct method names for coordinates
                if joint == 'LeftShoulder':
                    position = self.helper.left_shoulder_coord(image.shape[1], image.shape[0])
                elif joint == 'RightShoulder':
                    position = self.helper.right_shoulder_coord(image.shape[1], image.shape[0])
                elif joint == 'LeftKnee':
                    position = self.helper.left_knee_coord(image.shape[1], image.shape[0])
                elif joint == 'RightKnee':
                    position = self.helper.right_knee_coord(image.shape[1], image.shape[0])
                elif joint == 'LeftElbow':
                    position = self.helper.left_elbow_coord(image.shape[1], image.shape[0])
                elif joint == 'RightElbow':
                    position = self.helper.right_elbow_coord(image.shape[1], image.shape[0])
                elif joint == 'Hip':
                    position = self.helper.hip_coord(image.shape[1], image.shape[0])
                else:
                    continue  # Skip if we don't have a coordinate method for this joint

                self.draw_angle(image, angle, (int(position[0]), int(position[1])))

        return angles

    def save_frame_data(self, angles):
        self.frame_data.append(angles)

    def save_to_json(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.frame_data, f, indent=2)

    def draw_pose(self, image, landmarks):
        self.mp_drawing.draw_landmarks(image, landmarks, self.mp_pose.POSE_CONNECTIONS)

    def calculate_side_visibility(self, landmarks):
        left_joints = [11, 13, 15, 23, 25, 27]  # Left shoulder, elbow, wrist, hip, knee, ankle
        right_joints = [12, 14, 16, 24, 26, 28]  # Right shoulder, elbow, wrist, hip, knee, ankle

        left_visibility = sum(landmarks.landmark[i].visibility for i in left_joints)
        right_visibility = sum(landmarks.landmark[i].visibility for i in right_joints)

        # Normalize visibility (0 to 1)
        max_visibility = max(left_visibility, right_visibility)
        left_visibility = left_visibility / max_visibility if max_visibility > 0 else 0
        right_visibility = right_visibility / max_visibility if max_visibility > 0 else 0

        return left_visibility, right_visibility
        
        # Always show hip angle
        angles[Joint.Hip] = (self.helper.hip_angle, self.helper.hip_coord)

        for joint, (angle_func, coord_func) in angles.items():
            angle = angle_func()
            if angle is not None:
                position = coord_func(image.shape[1], image.shape[0])
                self.draw_angle(image, angle, (int(position[0]), int(position[1])))

    @staticmethod
    def draw_angle(image, angle, position, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1.0, color=(255, 255, 255), thickness=2):
        cv2.putText(image, f"{angle:.1f}", position, font, font_scale, color, thickness)

    def draw_visibility_diagram(self, image, left_visibility, right_visibility):
        height, width, _ = image.shape
        diagram_width, diagram_height = 200, 100
        x, y = width - diagram_width - 10, height - diagram_height - 10

        cv2.rectangle(image, (x, y), (x + diagram_width, y + diagram_height), (0, 0, 0), -1)
        cv2.rectangle(image, (x, y), (x + diagram_width, y + diagram_height), (255, 255, 255), 2)

        bar_height = 30
        bar_y = y + (diagram_height - bar_height * 2) // 3

        # Left side bar
        cv2.rectangle(image, (x + 10, bar_y), (x + 190, bar_y + bar_height), (0, 255, 0), 2)
        cv2.rectangle(image, (x + 10, bar_y), (x + 10 + int(180 * left_visibility), bar_y + bar_height), (0, 255, 0), -1)
        cv2.putText(image, f"Left: {left_visibility:.2f}", (x + 10, bar_y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Right side bar
        cv2.rectangle(image, (x + 10, bar_y + bar_height + 10), (x + 190, bar_y + bar_height * 2 + 10), (0, 0, 255), 2)
        cv2.rectangle(image, (x + 10, bar_y + bar_height + 10), (x + 10 + int(180 * right_visibility), bar_y + bar_height * 2 + 10), (0, 0, 255), -1)
        cv2.putText(image, f"Right: {right_visibility:.2f}", (x + 10, bar_y + bar_height * 2 + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

class StreamHandler:
    def __init__(self):
        self.stream = None

    def load_stream(self, source, path=None):
        if self.stream is not None:
            self.stream.release()

        if source == "camera":
            self.stream = cv2.VideoCapture(0)
        elif source == "recording" and path is not None:
            self.stream = cv2.VideoCapture(path)
        else:
            raise ValueError("Invalid source or missing path for recording")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.stream is not None:
            self.stream.release()

    def get_frame(self):
        if self.stream is None:
            raise ValueError("No stream loaded. Call load_stream first.")
        success, frame = self.stream.read()
        if not success:
            return None
        return frame

def main():
    # Get user input for mode
    while True:
        mode = input("Select mode (1 for Squat, 2 for All): ")
        if mode == '1':
            mode = 'Squat'
            break
        elif mode == '2':
            mode = 'All'
            break
        else:
            print("Invalid input. Please enter 1 or 2.")

    visualizer = PoseVisualizer(mode)
    stream_handler = StreamHandler()

    # Choose your input source here
    # stream_handler.load_stream("camera")
    stream_handler.load_stream("recording", "videos/side_squat.mp4")

    frame_count = 0
    with stream_handler:
        while True:
            frame = stream_handler.get_frame()
            if frame is None:
                break

            processed_frame = visualizer.process_frame(frame)
            cv2.imshow('MediaPipe Pose', processed_frame)

            frame_count += 1
            if frame_count % 100 == 0:
                print(f"Processed {frame_count} frames")

            if cv2.waitKey(5) & 0xFF == 27:  # Exit on ESC
                break

    cv2.destroyAllWindows()

    # Save the collected data to a JSON file
    visualizer.save_to_json(f"{mode.lower()}_angles.json")
    print(f"Angle data saved to {mode.lower()}_angles.json")

if __name__ == "__main__":
    main()