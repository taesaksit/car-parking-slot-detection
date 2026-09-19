# YOLO Parking Slot Detection
Real-time parking slot occupancy detection system using YOLO OBB and OpenCV.  
#### Demo: https://youtu.be/AGb9QHHth04?si=ldsbL6ty-3ndCXaY
---
## Workflow / ขั้นตอนการทำงาน
1. **Label data from CVAT**
2. **Create spot center** 
3. **Train model** 
---
## Training Results
![Training Results](results.png)
![YOLo Results](result-detected.png)

## Folder Structure
``` 📦 YOLO Parking Space Detector
├── 📂 dataset/
│   ├── 📄 data.yaml
│   ├── 📂 images/train/ (frame_*.jpg)
│   └── 📂 labels/train/ (frame_*.txt)
├── 📂 runs/obb/train/        # ผลลัพธ์จากการ Train (Weights & Metrics)
├── 📂 utils/                # สคริปต์ช่วยเตรียมข้อมูลและแปลงไฟล์
│   ├── convert_coco.py
│   ├── create_slot_center.py
│   └── prepare_vdotoimg.py
├── 📄 main.py               # ไฟล์รันระบบหลัก (Real-time Detection)
├── 📄 train.py              # ไฟล์สำหรับเทรนโมเดล YOLO OBB
├── 📄 parking_slots_center.json # ไฟล์พิกัดจุดศูนย์กลางช่องจอด
├── 📄 requirements.txt
├── 🎥 carparking.mp4        # วิดีโอต้นทาง
├── 🎥 carparking-output.mp4 # วิดีโอผลลัพธ์
└── 📄 README.md ```
