import math
from enum import Enum

class Joint(Enum):
    LeftElbow = "LeftElbow"
    RightElbow = "RightElbow"
    Hip = "Hip"
    LeftKnee = "LeftKnee"
    RightKnee = "RightKnee"
    RightShoulder = "RightShoulder"
    LeftShoulder = "LeftShoulder"
    Elbow = "Elbow"
    Knee = "Knee"
    Shoulder = "Shoulder"

def landmark_angle(a, b, c):
    # Vector from b to a
    ba = {"x": a.x - b.x, "y": a.y - b.y}
    # Vector from b to c
    bc = {"x": c.x - b.x, "y": c.y - b.y}

    # Calculate the angle using dot product and cross product
    dot_product = ba["x"] * bc["x"] + ba["y"] * bc["y"]
    cross_product = ba["x"] * bc["y"] - ba["y"] * bc["x"]
    
    angle = math.atan2(cross_product, dot_product)
    deg = math.degrees(angle)
    if deg < 0:
        deg = -deg
    return normalize_angle(deg, 0, 360)

def normalize_angle(value, start=0, end=360):
    width = end - start
    offset_value = value - start
    print("This is value", value)
    return (offset_value - (math.floor(offset_value / width) * width)) + start

class LandmarkAngleHelper:
    def __init__(self):
        self.landmarks = []
        self.visibility_threshold = 0.1

    def set_landmarks(self, landmarks):
        self.landmarks = landmarks

    def check_visibility(self, indices):
        return all((self.landmarks[i].visibility or 0) >= self.visibility_threshold for i in indices)

    def calculate_angle(self, a_index, b_index, c_index):
        if not self.check_visibility([a_index, b_index, c_index]):
            return None
        a, b, c = self.landmarks[a_index], self.landmarks[b_index], self.landmarks[c_index]
        return landmark_angle(a, b, c)

    def left_elbow_angle(self):
        return self.calculate_angle(11, 13, 15)  # shoulder, elbow, wrist

    def right_elbow_angle(self):
        return self.calculate_angle(12, 14, 16)  # shoulder, elbow, wrist

    def hip_angle(self):
        if (self.landmarks[12].visibility or 0) > (self.landmarks[11].visibility or 0):
            return self.calculate_angle(12, 24, 26)  # right shoulder, right hip, right knee
        else:
            return self.calculate_angle(11, 23, 25)  # left shoulder, left hip, left knee

    def right_knee_angle(self):
        return self.calculate_angle(24, 26, 28)  # hip, knee, ankle

    def left_knee_angle(self):
        return self.calculate_angle(23, 25, 27)  # hip, knee, ankle

    def left_shoulder_angle(self):
        return self.calculate_angle(13, 11, 23)  # elbow, shoulder, hip

    def right_shoulder_angle(self):
        return self.calculate_angle(14, 12, 24)  # elbow, shoulder, hip

    # Coordinate methods remain unchanged
    def right_elbow_coord(self, width, height):
        return (self.landmarks[14].x * width, self.landmarks[14].y * height)

    def left_elbow_coord(self, width, height):
        return (self.landmarks[13].x * width, self.landmarks[13].y * height)

    def hip_coord(self, width, height):
        if (self.landmarks[12].visibility or 0) > (self.landmarks[11].visibility or 0):
            return (self.landmarks[24].x * width, self.landmarks[24].y * height)
        else:
            return (self.landmarks[23].x * width, self.landmarks[23].y * height)

    def right_knee_coord(self, width, height):
        return (self.landmarks[26].x * width, self.landmarks[26].y * height)

    def left_knee_coord(self, width, height):
        return (self.landmarks[25].x * width, self.landmarks[25].y * height)

    def left_shoulder_coord(self, width, height):
        return (self.landmarks[11].x * width, self.landmarks[11].y * height)

    def right_shoulder_coord(self, width, height):
        return (self.landmarks[12].x * width, self.landmarks[12].y * height)