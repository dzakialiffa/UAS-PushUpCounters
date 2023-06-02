import cv2
import mediapipe as mp

# Inisialisasi penghitungan push-up
push_up_count = 0
is_counting = False

# Inisialisasi MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Fungsi untuk menghitung push-up
def count_push_ups(landmarks):
    global push_up_count, is_counting

    # Mendapatkan posisi bahu dan pinggul
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y
    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y

    # Menghitung push-up berdasarkan pergerakan bahu dan pinggul
    if left_shoulder > left_hip and right_shoulder > right_hip and not is_counting:
        push_up_count += 1
        is_counting = True
    elif left_shoulder < left_hip and right_shoulder < right_hip:
        is_counting = False

    # Menampilkan push-up count
    cv2.putText(image, f"Push-ups: {push_up_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

# Menginisialisasi webcam
cap = cv2.VideoCapture(0)

# Memulai MediaPipe Pose
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, image = cap.read()

        # Mengubah warna gambar ke BGR ke RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Mendeteksi pose dengan MediaPipe
        results = pose.process(image_rgb)

        # Mengubah kembali warna gambar ke RGB ke BGR
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

        # Menampilkan landmark pose jika ada
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Menghitung push-up
            count_push_ups(results.pose_landmarks.landmark)

        cv2.imshow('Push-up Counter', image)

        # Menutup aplikasi dengan menekan tombol 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Menghentikan webcam dan menutup jendela
cap.release()
cv2.destroyAllWindows()
