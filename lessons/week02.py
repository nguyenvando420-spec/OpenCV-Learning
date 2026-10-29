from pathlib import Path
import cv2
import numpy as np

# Dung lai du lieu da tao o Tuan 01, khong ghi de anh goc.
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw"
OUT = ROOT / "outputs" / "week02"

# ROI theo (x, y, width, height), phu hop anh demo 640x480.
ROIS = {
    "surface": (145, 110, 350, 260),
    "scratch_zone": (205, 150, 235, 160),
    "stain_zone": (340, 185, 70, 65),
}
COLORS = {
    "surface": (0, 255, 0),        # xanh la trong BGR
    "scratch_zone": (255, 0, 0),   # xanh duong trong BGR
    "stain_zone": (0, 165, 255),   # cam trong BGR
}
SAMPLE_POINTS = {
    "background": (40, 40),
    "metal": (180, 140),
    "scratch": (320, 225),
    "stain": (370, 215),
}


def load_image(path: Path) -> np.ndarray:
    if not path.exists():
        raise FileNotFoundError(
            f"Thieu anh {path}. Hay chay: python lessons/week01.py"
        )
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Anh bi hong/khong doc duoc: {path}")
    return image


def save_image(name: str, image: np.ndarray) -> None:
    path = OUT / name
    if image.size == 0 or not cv2.imwrite(str(path), image):
        raise OSError(f"Khong luu duoc: {path}")


def crop_roi(image: np.ndarray, rect: tuple[int, int, int, int]
             ) -> np.ndarray:
    x, y, w, h = rect
    height, width = image.shape[:2]
    if w <= 0 or h <= 0 or x < 0 or y < 0:
        raise ValueError(f"ROI khong hop le: {rect}")
    if x + w > width or y + h > height:
        raise ValueError(
            f"ROI {rect} vuot anh width={width}, height={height}"
        )
    return image[y:y + h, x:x + w].copy()


def resize_keep_ratio(image: np.ndarray, target_width: int
                      ) -> np.ndarray:
    if target_width <= 0:
        raise ValueError("target_width phai > 0")
    height, width = image.shape[:2]
    target_height = max(1, round(height * target_width / width))
    interpolation = (
        cv2.INTER_AREA if target_width < width else cv2.INTER_LINEAR
    )
    return cv2.resize(
        image, (target_width, target_height),
        interpolation=interpolation
    )


def inspect_image(label: str) -> None:
    image = load_image(DATA / f"product_{label}_001.png")
    height, width = image.shape[:2]

    # BGR la dang anh ma OpenCV doc duoc.
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    print(f"\n=== {label.upper()} ===")
    print(f"shape={image.shape}, dtype={image.dtype}")
    for point_name, (x, y) in SAMPLE_POINTS.items():
        if not (0 <= x < width and 0 <= y < height):
            raise ValueError(f"Diem mau {point_name} nam ngoai anh")
        print(
            f"{point_name} (x={x}, y={y}): "
            f"BGR={image[y, x].tolist()} | "
            f"RGB={rgb[y, x].tolist()} | "
            f"HSV={hsv[y, x].tolist()} | gray={int(gray[y, x])}"
        )

    # Ve tren BAN SAO: anh dau vao khong bi sua.
    annotated = image.copy()
    for roi_name, rect in ROIS.items():
        x, y, w, h = rect
        roi = crop_roi(image, rect)
        save_image(f"{label}_{roi_name}.png", roi)

        color = COLORS[roi_name]
        cv2.rectangle(
            annotated, (x, y), (x + w - 1, y + h - 1),
            color, 2
        )
        cv2.putText(
            annotated, roi_name, (x, max(20, y - 8)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.52, color, 2
        )
        print(f"ROI {roi_name}: {roi.shape}")

    surface = crop_roi(image, ROIS["surface"])
    surface_gray = cv2.cvtColor(surface, cv2.COLOR_BGR2GRAY)
    surface_hsv = cv2.cvtColor(surface, cv2.COLOR_BGR2HSV)
    surface_saturation = surface_hsv[:, :, 1]  # Kenh S, khong phai anh mau
    blue, green, red = cv2.split(surface)

    save_image(f"{label}_annotated.png", annotated)
    save_image(f"{label}_surface_gray.png", surface_gray)
    save_image(f"{label}_surface_saturation.png", surface_saturation)
    save_image(f"{label}_channel_b.png", blue)
    save_image(f"{label}_channel_g.png", green)
    save_image(f"{label}_channel_r.png", red)
    save_image(f"{label}_preview_320.png",
               resize_keep_ratio(annotated, 320))

    # cv2.imwrite nhan BGR. Chuyen RGB ve BGR truoc khi luu.
    roundtrip = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    assert np.array_equal(roundtrip, image)
    save_image(f"{label}_rgb_roundtrip.png", roundtrip)

    mean_bgr = surface.mean(axis=(0, 1))
    print("Mean BGR in surface:",
          [round(float(value), 2) for value in mean_bgr])


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for label in ("ok", "ng"):
        inspect_image(label)
    print(f"\nKet qua luu tai: {OUT}")
    print("Luu y: ROI la vung chon TRUOC, chua phat hien vet xuoc tu dong.")


if __name__ == "__main__":
    main()