import cv2
import mediapipe as mp

# Inicializa o MediaPipe Pose
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Inicializa o Pose Landmarker
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Captura de vídeo da câmera
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Converte a imagem para RGB (requerido pelo MediaPipe)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Processa a imagem para detectar a pose
    result = pose.process(rgb_frame)

    # Desenha os landmarks se a pose for detectada
    if result.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Exibe o frame com os landmarks desenhados
    cv2.imshow('Pose Landmarker', frame)

    # Sai ao pressionar a tecla 'ESC'
    if cv2.waitKey(1) & 0xFF == 27:  # 27 é o código ASCII para ESC
        break

# Libera os recursos
cap.release()
cv2.destroyAllWindows()
