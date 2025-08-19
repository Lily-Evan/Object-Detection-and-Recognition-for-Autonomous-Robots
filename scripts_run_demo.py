import argparse
import cv2
from detection.detector import YOLODetector

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="yolov5", help="Model type")
    parser.add_argument("--source", type=str, default="0", help="Camera index or video file")
    parser.add_argument("--device", type=str, default="cpu", help="cpu or cuda")
    args = parser.parse_args()

    if args.source.isdigit():
        cap = cv2.VideoCapture(int(args.source))
    else:
        cap = cv2.VideoCapture(args.source)

    detector = YOLODetector(device=args.device)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detections = detector.detect(frame)
        frame = detector.draw_detections(frame, detections)

        cv2.imshow("Object Detection", frame)
        key = cv2.waitKey(1)
        if key == 27:  # ESC
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()