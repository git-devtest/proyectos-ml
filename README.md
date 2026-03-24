# 🎥🎤 Proyectos ML con Webcam y Micrófono

Repositorio de aprendizaje progresivo de Machine Learning, Visión por Computadora e Inteligencia Artificial usando una webcam USB con micrófono integrado. Los proyectos están ordenados de menor a mayor dificultad.

## 🖥️ Entorno de desarrollo

| Item | Detalle |
|------|---------|
| **SO** | Linux Mint XFCE (dual-boot con Windows 10) |
| **Python** | 3.10+ |
| **Cámara** | Webcam USB con micrófono integrado, zoom digital 10x |
| **OpenCV** | `python3-opencv` via `apt` (compilado con GTK) |
| **NumPy** | `numpy<2` via `pip --user` (requerido por `python3-opencv`) |

---

## ⚙️ Instalación base (hacer una sola vez)

```bash
# 1. OpenCV con soporte GTK nativo
sudo apt install python3-opencv

# 2. NumPy compatible con el OpenCV del sistema
#    IMPORTANTE: apt compila opencv con NumPy 1.x — no usar NumPy 2.x
pip install --user "numpy<2"

# 3. Verificar que todo quedó bien
python3 -c "import cv2; import numpy as np; print('OpenCV:', cv2.__version__, '| NumPy:', np.__version__)"
```

### ⚠️ Lecciones aprendidas en la instalación

**No mezclar `apt` y `pip` para el mismo ecosistema.** En este proyecto fue necesario porque `python3-opencv` de apt es la única versión compilada con GTK disponible sin recompilar desde cero. La consecuencia es que NumPy debe mantenerse en `< 2.0`.

| Síntoma | Causa | Solución |
|---------|-------|----------|
| `QFontDatabase: Cannot find font directory` | `opencv-python` de pip trae Qt sin fuentes | Usar `python3-opencv` de apt |
| `The function is not implemented` en `imshow` | `opencv-python-headless` no tiene GUI | No usar headless si se necesita ventana |
| `_ARRAY_API not found` / `numpy.core.multiarray failed to import` | NumPy 2.x incompatible con opencv de apt | `pip install --user "numpy<2"` |
| Warning `GStreamer: Cannot query video position` | Normal con webcams USB | Ignorar, no afecta funcionamiento |

---

## 📷 Proyectos de Visión (Cámara)

| # | Proyecto | Librerías | Estado |
|---|----------|-----------|--------|
| 1 | [Captura y procesamiento de imagen](./proyecto1-webcam/) | `opencv` `numpy` | ✅ Completado |
| 2 | [Detector de movimiento](./proyecto2-movimiento/) | `opencv` `numpy` | 🔜 Próximo |
| 3 | [Detector de rostros](./proyecto3-rostros/) | `opencv` | ⏳ Pendiente |
| 4 | [Reconocimiento de emociones](./proyecto4-emociones/) | `deepface` | ⏳ Pendiente |
| 5 | [Contador de personas](./proyecto5-personas/) | `ultralytics` | ⏳ Pendiente |
| 6 | [Reconocimiento de gestos](./proyecto6-gestos/) | `mediapipe` | ⏳ Pendiente |
| 7 | [Control de PC con gestos](./proyecto7-control-gestos/) | `mediapipe` `pyautogui` | ⏳ Pendiente |

---

## 🎤 Proyectos de Audio (Micrófono)

| # | Proyecto | Librerías | Estado |
|---|----------|-----------|--------|
| 8 | [Grabación y visualización de audio](./proyecto8-audio-viz/) | `pyaudio` `matplotlib` | ⏳ Pendiente |
| 9 | [Detector de silencio/voz (VAD)](./proyecto9-vad/) | `pyaudio` `webrtcvad` | ⏳ Pendiente |
| 10 | [Transcripción de voz a texto](./proyecto10-transcripcion/) | `speech_recognition` `whisper` | ⏳ Pendiente |
| 11 | [Clasificador de sonidos](./proyecto11-sonidos/) | `librosa` `scikit-learn` | ⏳ Pendiente |
| 12 | [Asistente de voz simple](./proyecto12-asistente-voz/) | `speech_recognition` `pyttsx3` | ⏳ Pendiente |

---

## 🎥🎤 Proyectos Combinados (Cámara + Micrófono)

| # | Proyecto | Librerías | Estado |
|---|----------|-----------|--------|
| 13 | [Sistema de vigilancia con alerta de voz](./proyecto13-vigilancia/) | `opencv` `pyttsx3` | ⏳ Pendiente |
| 14 | [Asistente que reconoce tu cara](./proyecto14-reconocimiento-facial/) | `face_recognition` `pyttsx3` | ⏳ Pendiente |
| 15 | [Tutor de poses con retroalimentación](./proyecto15-poses/) | `mediapipe` `pyttsx3` | ⏳ Pendiente |

---

## 🗺️ Ruta de aprendizaje

```
[1] Imagen básica ──► [2] Movimiento ──► [3] Rostros
                                               │
        ┌──────────────────────────────────────┘
        ▼
[8] Audio básico ──► [9] VAD ──► [10] Transcripción
        │
        ▼
[13] Primer proyecto combinado (vigilancia + voz)
        │
        ▼
[4] Emociones ──► [6] Gestos ──► [7] Control PC
[11] Clasificador ──► [12] Asistente
        │
        ▼
[14] Reconocimiento facial ──► [15] Tutor de poses
```

---

## 🔢 Nota: teclado numérico en Linux con OpenCV

En Linux con backend GTK, el numpad envía códigos distintos a las teclas numéricas superiores. El offset es **176 + dígito**:

| Tecla superior | Código | Numpad | Código |
|----------------|--------|--------|--------|
| `1` | 49 | Numpad 1 | 177 |
| `2` | 50 | Numpad 2 | 178 |
| `3` | 51 | Numpad 3 | 179 |
| `4` | 52 | Numpad 4 | 180 |
| `5` | 53 | Numpad 5 | 181 |
| `6` | 54 | Numpad 6 | 182 |

Para detectar ambos en `cv2.waitKey()`:
```python
tecla = cv2.waitKey(1) & 0xFF
if tecla in (ord('1'), 177): ...  # acepta tecla superior Y numpad
```

Para identificar los códigos de cualquier tecla en tu máquina:
```python
import cv2, numpy as np
img = np.zeros((200, 400, 3), dtype=np.uint8)
cv2.imshow("test", img)
while True:
    tecla = cv2.waitKey(0)
    print(f"raw: {tecla}  |  & 0xFF: {tecla & 0xFF}")
    if tecla & 0xFF == ord('q'): break
cv2.destroyAllWindows()
```

---

## 📦 Dependencias por proyecto

```bash
# Proyectos 1–3 (ya disponibles con la instalación base)
sudo apt install python3-opencv
pip install --user "numpy<2"

# Proyectos 4–7 (instalar cuando se llegue a ellos)
pip install --user mediapipe deepface ultralytics

# Proyectos 8–12
pip install --user pyaudio speechrecognition openai-whisper librosa pyttsx3

# Proyecto 14
pip install --user face-recognition
```

---

## 📁 Estructura del repositorio

```
proyectos-ml/
├── README.md                             ← este archivo
├── proyecto1-webcam/
│   ├── README.md
│   └── proyecto1_webcam.py
├── proyecto2-movimiento/
│   ├── README.md
│   └── proyecto2_movimiento.py
└── ...
```

---

## 📚 Recursos

- [Documentación oficial OpenCV Python](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [MediaPipe — Google](https://developers.google.com/mediapipe)
- [Whisper — OpenAI](https://github.com/openai/whisper)
- [Ultralytics YOLO](https://docs.ultralytics.com/)

---

*Serie de proyectos construida paso a paso — de básico a intermedio.*