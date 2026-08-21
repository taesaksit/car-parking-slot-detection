import os
import json
import cv2
import numpy as np
from ultralytics import YOLO


def load_parking_slots(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)


def draw_text(frame, text, pos_x, color, y, font_scale):
    font = cv2.FONT_HERSHEY_SIMPLEX
    thickness = 2
    cv2.putText(frame, text, (pos_x, y), font, font_scale, color, thickness)
    (text_w, _), _ = cv2.getTextSize(text, font, font_scale, thickness)
    return pos_x + text_w


def init_video_writer(cap, output_path):
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter.fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    return out


def validate_paths(model_path, json_path, video_path):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Error: ไม่พบไฟล์ Model ที่ path: {model_path}")
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Error: ไม่พบไฟล์ JSON ช่องจอดที่ path: {json_path}")
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Error: ไม่พบไฟล์วิดีโอต้นทางที่ path: {video_path}")


def main(model_path, json_path, video_path, output_path):

    validate_paths(model_path, json_path, video_path)
    model = YOLO(model_path)
    slots = load_parking_slots(json_path)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Error: ไม่สามารถเปิดไฟล์วิดีโอได้ที่ {video_path}")

    out = init_video_writer(cap, output_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model.track(
            source=frame,
            persist=True,
            device=0,
            verbose=False,
            # iou=0.4,
            # conf=0.7,
        )
        car_boxes = []
        if results[0].obb is not None and results[0].obb.xyxyxyxy is not None:
            car_boxes = results[0].obb.xyxyxyxy.cpu().numpy()

        available_count = 0
        occupied_count = 0
        total_slots = len(slots)

        for slot in slots:
            slot_id = slot["id"]
            cx, cy = slot["center"]
            is_occupied = False

            for box in car_boxes:
                pts = np.array(box, dtype=np.float32)
                result = cv2.pointPolygonTest(pts, (float(cx), float(cy)), False)
                if result >= 0:
                    is_occupied = True
                    break

            if is_occupied:
                occupied_count += 1
                color = (0, 0, 255)
            else:
                available_count += 1
                color = (0, 255, 0)

            dot_radius = 17
            border_thickness = 3
            cv2.circle(frame, (cx, cy), dot_radius, color, -1)
            cv2.circle(frame, (cx, cy), dot_radius, (255, 255, 255), border_thickness)
            draw_text(frame, str(slot_id), cx - 10, (0, 0, 0), cy + 5, font_scale=0.5)

        if results[0].obb is not None:
            frame = results[0].plot(
                line_width=4,
                labels=False,
                conf=False,
                font_size=1,
            )

        x, y = 30, 50
        x = draw_text(frame, f"Total: {total_slots}", x, (255, 0, 0), y, 1)
        x = draw_text(frame, "  |  ", x, (255, 255, 255), y, 1)
        x = draw_text(frame, f"Available: {available_count}", x, (0, 255, 0), y, 1)
        x = draw_text(frame, "  |  ", x, (255, 255, 255), y, 1)
        x = draw_text(frame, f"Occupied: {occupied_count}", x, (0, 0, 255), y, 1)

        out.write(frame)
        cv2.imshow("ํYOLO AI-Parking ", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main(
        model_path="runs/obb/train/weights/best.pt",
        json_path="parking_slots_center.json",
        video_path="carparking.mp4",
        output_path="output_parking.mp4",
    )
