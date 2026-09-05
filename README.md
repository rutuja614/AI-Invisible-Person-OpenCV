# 🪄 AI Invisible Person Using Computer Vision

A real-time **Invisible Person / Invisibility Cloak** project built using **Python, OpenCV, and NumPy**.

The system first captures and stores the empty background. When a person enters the camera frame wearing a specific colored cloth, the system detects that color and replaces the detected area with the previously captured background. This creates an illusion that the person has become invisible.

---

## 📌 Project Overview

The project demonstrates how **computer vision, image masking, color segmentation, and background replacement** can be combined to create a real-time invisibility effect.

### Basic Concept

```text
Webcam
   ↓
Capture Empty Background
   ↓
Store Background Image
   ↓
Person Enters With Colored Cloth
   ↓
Detect Cloak Color
   ↓
Create Color Mask
   ↓
Replace Masked Area With Background
   ↓
🪄 Invisible Person Effect
```

---

## 🎯 Objectives

* Capture the background automatically.
* Detect a specific colored cloak/cloth.
* Create a mask around the detected color.
* Replace the detected area with the original background.
* Generate a real-time invisibility effect.
* Capture screenshots of the invisible effect.
* Provide support for multiple cloak colors.

---

## ✨ Features

* 🎥 Real-time webcam processing
* 🏠 Automatic background capture
* 🎨 Colored cloak detection
* 🔴 Red cloak support
* 🟢 Green cloak support
* 🟡 Yellow cloak support
* 🎭 Image masking
* 🔄 Background replacement
* 🧹 Noise removal using morphological operations
* 📸 Screenshot capture
* ⚡ Real-time processing
* 🖥️ Simple keyboard-based controls

---

## 🛠️ Technologies Used

| Technology                   | Purpose                                      |
| ---------------------------- | -------------------------------------------- |
| **Python**                   | Main programming language                    |
| **OpenCV**                   | Webcam, image processing and computer vision |
| **NumPy**                    | Image/matrix calculations                    |
| **HSV Color Space**          | Detecting cloak colors                       |
| **Morphological Operations** | Removing noise from masks                    |
| **Webcam**                   | Real-time video input                        |

---

## 🧠 Computer Vision Techniques

### 1. Background Capture

Before the person enters the scene, the system captures multiple frames of the empty background.

```text
Empty Room
    ↓
30 Camera Frames
    ↓
Background Processing
    ↓
background.jpg
```

Multiple frames are used to obtain a cleaner background.

---

### 2. HSV Color Detection

The camera image is converted from BGR to HSV:

```python
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
```

HSV makes it easier to identify a particular color.

The project currently supports:

* Red
* Green
* Yellow

---

### 3. Mask Creation

The selected cloak color is converted into a binary mask.

```text
Cloak Area     → 255
Other Areas    → 0
```

Example:

```text
0   0   255 255
0   255 255 255
0   0   255 255
```

The white/high-value region represents the detected cloak.

---

### 4. Noise Removal

The generated mask can contain small unwanted pixels.

Morphological operations are applied:

```python
cv2.MORPH_OPEN
cv2.MORPH_CLOSE
```

These help clean the mask and fill small gaps.

---

### 5. Background Replacement

The detected cloak region is replaced with the corresponding area from the previously captured background.

Conceptually:

```text
Result =
Background × Mask
+
Current Frame × (1 - Mask)
```

Therefore:

```text
Cloak Region
     ↓
Original Background

Normal Region
     ↓
Current Camera Frame
```

This produces the invisibility illusion.

---


## 🎬 How to Use

### Step 1 — Set up the Camera

Place the webcam/laptop at a fixed position.

**Do not move the camera after capturing the background.**

---

### Step 2 — Capture Background

Make sure the area in front of the camera is empty.

Press:

```text
B
```

The program will show a countdown and capture the background.

The background is saved as:

```text
background.jpg
```

---

### Step 3 — Enter the Frame

Wear a colored cloth.

For example:

```text
🧍 + 🔴 Red Cloth
```

The camera detects the red cloth.

---

### Step 4 — Activate the Correct Color

Press:

```text
R → Red
G → Green
Y → Yellow
```

---

### Step 5 — Become Invisible 🪄

The system detects the cloak and replaces its area with the previously captured background.

The output looks approximately like:

```text
Before:

     🧍
   Person
     +
  Red Cloth


After:

   Background
   Background
   Background
```

---

### Step 6 — Save Screenshot

Press:

```text
S
```

The current output is saved as an image.

---

### Step 7 — Exit

Press:

```text
Q
```

---

## ⌨️ Keyboard Controls

| Key   | Function            |
| ----- | ------------------- |
| **B** | Capture background  |
| **R** | Select red cloak    |
| **G** | Select green cloak  |
| **Y** | Select yellow cloak |
| **S** | Save screenshot     |
| **Q** | Exit application    |

---

## 📊 System Workflow

```text
              ┌─────────────┐
              │   Webcam    │
              └──────┬──────┘
                     ↓
             ┌───────────────┐
             │ Empty Scene?  │
             └───────┬───────┘
                     ↓
              Capture Frames
                     ↓
              Background Image
                     ↓
             Current Camera Frame
                     ↓
                HSV Conversion
                     ↓
              Color Segmentation
                     ↓
                Create Mask
                     ↓
           Morphological Processing
                     ↓
             Background Replacement
                     ↓
              Invisible Effect
                     ↓
             Real-Time Display
```


## ⚠️ Limitations

The current version works best under controlled conditions.

### Camera must remain stationary

If the camera moves after capturing the background, the saved background will no longer align correctly with the current frame.

### Lighting should remain stable

Major changes in lighting can affect color detection.

### Cloth should have a distinct color

The cloak color should be clearly different from the background.

### Background should remain mostly unchanged

Moving objects in the background can appear incorrectly in the final output.

---

## 🚀 Future Improvements

The project can be upgraded from a traditional OpenCV project to an AI-based computer vision system.

### Planned improvements

* 🤖 AI-based person segmentation
* 👤 Automatic human detection
* 🎨 Automatic cloak-color detection
* 🧠 Deep-learning segmentation
* 🎥 Video recording
* 📱 Web/mobile interface
* 🖥️ Graphical user interface
* ⚡ FPS monitoring
* 🎭 Better edge detection
* 🌈 Support for more colors
* 📷 Automatic background scanning
* 🔄 Dynamic background reconstruction

### Advanced Architecture

```text
                 Webcam
                    ↓
            Background Scan
                    ↓
              AI Detection
                    ↓
           Person Segmentation
                    ↓
              Person Mask
                    ↓
          Background Reconstruction
                    ↓
           Invisible Person Effect
                    ↓
             Live Video Output
```


## 💡 Real-World Applications

Although the project is primarily an educational visual-effect system, the underlying techniques are useful for:

* Augmented reality
* Virtual environments
* Background replacement
* Video effects
* Green-screen systems
* Human segmentation
* Computer vision research
* Interactive entertainment
* Virtual production

---

## 🎓 Learning Outcomes

Through this project, you learn:

* Python programming
* OpenCV
* NumPy
* Webcam programming
* Image processing
* HSV color space
* Binary masks
* Image segmentation
* Morphological operations
* Background subtraction/replacement
* Real-time computer vision

---

## 📌 Requirements

* Python 3.x
* Laptop/Desktop
* Working webcam
* OpenCV
* NumPy
* Colored cloth
* Stable camera position

---

## 👩‍💻 Author

**Rutuja Desai**

Information Technology Student

---

## 📜 License

This project is created for educational and academic purposes.
