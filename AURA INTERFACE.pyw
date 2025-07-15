import cv2
import mediapipe as mp
import numpy as np
import time
import platform
import math
import pyautogui
import threading

# --- Tenta importar bibliotecas específicas para o sistema ---
IS_WINDOWS = platform.system() == 'Windows'
if IS_WINDOWS:
    import ctypes

# =====================================================================================
# --- PARÂMETROS DE CONFIGURAÇÃO ---
# =====================================================================================
W_CAM, H_CAM = 1280, 720
SENSITIVITY = 5.0
SMOOTHING_FACTOR = 0.2

# VALOR ALTERADO de 1.0 para 0.5 para uma resposta mais rápida.
ACTION_DELAY_SECONDS = 0.5

TWO_HAND_CONFIDENCE_FRAMES = 3
# =====================================================================================

# --- Variáveis Globais de Estado para Controle via Terminal ---
program_is_running = True
camera_window_visible = False
lock = threading.Lock()

def user_input_handler():
    """Thread dedicada para ouvir os comandos do usuário no terminal."""
    global program_is_running, camera_window_visible
    
    while program_is_running:
        try:
            command = input().lower()
            with lock:
                if command == 'c':
                    camera_window_visible = not camera_window_visible
                    if camera_window_visible:
                        print("--> Comando: Mostrar janela da camera.")
                    else:
                        print("--> Comando: Esconder janela da camera.")
                elif command == 'q':
                    print("--> Comando: Encerrando o programa...")
                    program_is_running = False
        except (EOFError, KeyboardInterrupt):
            with lock:
                program_is_running = False
            break

def move_mouse_fast(x, y):
    if IS_WINDOWS: ctypes.windll.user32.SetCursorPos(int(x), int(y))
    else: pyautogui.moveTo(x, y)

def get_finger_state(hand_landmarks, handedness_label):
    fingers = []
    tip_ids = [4, 8, 12, 16, 20]
    is_right_hand = handedness_label == 'Right'
    if is_right_hand:
        if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x: fingers.append(1)
        else: fingers.append(0)
    else:
        if hand_landmarks.landmark[tip_ids[0]].x > hand_landmarks.landmark[tip_ids[0] - 1].x: fingers.append(1)
        else: fingers.append(0)
    for id in range(1, 5):
        if hand_landmarks.landmark[tip_ids[id]].y < hand_landmarks.landmark[tip_ids[id] - 2].y: fingers.append(1)
        else: fingers.append(0)
    return fingers

# --- INICIALIZAÇÃO ---
print("Iniciando Sistema de Controle por Gestos...")
cap = cv2.VideoCapture(0)
cap.set(3, W_CAM)
cap.set(4, H_CAM)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(model_complexity=0, max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Variáveis de estado
prev_hand_x, prev_hand_y = 0, 0
smoothed_delta_x, smoothed_delta_y = 0, 0
is_moving_mode = False
is_mouse_down = False
initial_zoom_dist = 0
two_hand_frame_counter = 0
p_time = 0
current_gesture = "NEUTRAL"
gesture_start_time = 0
action_locked = False

screen_width, screen_height = pyautogui.size()
pyautogui.FAILSAFE = False

input_thread = threading.Thread(target=user_input_handler, daemon=True)
input_thread.start()

print("\n=======================================================")
print("    SISTEMA DE CONTROLE DISCRETO ATIVADO")
print("-------------------------------------------------------")
print("-> O controle por gestos JA ESTA FUNCIONANDO.")
print("-> A janela da camera esta escondida por padrao.")
print("\nCOMANDOS DO TERMINAL:")
print("  'c' + Enter : Mostrar/Esconder a janela da camera")
print("  'q' + Enter : Encerrar o programa")
print("=======================================================\n")

try:
    while program_is_running:
        success, img = cap.read()
        if not success: continue
        img = cv2.flip(img, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        detected_gesture_this_frame = "NEUTRAL"
        all_hands_data = []

        if results.multi_hand_landmarks:
            for hand_landmarks, handedness_info in zip(results.multi_hand_landmarks, results.multi_handedness):
                handedness_label = handedness_info.classification[0].label
                fingers = get_finger_state(hand_landmarks, handedness_label)
                all_hands_data.append({'landmarks': hand_landmarks, 'fingers': fingers, 'label': handedness_label})
                if camera_window_visible:
                    mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            num_hands = len(all_hands_data)
            if num_hands == 1:
                fingers = all_hands_data[0]['fingers']
                if fingers == [0, 1, 1, 0, 0]: detected_gesture_this_frame = "MOVE"
                elif fingers == [1, 1, 1, 0, 0]: detected_gesture_this_frame = "DRAG_INTENT"
                elif fingers == [0, 1, 1, 0, 1]: detected_gesture_this_frame = "CLICK_INTENT"
            elif num_hands == 2:
                if all_hands_data[0]['label'] != all_hands_data[1]['label']:
                    if all_hands_data[0]['fingers'] == [0, 1, 1, 0, 0] and all_hands_data[1]['fingers'] == [0, 1, 1, 0, 0]:
                        detected_gesture_this_frame = "ZOOM"

        if detected_gesture_this_frame != current_gesture:
            current_gesture = detected_gesture_this_frame
            gesture_start_time = time.time()
            action_locked = False
            if current_gesture != "DRAG_INTENT" and is_mouse_down:
                pyautogui.mouseUp(); is_mouse_down = False
        
        is_movement_gesture = (current_gesture == "MOVE") or (current_gesture == "DRAG_INTENT" and is_mouse_down)
        
        if is_movement_gesture and all_hands_data:
            lm = all_hands_data[0]['landmarks']
            ix, iy = lm.landmark[8].x * W_CAM, lm.landmark[8].y * H_CAM
            mx, my = lm.landmark[12].x * W_CAM, lm.landmark[12].y * H_CAM
            current_hand_x = (ix + mx) / 2
            current_hand_y = (iy + my) / 2
            if not is_moving_mode:
                is_moving_mode = True
                prev_hand_x, prev_hand_y = current_hand_x, current_hand_y
            else:
                delta_x = current_hand_x - prev_hand_x
                delta_y = current_hand_y - prev_hand_y
                smoothed_delta_x = (smoothed_delta_x * (1 - SMOOTHING_FACTOR)) + (delta_x * SMOOTHING_FACTOR)
                smoothed_delta_y = (smoothed_delta_y * (1 - SMOOTHING_FACTOR)) + (delta_y * SMOOTHING_FACTOR)
                mouse_x, mouse_y = pyautogui.position()
                new_mouse_x = mouse_x + smoothed_delta_x * SENSITIVITY
                new_mouse_y = mouse_y + smoothed_delta_y * SENSITIVITY
                move_mouse_fast(max(0, min(screen_width - 1, new_mouse_x)), max(0, min(screen_height - 1, new_mouse_y)))
                prev_hand_x, prev_hand_y = current_hand_x, current_hand_y
        else:
            is_moving_mode = False

        if current_gesture == "CLICK_INTENT":
            elapsed_time = time.time() - gesture_start_time
            if elapsed_time >= ACTION_DELAY_SECONDS and not action_locked:
                pyautogui.click(); action_locked = True
        
        elif current_gesture == "DRAG_INTENT":
            elapsed_time = time.time() - gesture_start_time
            if elapsed_time >= ACTION_DELAY_SECONDS and not is_mouse_down:
                pyautogui.mouseDown(); is_mouse_down = True
        
        if current_gesture == "ZOOM":
            two_hand_frame_counter += 1
            if two_hand_frame_counter > TWO_HAND_CONFIDENCE_FRAMES:
                lm1, lm2 = all_hands_data[0]['landmarks'], all_hands_data[1]['landmarks']
                ix1, iy1, mx1, my1 = lm1.landmark[8].x, lm1.landmark[8].y, lm1.landmark[12].x, lm1.landmark[12].y
                ix2, iy2, mx2, my2 = lm2.landmark[8].x, lm2.landmark[8].y, lm2.landmark[12].x, lm2.landmark[12].y
                cx1, cy1 = (ix1 + mx1) / 2 * W_CAM, (iy1 + my1) / 2 * H_CAM
                cx2, cy2 = (ix2 + mx2) / 2 * W_CAM, (iy2 + my2) / 2 * H_CAM
                dist = math.hypot(cx2 - cx1, cy2 - cy1)
                if initial_zoom_dist == 0: initial_zoom_dist = dist
                zoom_amount = (dist - initial_zoom_dist) / 200.0
                pyautogui.scroll(int(zoom_amount * 10))
        else:
            initial_zoom_dist = 0
            two_hand_frame_counter = 0

        if camera_window_visible:
            # Bloco de feedback visual
            if current_gesture == "MOVE": cv2.putText(img, "MOVER CURSOR", (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
            elif current_gesture == "CLICK_INTENT":
                if not action_locked: cv2.putText(img, "Segure para Clicar...", (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 3)
                else: cv2.putText(img, "CLICADO!", (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
            elif current_gesture == "DRAG_INTENT":
                if not is_mouse_down: cv2.putText(img, "Segure para Arrastar...", (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 3)
                else: cv2.putText(img, "ARRASTANDO", (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
            elif current_gesture == "ZOOM":
                if 'cx1' in locals():
                    cv2.line(img, (int(cx1), int(cy1)), (int(cx2), int(cy2)), (0, 255, 255), 3)
                cv2.putText(img, "ZOOM", (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 3)
            
            c_time = time.time()
            fps = 1 / (c_time - p_time) if (c_time - p_time) > 0 else 0
            p_time = c_time
            cv2.putText(img, f'FPS: {int(fps)}', (W_CAM - 150, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
            
            cv2.imshow("Visualizador de Controle", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                program_is_running = False
        else:
            cv2.destroyAllWindows()
            p_time = time.time()
            time.sleep(0.01)

finally:
    print("Recursos liberados. Programa encerrado.")
    program_is_running = False
    cap.release()
    cv2.destroyAllWindows()