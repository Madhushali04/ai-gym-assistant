import cv2
import numpy as np
import mediapipe as mp
import os

# New API only - no mp.solutions at all!
BaseOptions           = mp.tasks.BaseOptions
PoseLandmarker        = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode     = mp.tasks.vision.RunningMode

MODEL_PATH = os.path.join(os.path.dirname(__file__), "pose_landmarker.task")

RIGHT_SHOULDER = 12
RIGHT_ELBOW    = 14
RIGHT_WRIST    = 16
RIGHT_HIP      = 24
RIGHT_KNEE     = 26
RIGHT_ANKLE    = 28

CONNECTIONS = [
    (11,12),(11,13),(13,15),(12,14),(14,16),
    (11,23),(12,24),(23,24),(23,25),(25,27),(24,26),(26,28)
]

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

class RepCounter:
    def __init__(self):
        self.count    = 0
        self.stage    = None
        self.feedback = "Get Ready!"

    def reset(self):
        self.count    = 0
        self.stage    = None
        self.feedback = "Get Ready!"

    def count_curl_reps(self, angle):
        if angle > 160:
            self.stage    = "down"
            self.feedback = "Good! Now curl up!"
        if angle < 30 and self.stage == "down":
            self.stage    = "up"
            self.count   += 1
            self.feedback = "Great rep! Keep going!"
        return self.count, self.stage, self.feedback

    def count_squat_reps(self, angle):
        if angle > 160:
            self.stage    = "up"
            self.feedback = "Good! Now squat down!"
        if angle < 90 and self.stage == "up":
            self.stage    = "down"
            self.count   += 1
            self.feedback = "Great squat! Stand back up!"
        return self.count, self.stage, self.feedback
    def count_shoulder_press_reps(self, angle):
        # Start with arms bent (angle < 90) = DOWN
        # Push up until arms straight (angle > 160) = UP
        if angle < 90:
            self.stage    = "down"
            self.feedback = "Good! Now press up!"
        if angle > 160 and self.stage == "down":
            self.stage    = "up"
            self.count   += 1
            self.feedback = "Great press! Bring it back down!"
        return self.count, self.stage, self.feedback

    def count_lateral_raise_reps(self, angle):
        # Arm down by side (angle < 30) = DOWN
        # Arm raised to shoulder height (angle > 80) = UP
        if angle < 30:
            self.stage    = "down"
            self.feedback = "Good! Now raise your arm!"
        if angle > 80 and self.stage == "down":
            self.stage    = "up"
            self.count   += 1
            self.feedback = "Great raise! Bring it back down!"
        return self.count, self.stage, self.feedback

    def count_lunge_reps(self, angle):
        # Standing straight (angle > 160) = UP
        # Knee bent in lunge (angle < 90) = DOWN
        if angle > 160:
            self.stage    = "up"
            self.feedback = "Good! Now lunge down!"
        if angle < 90 and self.stage == "up":
            self.stage    = "down"
            self.count   += 1
            self.feedback = "Great lunge! Stand back up!"
        return self.count, self.stage, self.feedback

    def count_tricep_reps(self, angle):
        # Arm bent behind head (angle < 60) = DOWN
        # Arm extended straight (angle > 150) = UP
        if angle < 60:
            self.stage    = "down"
            self.feedback = "Good! Now extend your arm!"
        if angle > 150 and self.stage == "down":
            self.stage    = "up"
            self.count   += 1
            self.feedback = "Great rep! Bend it back!"
        return self.count, self.stage, self.feedback

def draw_skeleton(frame, landmarks, h, w):
    for start, end in CONNECTIONS:
        sx = int(landmarks[start].x * w)
        sy = int(landmarks[start].y * h)
        ex = int(landmarks[end].x * w)
        ey = int(landmarks[end].y * h)
        cv2.line(frame, (sx, sy), (ex, ey), (0, 255, 0), 2)
    for lm in landmarks:
        cx = int(lm.x * w)
        cy = int(lm.y * h)
        cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

def process_frame(frame, rep_counter, exercise):
    h, w, _ = frame.shape
    rgb     = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_img  = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

    options = PoseLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=VisionRunningMode.IMAGE
    )

    with PoseLandmarker.create_from_options(options) as detector:
        result = detector.detect(mp_img)

        if result.pose_landmarks and len(result.pose_landmarks) > 0:
            lms = result.pose_landmarks[0]

            def pt(idx):
                return [lms[idx].x, lms[idx].y]

            if exercise == "Bicep Curl":
                angle = calculate_angle(pt(RIGHT_SHOULDER), pt(RIGHT_ELBOW), pt(RIGHT_WRIST))
                count, stage, feedback = rep_counter.count_curl_reps(angle)
                jx = int(lms[RIGHT_ELBOW].x * w)
                jy = int(lms[RIGHT_ELBOW].y * h)

            elif exercise == "Squat":
                angle = calculate_angle(pt(RIGHT_HIP), pt(RIGHT_KNEE), pt(RIGHT_ANKLE))
                count, stage, feedback = rep_counter.count_squat_reps(angle)
                jx = int(lms[RIGHT_KNEE].x * w)
                jy = int(lms[RIGHT_KNEE].y * h)

            elif exercise == "Shoulder Press":
                angle = calculate_angle(pt(RIGHT_SHOULDER), pt(RIGHT_ELBOW), pt(RIGHT_WRIST))
                count, stage, feedback = rep_counter.count_shoulder_press_reps(angle)
                jx = int(lms[RIGHT_ELBOW].x * w)
                jy = int(lms[RIGHT_ELBOW].y * h)

            elif exercise == "Lateral Raise":
                # Measure angle at shoulder using hip-shoulder-elbow
                angle = calculate_angle(pt(RIGHT_HIP), pt(RIGHT_SHOULDER), pt(RIGHT_ELBOW))
                count, stage, feedback = rep_counter.count_lateral_raise_reps(angle)
                jx = int(lms[RIGHT_SHOULDER].x * w)
                jy = int(lms[RIGHT_SHOULDER].y * h)

            elif exercise == "Lunge":
                angle = calculate_angle(pt(RIGHT_HIP), pt(RIGHT_KNEE), pt(RIGHT_ANKLE))
                count, stage, feedback = rep_counter.count_lunge_reps(angle)
                jx = int(lms[RIGHT_KNEE].x * w)
                jy = int(lms[RIGHT_KNEE].y * h)

            elif exercise == "Tricep Extension":
                angle = calculate_angle(pt(RIGHT_SHOULDER), pt(RIGHT_ELBOW), pt(RIGHT_WRIST))
                count, stage, feedback = rep_counter.count_tricep_reps(angle)
                jx = int(lms[RIGHT_ELBOW].x * w)
                jy = int(lms[RIGHT_ELBOW].y * h)

            else:
                angle = 0
                count, stage, feedback = rep_counter.count, rep_counter.stage, rep_counter.feedback
                jx, jy = 0, 0

            draw_skeleton(frame, lms, h, w)

            cv2.putText(frame, str(int(angle)), (jx, jy),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

            cv2.rectangle(frame, (0,0), (300,120), (0,0,0), -1)
            cv2.putText(frame, f"Reps: {count}", (10,50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 3)
            cv2.putText(frame, f"Stage: {stage}", (10,90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

            return frame, count, stage, feedback

    return frame, rep_counter.count, rep_counter.stage, "Stand in front of camera!"