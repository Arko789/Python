'''
Camera Two-Person Detection
============================
Detects exactly two persons:
  - FIXED PERSON  : the reference person captured at startup (blue box)
  - MOVING PERSON : any new person entering the frame (green box)

Strategy:
1. Use OpenCV's built-in HOG person detector.
2. Capture a reference frame to identify the fixed person's position.
3. In live mode, keep matching detections against the last known fixed person box.
   Any unmatched person is labelled as MOVING PERSON.

Requirements:
    pip install opencv-python numpy
'''

import cv2
import numpy as np
import time


CAMERA_INDEX = 0
REFERENCE_DELAY = 3
HOG_WIN_STRIDE = (8, 8)
HOG_PADDING = (8, 8)
HOG_SCALE = 1.05
IOU_THRESHOLD = 0.3
DIST_THRESHOLD = 120
BLUE_BOX = (255, 0, 0)
GREEN_BOX = (0, 255, 0)


hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
fullbody_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")
upperbody_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_upperbody.xml")


def detect_persons(frame: np.ndarray) -> list:
    """Return list of bounding boxes (x, y, w, h) for detected persons."""
    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    boxes, weights = hog.detectMultiScale(
        frame,
        winStride=HOG_WIN_STRIDE,
        padding=HOG_PADDING,
        scale=HOG_SCALE,
    )
    candidate_boxes = [tuple(box) for box in boxes] if len(boxes) > 0 else []
    candidate_weights = [float(w) for w in np.array(weights).flatten()] if len(boxes) > 0 else []

    fullbody_boxes = fullbody_cascade.detectMultiScale(
        gray,
        scaleFactor=1.05,
        minNeighbors=3,
        minSize=(60, 120),
    )
    for box in fullbody_boxes:
        candidate_boxes.append(tuple(int(v) for v in box))
        candidate_weights.append(1.2)

    upperbody_boxes = upperbody_cascade.detectMultiScale(
        gray,
        scaleFactor=1.05,
        minNeighbors=4,
        minSize=(60, 60),
    )
    for (x, y, w, h) in upperbody_boxes:
        candidate_boxes.append((int(x), int(y), int(w), int(h * 2.1)))
        candidate_weights.append(0.9)

    if not candidate_boxes:
        return []

    boxes_list = [list(box) for box in candidate_boxes]
    kept_indices = cv2.dnn.NMSBoxes(boxes_list, candidate_weights, 0.0, 0.35)
    if len(kept_indices) == 0:
        return candidate_boxes

    return [tuple(boxes_list[int(idx)]) for idx in np.array(kept_indices).flatten()]


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


def box_center(box: tuple) -> tuple:
    """Return the center point of an (x, y, w, h) box."""
    x, y, w, h = box
    return (x + w / 2.0, y + h / 2.0)


def center_distance(boxA: tuple, boxB: tuple) -> float:
    """Return Euclidean distance between the centers of two boxes."""
    ax, ay = box_center(boxA)
    bx, by = box_center(boxB)
    return ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5


def draw_box(frame, box, label, color):
    """Draw a labelled bounding box on the frame."""
    x, y, w, h = box
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
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

    fixed_box = None
    reference_captured = False
    ref_capture_time = time.time() + REFERENCE_DELAY

    while True:
        ret, frame = cap.read()
        if not ret:
            print("  Frame read error - exiting.")
            break

        frame = cv2.resize(frame, (640, 480))

        display = frame.copy()
        now = time.time()

        if not reference_captured:
            remaining = ref_capture_time - now
            if remaining > 0:
                countdown_overlay(display, remaining)
            else:
                persons = detect_persons(frame)
                if len(persons) == 1:
                    fixed_box = persons[0]
                    reference_captured = True
                    print("  [OK] Fixed person detected and locked.")
                    print("  -> Now bring the MOVING PERSON into frame.\n")
                elif len(persons) > 1:
                    print("  [!]  Multiple persons detected. Keep only the fixed person in frame.")
                    ref_capture_time = time.time() + 1
                else:
                    print("  [!]  No person detected in reference frame. Retrying in 1s...")
                    ref_capture_time = time.time() + 1
        else:
            persons = detect_persons(frame)
            fixed_found = False
            moving_found = False
            matched_fixed = None
            moving_box = None

            if persons and fixed_box is not None:
                best_box = None
                best_score = None

                for box in persons:
                    iou = compute_iou(fixed_box, box)
                    distance = center_distance(fixed_box, box)
                    score = (iou, -distance)
                    if best_score is None or score > best_score:
                        best_score = score
                        best_box = box

                if best_box is not None:
                    best_iou = compute_iou(fixed_box, best_box)
                    best_distance = center_distance(fixed_box, best_box)
                    if len(persons) == 1 or best_iou >= IOU_THRESHOLD or best_distance <= DIST_THRESHOLD:
                        matched_fixed = best_box
                        fixed_box = matched_fixed
                        draw_box(display, matched_fixed, "FIXED PERSON", BLUE_BOX)
                        fixed_found = True

            for box in persons:
                if matched_fixed is not None and box == matched_fixed:
                    continue

                if moving_box is None or (box[2] * box[3]) > (moving_box[2] * moving_box[3]):
                    moving_box = box

            if moving_box is not None:
                draw_box(display, moving_box, "MOVING PERSON", GREEN_BOX)
                moving_found = True

            if moving_found:
                status_text = "Moving person detected!"
                status_color = GREEN_BOX
            elif fixed_found:
                status_text = "Only fixed person visible"
                status_color = (200, 200, 200)
            else:
                status_text = "No person detected"
                status_color = (100, 100, 255)

            cv2.putText(display, status_text, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, status_color, 2)
            cv2.putText(display,
                        "Blue=Fixed | Green=Moving | 'r'=Reset | 'q'=Quit",
                        (10, display.shape[0] - 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)

        cv2.imshow("Two-Person Detection", display)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            print("  Quit - goodbye.")
            break
        elif key == ord("r") and reference_captured:
            persons = detect_persons(frame)
            if len(persons) == 1:
                fixed_box = persons[0]
                print("  [OK] Reference re-captured.")
            elif len(persons) > 1:
                print("  [!] Multiple persons detected - keep only the fixed person for reset.")
            else:
                print("  [!] No person in frame - reference not updated.")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()