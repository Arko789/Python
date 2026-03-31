"""
Camera Two-Person Detection
============================
Detects exactly two persons:
  - FIXED PERSON  : the reference person captured at startup (blue box)
  - MOVING PERSON : any new person entering the frame (green box)

Strategy:
1. Use OpenCV's built-in HOG person detector.
2. Capture a reference frame to identify the fixed person's position.
3. In live mode, match detected persons against the fixed person.
   Any unmatched person is labelled as MOVING PERSON.

Requirements:
    pip install opencv-python numpy
"""

import cv2
import numpy as np
import time


# ─── CONFIG ──────────────────────────────────────────────────────────────────
CAMERA_INDEX      = 0       # 0 = default webcam
REFERENCE_DELAY   = 3       # seconds before reference is captured
HOG_WIN_STRIDE    = (8, 8)  # HOG detection stride (smaller = more accurate, slower)
HOG_PADDING       = (8, 8)  # HOG padding
HOG_SCALE         = 1.05    # HOG scale factor
IOU_THRESHOLD     = 0.3     # overlap needed to match a person to the fixed person
# ─────────────────────────────────────────────────────────────────────────────


# ── HOG People Detector ───────────────────────────────────────────────────────
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


def detect_persons(frame: np.ndarray) -> list:
    """Return list of bounding boxes (x, y, w, h) for detected persons."""
    boxes, _ = hog.detectMultiScale(
        frame,
        winStride=HOG_WIN_STRIDE,
        padding=HOG_PADDING,
        scale=HOG_SCALE
    )
    return list(boxes) if len(boxes) > 0 else []


def compute_iou(boxA: tuple, boxB: tuple) -> float:
    """Compute Intersection over Union of two (x, y, w, h) boxes."""
    ax1, ay1 = boxA[0], boxA[1]
    ax2, ay2 = boxA[0] + boxA[2], boxA[1] + boxA[3]
    bx1, by1 = boxB[0], boxB[1]
    bx2, by2 = boxB[0] + boxB[2], boxB[1] + boxB[3]

    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    inter = max(0, ix2 - ix1) * max(0, iy2 - iy1)
    if inter == 0:
        return 0.0

    areaA = boxA[2] * boxA[3]
    areaB = boxB[2] * boxB[3]
    return inter / float(areaA + areaB - inter)


def draw_box(frame, box, label, color):
    """Draw a labelled bounding box on the frame."""
    x, y, w, h = box
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
    # Background rect for label
    (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
    cv2.rectangle(frame, (x, y - th - 8), (x + tw + 6, y), color, -1)
    cv2.putText(frame, label, (x + 3, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)


def countdown_overlay(frame: np.ndarray, seconds_left: float):
    """Display a semi-transparent countdown overlay."""
    h, w = frame.shape[:2]
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.45, frame, 0.55, 0, frame)
    msg1 = "Place FIXED PERSON in frame"
    msg2 = f"Capturing reference in {int(seconds_left) + 1}s ..."
    cv2.putText(frame, msg1, (w // 2 - 185, h // 2 - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 100), 2)
    cv2.putText(frame, msg2, (w // 2 - 175, h // 2 + 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.70, (100, 220, 255), 2)


def main():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open camera index {CAMERA_INDEX}")

    print("=" * 55)
    print("  Two-Person Detection: Fixed + Moving")
    print("=" * 55)
    print("  -> FIXED PERSON  : stays in frame from the start")
    print("  -> MOVING PERSON : enters the frame later")
    print(f"  -> Reference captured automatically in {REFERENCE_DELAY}s")
    print("  -> Press 'r' to re-capture reference | 'q' to quit\n")

    fixed_box         = None   # bounding box of the fixed person
    reference_captured = False
    ref_capture_time  = time.time() + REFERENCE_DELAY

    while True:
        ret, frame = cap.read()
        if not ret:
            print("  Frame read error — exiting.")
            break

        display = frame.copy()
        now     = time.time()

        # ── Phase 1: Countdown + capture reference ──────────────────────────
        if not reference_captured:
            remaining = ref_capture_time - now
            if remaining > 0:
                countdown_overlay(display, remaining)
            else:
                persons = detect_persons(frame)
                if persons:
                    # Pick the largest detected box as the fixed person
                    fixed_box = max(persons, key=lambda b: b[2] * b[3])
                    reference_captured = True
                    print("  [OK] Fixed person detected and locked.")
                    print("  -> Now bring the MOVING PERSON into frame.\n")
                else:
                    # No person found — retry in 1 second
                    print("  [!]  No person detected in reference frame. Retrying in 1s...")
                    ref_capture_time = time.time() + 1

        # ── Phase 2: Live detection ─────────────────────────────────────────
        else:
            persons = detect_persons(frame)

            fixed_found  = False
            moving_found = False

            for box in persons:
                iou = compute_iou(fixed_box, tuple(box))
                if iou >= IOU_THRESHOLD:
                    # This is the FIXED person
                    draw_box(display, box, "FIXED PERSON", (255, 100, 0))
                    fixed_found = True
                else:
                    # This is a NEW / MOVING person
                    draw_box(display, box, "MOVING PERSON", (0, 220, 80))
                    moving_found = True

            # Status text
            if moving_found:
                status_text  = "Moving person detected!"
                status_color = (0, 220, 80)
            elif fixed_found:
                status_text  = "Only fixed person visible"
                status_color = (200, 200, 200)
            else:
                status_text  = "No person detected"
                status_color = (100, 100, 255)

            cv2.putText(display, status_text, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, status_color, 2)
            cv2.putText(display,
                        "Blue=Fixed | Green=Moving | 'r'=Reset | 'q'=Quit",
                        (10, display.shape[0] - 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)

        cv2.imshow("Two-Person Detection", display)

        # ── Key handling ────────────────────────────────────────────────────
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("  Quit — goodbye.")
            break
        elif key == ord('r') and reference_captured:
            persons = detect_persons(frame)
            if persons:
                fixed_box = max(persons, key=lambda b: b[2] * b[3])
                print("  [OK] Reference re-captured.")
            else:
                print("  [!] No person in frame — reference not updated.")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()