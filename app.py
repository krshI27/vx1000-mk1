import numpy as np
import streamlit as st
from PIL import Image

import processing

st.set_page_config(page_title="VX1000 Fisheye Simulator", layout="wide")
st.title("VX1000 Fisheye Simulator")
st.write(
    "Upload an image and apply a skateboard fisheye distortion with VX1000-inspired color and film styling."
)

with st.sidebar:
    st.header("Controls")
    preset = st.selectbox(
        "Preset",
        ["Default", "Classic VX1000", "Soft Skate", "High Contrast"],
    )
    strength = st.slider("Lens strength", 0.0, 1.5, 0.9, 0.05)
    scale = st.slider("Image scale", 0.4, 1.0, 0.98, 0.01)
    vignette = st.slider("Vignette", 0.0, 1.0, 0.36, 0.05)
    contrast = st.slider("Contrast", 0.5, 1.6, 1.15, 0.05)
    saturation = st.slider("Saturation", 0.6, 1.6, 1.15, 0.05)
    exposure = st.slider("Exposure", -0.5, 0.5, 0.0, 0.05)
    grain = st.slider("Grain", 0.0, 0.5, 0.12, 0.02)

if preset != "Default":
    if preset == "Classic VX1000":
        strength, scale, vignette, contrast, saturation, exposure, grain = (
            1.05,
            0.94,
            0.48,
            1.25,
            1.20,
            0.04,
            0.18,
        )
    elif preset == "Soft Skate":
        strength, scale, vignette, contrast, saturation, exposure, grain = (
            0.72,
            1.00,
            0.30,
            1.05,
            1.10,
            0.02,
            0.10,
        )
    elif preset == "High Contrast":
        strength, scale, vignette, contrast, saturation, exposure, grain = (
            1.10,
            0.92,
            0.42,
            1.40,
            1.25,
            0.08,
            0.20,
        )

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png", "bmp", "tiff"],
)

if uploaded_file is not None:
    original_image = Image.open(uploaded_file).convert("RGB")
    original_array = np.array(original_image)

    processed_image = processing.process_frame(
        original_array,
        strength=strength,
        scale=scale,
        vignette=vignette,
        contrast=contrast,
        saturation=saturation,
        exposure=exposure,
        grain=grain,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original")
        st.image(original_image, use_container_width=True)
    with col2:
        st.subheader("Processed")
        st.image(processed_image, use_container_width=True)

    buffer = processing.pil_image_to_bytes(processed_image)
    st.download_button(
        "Download processed image",
        data=buffer,
        file_name="vx1000_result.png",
        mime="image/png",
    )
else:
    st.info("Upload an image to preview the VX1000 fisheye effect.")
