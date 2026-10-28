from pathlib import Path
import cv2
import numpy as np

# Duong dan theo vi tri file, khong phu thuoc thu muc terminal
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw"
OUT = ROOT / "outputs" / "week01"
WIDTH, HEIGHT = 640, 480
ROI = (145, 110, 350, 260)  # x, y, width, height


def save_image(path: Path, image: np.ndarray) -> None:
    if not cv2.imwrite(str(path), image):
        raise OSError(f"Khong luu duoc anh: {path}")


def create_demo_images() -> None:
    """Tao 2 anh cung mot tam kim loai: OK va NG."""
    DATA.mkdir(parents=True, exist_ok=True)
    base = np.full((HEIGHT, WIDTH, 3), 45, dtype=np.uint8)
    cv2.rectangle(base, (145, 110), (495, 370), (185, 190, 195), -1)
    cv2.rectangle(base, (160, 125), (480, 355), (195, 200, 210), -1)

    defect = base.copy()
    cv2.line(defect, (220, 165), (420, 285), (30, 30, 30), 3)
    cv2.circle(defect, (370, 215), 17, (95, 95, 95), -1)

    save_image(DATA / "product_ok_001.png", base)
    save_image(DATA / "product_ng_001.png", defect)


def load_image(path: Path) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Khong doc duoc anh: {path}")
    return image


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    # Chi tao anh demo khi chua du 2 anh dau vao
    if not (DATA / "product_ok_001.png").exists() or not (
        DATA / "product_ng_001.png"
    ).exists():
        create_demo_images()

    x, y, w, h = ROI
    gray_rois = {}

    for label in ("ok", "ng"):
        image = load_image(DATA / f"product_{label}_001.png")
        height, width, channels = image.shape

        if x < 0 or y < 0 or x + w > width or y + h > height:
            raise ValueError(f"ROI nam ngoai anh {label}")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        roi_color = image[y:y + h, x:x + w]
        gray_rois[label] = gray[y:y + h, x:x + w]

        save_image(OUT / f"{label}_gray.png", gray)
        save_image(OUT / f"{label}_roi.png", roi_color)

        print(
            f"{label.upper()}: shape={image.shape}, dtype={image.dtype}, "
            f"ROI={roi_color.shape}, "
            f"mean_gray={gray_rois[label].mean():.1f}"
        )

    # Phep toan nay chi MINH HOA su khac pixel,
    # KHONG du de ket luan san pham thuc te OK/NG
    difference = cv2.absdiff(gray_rois["ok"], gray_rois["ng"])
    save_image(OUT / "difference.png", difference)
    print(f"So pixel khac nhau trong ROI: {cv2.countNonZero(difference)}")
    print(f"Da luu ket qua vao: {OUT}")
    print("Luu y: absdiff chi minh hoa, CHUA phai bo kiem tra OK/NG.")


if __name__ == "__main__":
    main()