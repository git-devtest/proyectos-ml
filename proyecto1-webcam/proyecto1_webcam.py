import cv2
import numpy as np
from datetime import datetime
import os

# ── 1. Abrir cámara (índice 0 = primera cámara USB) ──────────────
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: no se pudo abrir la cámara")
    exit()

# ── 2. Selector de filtro activo ──────────────────────────────────
filtro_activo = "original"

# ── 3. Loop principal ─────────────────────────────────────────────
while True:
    # Leer un frame de la cámara
    ret, frame = cap.read()

    if not ret:
        print("Error al leer frame")
        break

    # Reto C: Mostrar la imagen en espejo
    frame = cv2.flip(frame, 1)  # 1 = horizontal (espejo), 0 = vertical, -1 = ambos ejes

    # ── 4. Aplicar filtro según selección ─────────────────────────
    if filtro_activo == "gris":
        resultado = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    elif filtro_activo == "blur":
        resultado = cv2.GaussianBlur(frame, (15, 15), 0)

    elif filtro_activo == "bordes":
        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resultado = cv2.Canny(gris, 100, 200)

    elif filtro_activo == "sepia":
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        resultado = cv2.transform(frame, kernel)
        resultado = np.clip(resultado, 0, 255).astype(np.uint8)

    elif filtro_activo == "invertido":
        resultado = cv2.bitwise_not(frame)
    
    # Reto E: Filtro "pixelado" (pixelate)
    # Agregar como nuevo elif en el bloque de filtros:
    elif filtro_activo == "pixelado":
        alto, ancho = frame.shape[:2]
        factor = 12  # tamaño de cada "pixel" (mayor = más cuadrados)

        # 1. Reducir a tamaño pequeño
        pequeño = cv2.resize(frame,
        (ancho // factor, alto // factor),
        interpolation=cv2.INTER_LINEAR)

        # 2. Escalar de vuelta al tamaño original
        resultado = cv2.resize(pequeño,
            (ancho, alto),
            interpolation=cv2.INTER_NEAREST)  # clave: sin interpolación

    else:  # "original"
        resultado = frame

    # ── 5. Mostrar información en pantalla ────────────────────────
    cv2.putText(
        resultado,
        f"Filtro: {filtro_activo}  |  1-7 cambiar  |  Q salir",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 0),
        2
    )

    # Reto B: Mostrar dimensiones de la imagen en pantalla
    alto, ancho, canales = frame.shape
    info_text = f"Dimensiones: {ancho}x{alto} | Canales: {canales}"
    cv2.putText(
        resultado, info_text,
        (10, alto - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5, (200, 200, 200), 1
    )

    # Reto D: Dibujar un rectángulo en el centro de la imagen
    centro_x = frame.shape[1] // 2  # Obtiene el ancho de la imagen y lo divide por 2
    centro_y = frame.shape[0] // 2  # Obtiene el alto de la imagen y lo divide por 2
    # offset de 50 para un cuadrado de 100x100 centrado real
    cv2.rectangle(resultado, (centro_x - 50, centro_y - 50), (centro_x + 50, centro_y + 50), (0, 255, 0), 2)

    # ── 6. Mostrar ventana ────────────────────────────────────────
    cv2.imshow("Proyecto 1 - Webcam", resultado)

    # ── 7. Capturar teclado ───────────────────────────────────────
    tecla = cv2.waitKey(1) & 0xFF

    if   tecla == ord('q'): break
    elif tecla in (ord('1'), 177):  filtro_activo = "original"
    elif tecla in (ord('2'), 178):  filtro_activo = "gris"
    elif tecla in (ord('3'), 179):  filtro_activo = "blur"
    elif tecla in (ord('4'), 180):  filtro_activo = "bordes"
    elif tecla in (ord('5'), 181):  filtro_activo = "sepia"
    elif tecla in (ord('6'), 182):  filtro_activo = "invertido"
    elif tecla in (ord('7'), 183):  filtro_activo = "pixelado"

    # Reto A: Guardar imagen
    elif tecla == ord('s'): 
        os.makedirs("proyecto1-webcam/saves", exist_ok=True)
        nombre = f"proyecto1-webcam/saves/captura_{datetime.now():%Y%m%d_%H%M%S}.png"
        cv2.imwrite(nombre, resultado)
        print(f"Guardada: {nombre}")

# ── 8. Liberar recursos ───────────────────────────────────────────
cap.release()
cv2.destroyAllWindows()
