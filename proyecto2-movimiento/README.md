# Proyecto 2 — Detector de movimiento

Segundo proyecto de la serie. Detecta zonas en movimiento en tiempo real comparando frames consecutivos. Introduce dos métodos clásicos de sustracción de fondo: **AbsDiff** y **MOG2**.

## 🎯 Objetivos de aprendizaje

- Comprender la sustracción de fondo como técnica base de vigilancia
- Usar `cv2.absdiff()` para comparar frames consecutivos
- Usar `cv2.createBackgroundSubtractorMOG2()` para fondo adaptativo
- Aplicar morfología (dilatación) para limpiar máscaras de ruido
- Trabajar con contornos: `findContours`, `contourArea`, `boundingRect`
- Crear overlays semitransparentes con `cv2.addWeighted`
- Usar `cv2.createTrackbar` para ajustar parámetros en tiempo real

## 📋 Requisitos

| Requisito | Versión |
|-----------|---------|
| Python | 3.10+ |
| OpenCV | 4.5.x (`python3-opencv` via apt) |
| NumPy | `< 2.0` (`pip install --user "numpy<2"`) |

> Mismas dependencias que el [Proyecto 1](../proyecto1-webcam/). No requiere instalación adicional.

## 📁 Archivos

```
proyecto2-movimiento/
├── README.md                  ← este archivo
└── proyecto2_movimiento.py    ← script principal
```

## ▶️ Ejecución

```bash
python3 proyecto2_movimiento.py
```

Se abren **dos ventanas**:
- `Proyecto 2 - Detector de movimiento` — video con bounding boxes
- `Mascara de movimiento` — la máscara binaria en blanco y negro

## ⌨️ Controles

| Tecla | Numpad | Acción |
|-------|--------|--------|
| `1` | 177 | Método AbsDiff (diferencia entre frames) |
| `2` | 178 | Método MOG2 (fondo adaptativo gaussiano) |
| `R` | — | Resetear fondo aprendido y contador |
| `S` | — | Guardar captura con timestamp |
| `Q` | — | Salir |

El **trackbar "Sensibilidad"** controla el área mínima (en px²) para considerar un contorno como movimiento real. Valores bajos = más sensible.

## 🔬 Métodos implementados

### Método 1 — AbsDiff (diferencia absoluta)

```
frame_actual (gris) → blur → absdiff(anterior) → threshold → dilate → contornos
```

- Compara el frame actual con el **inmediatamente anterior**
- Detecta cualquier cambio entre dos frames consecutivos
- Más reactivo a movimientos rápidos
- Más afectado por ruido de cámara e iluminación variable

### Método 2 — MOG2 (Mixture of Gaussians)

```
frame_actual → mog2.apply() → threshold (eliminar sombras) → dilate → contornos
```

- Construye un **modelo estadístico del fondo** a lo largo del tiempo
- Se adapta automáticamente a cambios de iluminación
- Más robusto para vigilancia continua de larga duración
- Necesita unos segundos iniciales para "aprender" el fondo

### Pipeline completo de procesamiento

```
Frame crudo
    │
    ▼ cvtColor (BGR → GRAY) + GaussianBlur   [solo AbsDiff]
    │
    ▼ absdiff / mog2.apply()
    │
    ▼ threshold (binarizar)
    │
    ▼ dilate (morfología — rellenar huecos)
    │
    ▼ findContours
    │
    ▼ filtrar por area_minima
    │
    ▼ boundingRect → dibujar rectángulo
```

## 🧠 Conceptos clave

**`cv2.absdiff(img1, img2)`**
Calcula `|img1 - img2|` píxel a píxel. El resultado es una imagen donde los píxeles que cambiaron tienen valores altos (claros) y los estáticos son 0 (negro).

**`cv2.threshold(src, 25, 255, THRESH_BINARY)`**
Binariza: si valor > 25 → 255 (blanco), si no → 0 (negro). El umbral 25 es el mínimo cambio de intensidad para considerar movimiento.

**`cv2.dilate(mascara, kernel, iterations=2)`**
Expande las zonas blancas de la máscara. Une fragmentos cercanos del mismo objeto y rellena huecos internos, evitando que un objeto genere muchos contornos pequeños.

**`cv2.findContours`** — bug conocido entre versiones:
```python
# OpenCV 4.x (tu entorno): devuelve 2 valores
contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# OpenCV 3.x: devuelve 3 valores — NO aplica aquí pero es importante saberlo
_, contornos, _ = cv2.findContours(...)
```

**`cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, dst)`**
Mezcla dos imágenes con pesos. Usado para la barra superior semitransparente: dibuja un rectángulo negro en `overlay` y lo fusiona con el frame original al 50%.

## 🚀 Retos propuestos

| # | Reto | Función clave |
|---|------|---------------|
| A | Mostrar hora y fecha en el HUD | `datetime.now().strftime()` |
| B | Grabar video automáticamente cuando hay movimiento | `cv2.VideoWriter` |
| C | Agregar un rectángulo de zona de interés (ROI) — solo detectar dentro | Slicing de numpy: `mascara[y1:y2, x1:x2]` |
| D | Heatmap acumulativo de movimiento | `cv2.addWeighted` + acumular máscara |
| E | Enviar alerta por pantalla que dure 3 segundos tras el último movimiento | `time.time()` + temporizador |

## 🐛 Problemas conocidos y soluciones

| Problema | Causa | Solución |
|----------|-------|----------|
| Muchos falsos positivos al iniciar | AbsDiff aún sin frame anterior estable | Esperar 1-2s o presionar `R` para resetear |
| MOG2 tarda en estabilizarse | Necesita aprender el fondo | Normal — esperar ~5s sin movimiento |
| `createTrackbar` falla si ventana no existe | `namedWindow` debe ir antes del trackbar | El código ya lo hace en el orden correcto |
| `findContours` retorna 3 valores | Usando OpenCV 3.x en lugar de 4.x | Cambiar a `_, contornos, _ = ...` |
| Movimiento fantasma al presionar `1` o `2` | `frame_anterior` desactualizado al cambiar método | El código resetea `frame_anterior = None` al cambiar |

## 🔗 Navegación

- ← [Proyecto 1 — Captura y filtros](../proyecto1-webcam/)
- → Proyecto 3 — Detector de rostros *(próximamente)*

---

*Proyecto 2 de 15 — Serie ML con Webcam y Micrófono*
