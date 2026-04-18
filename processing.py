from io import BytesIO

import cv2
import numpy as np
from PIL import Image


def pil_to_array(image: Image.Image) -> np.ndarray:
    return np.array(image.convert("RGB"))


def array_to_pil(array: np.ndarray) -> Image.Image:
    clipped = np.clip(array, 0, 255).astype(np.uint8)
    return Image.fromarray(clipped)


def pil_image_to_bytes(image: Image.Image) -> bytes:
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()


def fisheye_distort(
    image: np.ndarray,
    strength: float = 0.9,
    scale: float = 0.98,
) -> np.ndarray:
    height, width = image.shape[:2]
    center_x = width / 2.0
    center_y = height / 2.0

    xv, yv = np.meshgrid(
        np.linspace(0, width - 1, width),
        np.linspace(0, height - 1, height),
    )
    x = xv - center_x
    y = yv - center_y
    radius = np.sqrt(x * x + y * y)
    max_radius = np.sqrt(center_x**2 + center_y**2)
    r_norm = radius / max_radius

    factor = 1.0 + strength * (r_norm**2)
    x_distorted = center_x + x * factor * scale
    y_distorted = center_y + y * factor * scale

    map_x = x_distorted.astype(np.float32)
    map_y = y_distorted.astype(np.float32)

    warped = cv2.remap(
        image,
        map_x,
        map_y,
        interpolation=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0),
    )
    return warped


def apply_vignette(image: np.ndarray, amount: float = 0.35) -> np.ndarray:
    height, width = image.shape[:2]
    x = np.linspace(-1.0, 1.0, width)
    y = np.linspace(-1.0, 1.0, height)
    xv, yv = np.meshgrid(x, y)
    mask = 1.0 - amount * np.power(xv**2 + yv**2, 1.2)
    mask = np.clip(mask, 0.0, 1.0)
    return (image.astype(np.float32) * mask[..., np.newaxis]).astype(np.uint8)


def apply_color(
    image: np.ndarray,
    contrast: float = 1.15,
    saturation: float = 1.15,
    exposure: float = 0.0,
) -> np.ndarray:
    normalized = image.astype(np.float32) / 255.0
    normalized = np.clip(normalized + exposure, 0.0, 1.0)
    normalized = np.clip((normalized - 0.5) * contrast + 0.5, 0.0, 1.0)

    hsv = cv2.cvtColor((normalized * 255).astype(np.uint8), cv2.COLOR_RGB2HSV).astype(
        np.float32
    )
    hsv[..., 1] = np.clip(hsv[..., 1] * saturation, 0, 255)
    colored = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
    return colored


def add_film_grain(image: np.ndarray, amount: float = 0.12) -> np.ndarray:
    if amount <= 0:
        return image
    noise = np.random.normal(loc=0.0, scale=255.0 * amount, size=image.shape)
    noisy = image.astype(np.float32) + noise
    return np.clip(noisy, 0, 255).astype(np.uint8)


def process_frame(
    frame,
    strength: float = 0.9,
    scale: float = 0.98,
    vignette: float = 0.35,
    contrast: float = 1.15,
    saturation: float = 1.15,
    exposure: float = 0.0,
    grain: float = 0.12,
) -> Image.Image:
    if isinstance(frame, Image.Image):
        frame = pil_to_array(frame)

    distorted = fisheye_distort(frame, strength=strength, scale=scale)
    colored = apply_color(
        distorted,
        contrast=contrast,
        saturation=saturation,
        exposure=exposure,
    )
    vignetted = apply_vignette(colored, amount=vignette)
    grained = add_film_grain(vignetted, amount=grain)
    return array_to_pil(grained)
