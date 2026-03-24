# 🎥🎤 Proyectos ML con Webcam y Micrófono

Repositorio de aprendizaje progresivo de Machine Learning, Visión por Computadora e Inteligencia Artificial usando una webcam USB con micrófono integrado. Los proyectos están ordenados de menor a mayor dificultad.

## 🖥️ Entorno de desarrollo

| Item | Detalle |
|------|---------|
| **SO** | Linux Mint XFCE (dual-boot con Windows 10) |
| **Python** | 3.10+ |
| **Cámara** | Webcam USB con micrófono integrado, zoom digital 10x |
| **OpenCV** | `python3-opencv` (sistema, con soporte GTK) |

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

## 📦 Instalación general

```bash
# OpenCV con soporte GTK (recomendado en Linux Mint)
sudo apt install python3-opencv

# Dependencias por proyecto (instalar según se avance)
pip install --user numpy matplotlib pyaudio speechrecognition
pip install --user mediapipe ultralytics deepface librosa pyttsx3
```

---

## 📁 Estructura del repositorio

```
proyectos-ml/
├── README.md                        ← este archivo
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