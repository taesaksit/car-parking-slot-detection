import cv2
import os


# ฟังชันนี้คือการแคปรูปจาก VDO ตามจำนวนที่เราต้องการเพื่อนำไป label โดยใช้ CVAT
# Optimize โดยลูกพี่ claude เรียบร้อยโคตรเร็วจัด


def extract_custom_frames(
    video_path,
    output_folder="dataset_custom_frames",
    num_frames=5,
):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: ไม่สามารถเปิดไฟล์วิดีโอได้")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames <= 0:
        print("Error: ไม่สามารถอ่านจำนวนเฟรมของวิดีโอได้")
        cap.release()
        return

    num_frames = min(num_frames, total_frames)
    interval = total_frames / num_frames
    target_frames = {int(i * interval) for i in range(num_frames)}

    print(
        f"วิดีโอนี้มีทั้งหมด {total_frames} เฟรม | ต้องการ {num_frames} ภาพ "
        f"(เฉลี่ยทุกๆ {interval:.1f} เฟรม)"
    )

    saved_count = 0
    current_frame = 0

    while saved_count < len(target_frames):
        ret = cap.grab()
        if not ret:
            break

        if current_frame in target_frames:
            ret, frame = cap.retrieve()
            if ret:
                file_name = os.path.join(
                    output_folder, f"frame_{saved_count + 1:03d}.jpg"
                )
                cv2.imwrite(file_name, frame)
                print(f"บันทึก: {file_name} (ที่เฟรม {current_frame})")
                saved_count += 1

        current_frame += 1

    cap.release()
    print(f"{saved_count} รูป ในโฟลเดอร์ '{output_folder}'")


if __name__ == "__main__":
    video_file = "carparking.mp4"
    DESIRED_FRAMES = 200

    extract_custom_frames(
        video_file,
        output_folder="dataset_frames",
        num_frames=DESIRED_FRAMES,
    )
