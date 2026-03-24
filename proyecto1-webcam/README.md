# Proyecto 1 — Captura y procesamiento de imagen

Primer proyecto de la serie. Captura frames en tiempo real desde la webcam y aplica filtros clásicos de visión por computadora usando OpenCV. Base conceptual de todos los proyectos siguientes.

## 🎯 Objetivos de aprendizaje

- Entender cómo Python representa una imagen como matriz numérica (`numpy array`)
- Comprender el orden de canales BGR de OpenCV
- Capturar video en tiempo real con `cv2.VideoCapture`
- Aplicar transformaciones básicas sobre frames: escala de grises, desenfoque, detección de bordes, filtros de color
- Manejar el loop principal de una aplicación de visión en tiempo real

## 📋 Requisitos

| Requisito | Versión |
|-----------|---------|
| Python | 3.10+ |
| OpenCV | 4.5.x (`python3-opencv` via apt) |
| NumPy | `< 2.0` (`pip install --user "numpy<2"`) |

> **Nota:** usar `python3-opencv` de apt requiere mantener NumPy `< 2.0`. Ver [lecciones aprendidas](../README.md#️-lecciones-aprendidas-en-la-instalación) en el README principal.

## 📁 Archivos

```
proyecto1-webcam/
├── README.md               ← este archivo
└── proyecto1_webcam.py     ← script principal
```

## ▶️ Ejecución

```bash
python3 proyecto1_webcam.py
```

## ⌨️ Controles

| Tecla (superior) | Tecla (numpad) | Acción |
|------------------|----------------|--------|
| `1` | Numpad 1 (código 177) | Filtro original |
| `2` | Numpad 2 (código 178) | Escala de grises |
| `3` | Numpad 3 (código 179) | Desenfoque Gaussiano |
| `4` | Numpad 4 (código 180) | Detección de bordes (Canny) |
| `5` | Numpad 5 (código 181) | Filtro sepia |
| `6` | Numpad 6 (código 182) | Imagen invertida (negativo) |
| `Q` | — | Salir |

## 🎨 Filtros implementados

### 1 — Original
Sin transformación. Muestra el frame crudo de la cámara.

### 2 — Escala de grises
```python
cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
```
Combina los 3 canales BGR en 1 usando pesos perceptuales: el ojo humano es más sensible al verde (~59%), menos al rojo (~30%) y muy poco al azul (~11%).

**Fórmula:** `L = 0.114·B + 0.587·G + 0.299·R`

### 3 — Desenfoque Gaussiano
```python
cv2.GaussianBlur(frame, (15, 15), 0)
```
Promedia cada píxel con sus vecinos usando una distribución gaussiana. El kernel `(15, 15)` define el área de influencia — más grande = más borroso. Usado en casi todos los pipelines de visión como paso de preprocesamiento.

### 4 — Detección de bordes (Canny)
```python
gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
cv2.Canny(gris, 100, 200)
```
Algoritmo de 4 pasos: suaviza con Gaussian → calcula gradiente (Sobel) → suprime no-máximos → aplica umbral doble. Los valores `100` y `200` son los umbrales inferior y superior.

### 5 — Sepia
```python
kernel = np.array([[0.272, 0.534, 0.131],
                   [0.349, 0.686, 0.168],
                   [0.393, 0.769, 0.189]])
cv2.transform(frame, kernel)
```
Multiplicación matricial 3×3 que mezcla los canales para producir el tono café cálido característico del revelado fotográfico antiguo. Requiere `np.clip(resultado, 0, 255)` para evitar desbordamiento.

### 6 — Invertido (negativo)
```python
cv2.bitwise_not(frame)
```
Resta cada valor de píxel de 255. Negro → blanco, y cada color se convierte en su complementario.

**Fórmula:** `resultado[y, x] = 255 − frame[y, x]`

## 🧠 Conceptos clave

**Imagen = matriz numpy 3D**
```
img.shape → (alto, ancho, 3)
img[y, x] → [B, G, R]      # ojo: primero y (fila), luego x (columna)
img.dtype → uint8           # valores enteros 0–255
```

**Loop principal**
```python
cap = cv2.VideoCapture(0)   # 0 = primera cámara USB
while True:
    ret, frame = cap.read() # ret=True si leyó bien
    ...
    cv2.imshow("ventana", frame)
    tecla = cv2.waitKey(1) & 0xFF
    if tecla == ord('q'): break
cap.release()
cv2.destroyAllWindows()
```

## 🚀 Retos propuestos

| # | Reto | Función clave |
|---|------|---------------|
| A | Guardar captura con tecla `S` | `cv2.imwrite()` |
| B | Mostrar dimensiones del frame en pantalla | `frame.shape` + `cv2.putText()` |
| C | Imagen en espejo | `cv2.flip(frame, 1)` |
| D | Dibujar rectángulo centrado | `cv2.rectangle()` |
| E | Filtro pixelado (efecto 8-bit) | `cv2.resize()` + `INTER_NEAREST` |

## 🐛 Problemas conocidos y soluciones

| Problema | Solución |
|----------|----------|
| Warning `GStreamer: Cannot query video position` | Inofensivo, ignorar |
| Cámara no detectada con índice `0` | Probar con `cv2.VideoCapture(1)` o verificar `ls /dev/video*` |
| Numpad no cambia filtro | Ver tabla de controles — los códigos son 177–182, no 49–54 |
| `putText` falla sobre imagen en gris | Convertir con `cv2.cvtColor(gris, cv2.COLOR_GRAY2BGR)` antes de dibujar texto |

## 🔗 Siguiente proyecto

[Proyecto 2 — Detector de movimiento](../proyecto2-movimiento/) — usa este mismo loop como base y agrega sustracción de fondo entre frames consecutivos.

---

*Proyecto 1 de 15 — Serie ML con Webcam y Micrófono*
