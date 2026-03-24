import cv2
import numpy as np
import os
from datetime import datetime

# ── 1. Abrir cámara ───────────────────────────────────────────────
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: no se pudo abrir la cámara")
    exit()

# ── 2. Configuración inicial ──────────────────────────────────────
metodo_activo  = "absdiff"   # "absdiff" o "mog2"
frame_anterior = None        # usado por método absdiff
eventos_totales = 0          # contador de detecciones

# Sustractor de fondo MOG2 (Mixture of Gaussians)
# history=500: frames que usa para aprender el fondo
# varThreshold=50: sensibilidad — mayor = menos sensible
# detectShadows=False: ignorar sombras (más rápido)
mog2 = cv2.createBackgroundSubtractorMOG2(
    history=500, varThreshold=50, detectShadows=False
)

# ── 3. Ventana y trackbar de sensibilidad ─────────────────────────
VENTANA = "Proyecto 2 - Detector de movimiento"
cv2.namedWindow(VENTANA)

# Trackbar: área mínima de contorno para considerarse movimiento
# Valores bajos = más sensible (detecta objetos pequeños)
# Valores altos = menos sensible (ignora ruido y objetos pequeños)
cv2.createTrackbar("Sensibilidad", VENTANA, 1500, 10000, lambda x: None)

# ── 4. Loop principal ─────────────────────────────────────────────
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al leer frame")
        break

    # Espejo horizontal (más natural para vigilancia frontal)
    frame = cv2.flip(frame, 1)

    # Copia limpia para dibujar encima sin afectar el procesamiento
    visualizacion = frame.copy()

    # Leer sensibilidad desde trackbar
    area_minima = cv2.getTrackbarPos("Sensibilidad", VENTANA)
    area_minima = max(area_minima, 100)  # nunca menor a 100px²

    # ── 5. Calcular máscara de movimiento según método ────────────
    if metodo_activo == "absdiff":
        # Convertir a gris para comparar más rápido
        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Suavizar para reducir ruido de sensor
        gris = cv2.GaussianBlur(gris, (21, 21), 0)

        if frame_anterior is None:
            frame_anterior = gris
            continue

        # Diferencia absoluta entre frame actual y anterior
        diferencia = cv2.absdiff(frame_anterior, gris)

        # Umbralizar: píxeles con diferencia > 25 = movimiento
        _, mascara = cv2.threshold(diferencia, 25, 255, cv2.THRESH_BINARY)

        # Actualizar frame anterior
        frame_anterior = gris

    else:  # mog2
        # MOG2 aprende el fondo y devuelve máscara directamente
        # learningRate=-1 significa automático
        mascara = mog2.apply(frame, learningRate=-1)

        # Eliminar sombras (valores grises que MOG2 marca como 127)
        _, mascara = cv2.threshold(mascara, 200, 255, cv2.THRESH_BINARY)

    # ── 6. Limpiar máscara con morfología ─────────────────────────
    # Dilatar rellena huecos dentro de los objetos en movimiento
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mascara = cv2.dilate(mascara, kernel, iterations=2)

    # ── 7. Encontrar contornos de las zonas en movimiento ─────────
    # En OpenCV 4.x: findContours devuelve (contornos, jerarquía)
    # En OpenCV 3.x: devuelve (imagen, contornos, jerarquía) — bug conocido
    contornos, _ = cv2.findContours(
        mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    hay_movimiento = False

    for contorno in contornos:
        area = cv2.contourArea(contorno)

        # Ignorar contornos pequeños (ruido)
        if area < area_minima:
            continue

        hay_movimiento = True

        # Rectángulo delimitador del contorno
        x, y, w, h = cv2.boundingRect(contorno)
        cv2.rectangle(visualizacion, (x, y), (x + w, y + h),
                      (0, 255, 0), 2)

        # Etiqueta con el área
        cv2.putText(visualizacion, f"{int(area)}px2",
                    (x, y - 8), cv2.FONT_HERSHEY_SIMPLEX,
                    0.45, (0, 255, 0), 1)

    # ── 8. Contador de eventos ────────────────────────────────────
    if hay_movimiento:
        eventos_totales += 1

    # ── 9. HUD — información en pantalla ─────────────────────────
    estado_color = (0, 0, 255) if hay_movimiento else (200, 200, 200)
    estado_texto = "MOVIMIENTO DETECTADO" if hay_movimiento else "Sin movimiento"

    # Barra superior semitransparente
    overlay = visualizacion.copy()
    cv2.rectangle(overlay, (0, 0), (visualizacion.shape[1], 40),
                  (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.5, visualizacion, 0.5, 0, visualizacion)

    cv2.putText(visualizacion, estado_texto,
                (10, 26), cv2.FONT_HERSHEY_SIMPLEX,
                0.65, estado_color, 2)

    metodo_label = f"Metodo: {'AbsDiff' if metodo_activo == 'absdiff' else 'MOG2'}"
    cv2.putText(visualizacion, metodo_label,
                (visualizacion.shape[1] - 220, 26),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 1)

    # Esquina inferior: eventos y controles
    alto = visualizacion.shape[0]
    cv2.putText(visualizacion, f"Eventos: {eventos_totales}",
                (10, alto - 40), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (180, 180, 180), 1)
    cv2.putText(visualizacion,
                "1=AbsDiff  2=MOG2  R=reset  S=captura  Q=salir",
                (10, alto - 15), cv2.FONT_HERSHEY_SIMPLEX,
                0.45, (120, 120, 120), 1)

    # ── 10. Mostrar máscara en ventana secundaria ─────────────────
    mascara_bgr = cv2.cvtColor(mascara, cv2.COLOR_GRAY2BGR)
    cv2.imshow("Mascara de movimiento", mascara_bgr)

    cv2.imshow(VENTANA, visualizacion)

    # ── 11. Teclado ───────────────────────────────────────────────
    tecla = cv2.waitKey(1) & 0xFF

    if tecla == ord('q'):
        break

    elif tecla in (ord('1'), 177):
        metodo_activo  = "absdiff"
        frame_anterior = None
        print("Método: AbsDiff")

    elif tecla in (ord('2'), 178):
        metodo_activo = "mog2"
        print("Método: MOG2")

    elif tecla in (ord('r'), ord('R')):
        # Reset: olvidar fondo aprendido
        frame_anterior = None
        mog2 = cv2.createBackgroundSubtractorMOG2(
            history=500, varThreshold=50, detectShadows=False
        )
        eventos_totales = 0
        print("Fondo reseteado")

    elif tecla in (ord('s'), ord('S')):
        os.makedirs("proyecto2-movimiento/saves", exist_ok=True)
        nombre = f"proyecto2-movimiento/saves/movimiento_{datetime.now():%Y%m%d_%H%M%S}.png"
        cv2.imwrite(nombre, visualizacion)
        print(f"Captura guardada: {nombre}")

# ── 12. Liberar recursos ──────────────────────────────────────────
cap.release()
cv2.destroyAllWindows()
print(f"Sesión finalizada. Eventos detectados: {eventos_totales}")
