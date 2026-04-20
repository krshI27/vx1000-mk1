"""Thin preset-app wrapper around `image_effects` filters.

The filter math lives in `image_effects` (shared across the workspace).
This module keeps only PIL I/O helpers and the bundled `process_frame`
orchestration that composes the four VX1000 filters in order.
"""

from io import BytesIO

import numpy as np
from PIL import Image
from image_effects import color_grade as _color_grade
from image_effects import fisheye_2d as _fisheye_2d
from image_effects import grain as _grain
from image_effects import vignette as _vignette


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


# Back-compat aliases for the old `processing.*` call-sites.
fisheye_distort = _fisheye_2d
apply_vignette = _vignette
apply_color = _color_grade
add_film_grain = _grain


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

    distorted = _fisheye_2d(frame, strength=strength, scale=scale)
    colored = _color_grade(
        distorted, contrast=contrast, saturation=saturation, exposure=exposure
    )
    vignetted = _vignette(colored, amount=vignette)
    grained = _grain(vignetted, amount=grain)
    return array_to_pil(grained)
