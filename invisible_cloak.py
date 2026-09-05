import cv2
import numpy as np
import time
import os

# ============================================================
# INVISIBLE PERSON / INVISIBILITY CLOAK PROJECT
# ============================================================

# ------------------------------------------------------------
# SETTINGS
# ------------------------------------------------------------

CAMERA_INDEX = 0

# Background file
BACKGROUND_FILE = "background.jpg"

# Number of frames used to calculate the background
BACKGROUND_FRAMES = 30

# ------------------------------------------------------------
# OPEN WEBCAM
# ------------------------------------------------------------

cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    print("ERROR: Could not open webcam.")
    exit()

# Set camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

print("=" * 60)
print("     INVISIBLE PERSON PROJECT")
print("=" * 60)

print("\nControls:")
print("B -> Capture background")
print("R -> Use RED cloak")
print("G -> Use GREEN cloak")
print("Y -> Use YELLOW cloak")
print("S -> Save current invisible frame")
print("Q -> Quit")

# ------------------------------------------------------------
# VARIABLES
# ------------------------------------------------------------

background = None

cloak_color = "red"

# ------------------------------------------------------------
# FUNCTION: CAPTURE BACKGROUND
# ------------------------------------------------------------

def capture_background():

    print("\nPreparing to capture background...")

    frames = []

    # Countdown
    for i in range(3, 0, -1):

        print(f"Background capture starts in {i}...")

        start_time = time.time()

        while time.time() - start_time < 1:

            ret, frame = cap.read()

            if not ret:
                continue

            display_frame = frame.copy()

            cv2.putText(
                display_frame,
                f"GET READY: {i}",
                (50, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (0, 255, 255),
                3
            )

            cv2.imshow("Invisible Person", display_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                exit()

    print("Capturing background...")

    for i in range(BACKGROUND_FRAMES):

        ret, frame = cap.read()

        if ret:
            frames.append(frame)

        cv2.imshow("Invisible Person", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            exit()

    if len(frames) == 0:
        print("ERROR: Could not capture background.")
        return None

    # Median gives a cleaner background
    bg = np.median(frames, axis=0).astype(np.uint8)

    cv2.imwrite(BACKGROUND_FILE, bg)

    print("Background captured successfully!")
    print(f"Saved as: {BACKGROUND_FILE}")

    return bg


# ------------------------------------------------------------
# FUNCTION: CREATE COLOR MASK
# ------------------------------------------------------------

def create_mask(frame, color):

    # Convert BGR image to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # --------------------------------------------------------
    # RED
    # --------------------------------------------------------

    if color == "red":

        # Red wraps around HSV hue range
        lower_red1 = np.array([0, 100, 70])
        upper_red1 = np.array([10, 255, 255])

        lower_red2 = np.array([170, 100, 70])
        upper_red2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(
            hsv,
            lower_red1,
            upper_red1
        )

        mask2 = cv2.inRange(
            hsv,
            lower_red2,
            upper_red2
        )

        mask = mask1 + mask2

    # --------------------------------------------------------
    # GREEN
    # --------------------------------------------------------

    elif color == "green":

        lower_green = np.array([35, 80, 50])
        upper_green = np.array([85, 255, 255])

        mask = cv2.inRange(
            hsv,
            lower_green,
            upper_green
        )

    # --------------------------------------------------------
    # YELLOW
    # --------------------------------------------------------

    elif color == "yellow":

        lower_yellow = np.array([20, 100, 80])
        upper_yellow = np.array([35, 255, 255])

        mask = cv2.inRange(
            hsv,
            lower_yellow,
            upper_yellow
        )

    else:

        mask = np.zeros(
            frame.shape[:2],
            dtype=np.uint8
        )

    # --------------------------------------------------------
    # REMOVE SMALL NOISE
    # --------------------------------------------------------

    kernel = np.ones((5, 5), np.uint8)

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel
    )

    # --------------------------------------------------------
    # FILL SMALL HOLES
    # --------------------------------------------------------

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    # --------------------------------------------------------
    # BLUR MASK
    # --------------------------------------------------------

    mask = cv2.GaussianBlur(
        mask,
        (7, 7),
        0
    )

    return mask


# ------------------------------------------------------------
# FUNCTION: CREATE INVISIBLE EFFECT
# ------------------------------------------------------------

def create_invisible_effect(frame, background, mask):

    # Convert mask from 0-255 to 0-1
    mask_float = mask.astype(float) / 255.0

    # Make 3-channel mask
    mask_3 = np.dstack([
        mask_float,
        mask_float,
        mask_float
    ])

    # Background where cloak is detected
    background_part = (
        background.astype(float) * mask_3
    )

    # Original frame where cloak is not detected
    foreground_part = (
        frame.astype(float) * (1 - mask_3)
    )

    # Combine
    result = background_part + foreground_part

    result = np.clip(
        result,
        0,
        255
    ).astype(np.uint8)

    return result


# ------------------------------------------------------------
# LOAD EXISTING BACKGROUND IF AVAILABLE
# ------------------------------------------------------------

if os.path.exists(BACKGROUND_FILE):

    background = cv2.imread(
        BACKGROUND_FILE
    )

    if background is not None:

        print(
            f"\nExisting background found: "
            f"{BACKGROUND_FILE}"
        )

        print(
            "Press B if you want to capture a new background."
        )


# ------------------------------------------------------------
# MAIN LOOP
# ------------------------------------------------------------

while True:

    ret, frame = cap.read()

    if not ret:

        print("ERROR: Could not read webcam.")
        break

    # Flip camera for mirror effect
    frame = cv2.flip(frame, 1)

    display = frame.copy()

    # --------------------------------------------------------
    # IF BACKGROUND HAS NOT BEEN CAPTURED
    # --------------------------------------------------------

    if background is None:

        cv2.putText(
            display,
            "Press B to capture background",
            (40, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )

        cv2.putText(
            display,
            "Stand away from camera",
            (40, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

    # --------------------------------------------------------
    # BACKGROUND EXISTS
    # --------------------------------------------------------

    else:

        # Make sure dimensions match
        if background.shape != frame.shape:

            background = cv2.resize(
                background,
                (frame.shape[1], frame.shape[0])
            )

        # Create cloak mask
        mask = create_mask(
            frame,
            cloak_color
        )

        # Create invisible effect
        display = create_invisible_effect(
            frame,
            background,
            mask
        )

        # ----------------------------------------------------
        # DISPLAY STATUS
        # ----------------------------------------------------

        cv2.putText(
            display,
            f"CLOAK: {cloak_color.upper()}",
            (30, 45),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.putText(
            display,
            "B: Background | R/G/Y: Cloak | S: Save | Q: Quit",
            (30, display.shape[0] - 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

    # --------------------------------------------------------
    # SHOW CAMERA
    # --------------------------------------------------------

    cv2.imshow(
        "Invisible Person",
        display
    )

    # --------------------------------------------------------
    # KEYBOARD CONTROLS
    # --------------------------------------------------------

    key = cv2.waitKey(1) & 0xFF

    # Quit
    if key == ord('q'):

        break

    # Capture background
    elif key == ord('b'):

        background = capture_background()

    # Red cloak
    elif key == ord('r'):

        cloak_color = "red"

        print("Cloak color changed to RED")

    # Green cloak
    elif key == ord('g'):

        cloak_color = "green"

        print("Cloak color changed to GREEN")

    # Yellow cloak
    elif key == ord('y'):

        cloak_color = "yellow"

        print("Cloak color changed to YELLOW")

    # Save image
    elif key == ord('s'):

        filename = (
            f"invisible_{int(time.time())}.jpg"
        )

        cv2.imwrite(
            filename,
            display
        )

        print(
            f"Saved invisible image: {filename}"
        )


# ------------------------------------------------------------
# RELEASE
# ------------------------------------------------------------

cap.release()

cv2.destroyAllWindows()

print("\nProgram ended.")