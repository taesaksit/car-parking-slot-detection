import json
import cv2
import numpy as np

parking_slots = []
frame_display = None


# หมายเหตุ: ฟังก์ชันนี้สามารถใช้ CVAT แทนได้
def mouse_click(event, x, y, flags, param):
    global parking_slots, frame_display

    # เมื่อคลิกซ้าย 1 ครั้ง จะถือว่าเป็นจุดศูนย์กลางของ 1 ช่องจอด
    if event == cv2.EVENT_LBUTTONDOWN:
        slot_id = len(parking_slots) + 1
        parking_slots.append(
            {
                "id": slot_id,
                "center": [x, y],
            }
        )
        print(f"Added Slot ID {slot_id} at center: ({x}, {y})")

        # วาดวงกลมและตัวเลข ID ลงบนภาพเพื่อให้เห็นตำแหน่งชัดเจน
        cv2.circle(frame_display, (x, y), 6, (0, 0, 255), -1)
        cv2.putText(
            frame_display,
            str(slot_id),
            (x + 8, y + 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            2,
        )


def main():
    global frame_display

    video_path = "carparking.mp4"
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: ไม่สามารถเปิดไฟล์วิดีโอได้ที่ {video_path}")
        return

    # อ่านภาพเฟรมแรกมาใช้เป็นพื้นหลัง
    ret, frame = cap.read()
    if not ret:
        print("Error: ไม่สามารถอ่านเฟรมแรกจากวิดีโอได้")
        return

    frame_display = frame.copy()
    cap.release()

    cv2.imshow("Select Parking Center", frame_display)
    cv2.setMouseCallback("Select Parking Center", mouse_click)

    print("--- วิธีกดใช้งาน ---")
    print("1. คลิกซ้าย 1 ครั้ง ตรงกลาง (Center) ของแต่ละช่องจอด")
    print("2. ทำซ้ำจนครบทุกช่องจอด")
    print("3. กดปุ่ม 's' บนคีย์บอร์ดเพื่อบันทึกและปิดโปรแกรม")

    while True:
        cv2.imshow("Select Parking Center", frame_display)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):
            with open("parking_slots_center.json", "w", encoding="utf-8") as f:
                json.dump(parking_slots, f, indent=4)
            print(
                f"บันทึกจุดศูนย์กลางช่องจอดทั้งหมด {len(parking_slots)} ช่อง ลงในไฟล์ 'parking_slots_center.json' เรียบร้อยแล้ว!"
            )
            break
        elif key == ord("q"):
            print("ยกเลิกการทำงาน ไม่ได้บันทึกข้อมูล")
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
