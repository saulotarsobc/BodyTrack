import cv2
import mediapipe as mp
import numpy as np

# Inicializa o MediaPipe Pose e a captura de vídeo
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Captura de vídeo da câmera com proporção 4:3 (640x480)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Largura
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Altura


def desenha_retangulo(frame, cor, alpha):
    """Desenha o retângulo na cor e opacidade especificadas."""
    overlay = frame.copy()
    cv2.rectangle(overlay, (213, 80), (426, 240), cor, -1)
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha,
                    0, frame)  # Combina as imagens
    return frame


def desenha_circulo(frame, x, y, raio, cor=(255, 255, 255), opacidade=0.2):
    """Desenha um círculo opaco na imagem."""
    overlay = frame.copy()
    cv2.circle(overlay, (x, y), raio, cor, -1)
    return cv2.addWeighted(overlay, opacidade, frame, 1 - opacidade, 0)


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Converte a imagem para RGB (requerido pelo MediaPipe)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(rgb_frame)

    if result.pose_landmarks:
        landmarks = result.pose_landmarks.landmark
        height, width, _ = frame.shape

        # Desenha o círculo em torno da cabeça
        cabeca_x = int(landmarks[mp_pose.PoseLandmark.NOSE].x * width)
        cabeca_y = int(landmarks[mp_pose.PoseLandmark.NOSE].y * height)

        # Aumenta o raio para cobrir a cabeça inteira
        raio_cabeca = int(0.12 * height)
        frame = desenha_circulo(frame, cabeca_x, cabeca_y,
                                raio=raio_cabeca, cor=(255, 255, 255))

        # Verifica se o círculo saiu do retângulo verde
        if (cabeca_x - raio_cabeca < 213 or cabeca_x + raio_cabeca > 426 or
                cabeca_y - raio_cabeca < 80 or cabeca_y + raio_cabeca > 240):
            cor_retangulo = (0, 0, 255)  # Vermelho
        else:
            cor_retangulo = (40, 255, 65)  # Verde

        # Desenha o retângulo com a cor apropriada
        frame = desenha_retangulo(frame, cor_retangulo, alpha=0.2)

    # Exibe o frame com o enquadramento
    cv2.imshow('Enquadramento Automático - BodyTrack', frame)

    # Sai ao pressionar a tecla 'ESC'
    if cv2.waitKey(1) & 0xFF == 27:  # 27 é o código ASCII para ESC
        break

# Libera os recursos
cap.release()
cv2.destroyAllWindows()
