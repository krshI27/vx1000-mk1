import json
import urllib.parse

import numpy as np
import streamlit as st
from PIL import Image

import processing

st.set_page_config(page_title="VX1000 Fisheye Simulator", layout="wide")

st.markdown(
    """<style>
    .stApp { background-color: #E7DED2 !important; color: #30360F !important; }
    header[data-testid="stHeader"] { background-color: #E7DED2 !important; }
    section[data-testid="stSidebar"] { background-color: #DDD3C5 !important; padding-top: 16px !important; }
    [data-testid="stSidebar"] h3 {
        color: #CB411B !important; font-size: 18px !important; font-weight: 600 !important;
        letter-spacing: 0.5px !important; padding-bottom: 8px !important;
        border-bottom: 2px solid rgba(203,65,27,0.3) !important;
        margin-top: 24px !important; margin-bottom: 12px !important;
    }
    [data-testid="stSidebar"] hr { border-color: rgba(203,65,27,0.4) !important; }
    .stButton > button {
        background: linear-gradient(135deg, #CB411B 0%, #945029 100%) !important;
        color: white !important; border: none !important; border-radius: 6px !important;
        box-shadow: 0 2px 4px rgba(203,65,27,0.3) !important; transition: all 0.2s ease !important;
    }
    .stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 4px 8px rgba(203,65,27,0.4) !important; }
    [data-testid="stToggle"] input:checked + div { background-color: #CB411B !important; }
    .stCaption, [data-testid="stCaptionContainer"] { color: #945029 !important; }
    a { color: #945029 !important; }
    button:focus-visible { outline: 2px solid #CB411B !important; outline-offset: 2px !important; }
    [data-testid="stSpinner"] { color: #CB411B !important; }
    footer { display: none !important; }
    </style>""",
    unsafe_allow_html=True,
)

DEFAULTS = {
    "preset": "Default",
    "strength": 0.9,
    "scale": 0.98,
    "vignette": 0.36,
    "contrast": 1.15,
    "saturation": 1.15,
    "exposure": 0.0,
    "grain": 0.12,
}

PRESET_OVERRIDES = {
    "Classic VX1000": {
        "strength": 1.05, "scale": 0.94, "vignette": 0.48,
        "contrast": 1.25, "saturation": 1.20, "exposure": 0.04, "grain": 0.18,
    },
    "Soft Skate": {
        "strength": 0.72, "scale": 1.00, "vignette": 0.30,
        "contrast": 1.05, "saturation": 1.10, "exposure": 0.02, "grain": 0.10,
    },
    "High Contrast": {
        "strength": 1.10, "scale": 0.92, "vignette": 0.42,
        "contrast": 1.40, "saturation": 1.25, "exposure": 0.08, "grain": 0.20,
    },
}


def _load_preset() -> None:
    preset_raw = st.query_params.get("preset")
    if not preset_raw:
        return
    preset_text = preset_raw[0] if isinstance(preset_raw, list) else preset_raw
    try:
        preset = json.loads(preset_text)
        for key, value in preset.get("params", {}).items():
            if key in DEFAULTS:
                st.session_state.setdefault(key, value)
    except (json.JSONDecodeError, TypeError, AttributeError):
        pass


def _preset_url() -> str:
    params = {key: st.session_state.get(key, default) for key, default in DEFAULTS.items()}
    payload = {"name": "VX1000 preset", "app": "vx1000-mk1", "params": params}
    return f"?preset={urllib.parse.quote(json.dumps(payload, separators=(',', ':')))}"


_load_preset()

for key, default_value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = default_value

st.title("VX1000 Fisheye Simulator")
st.write(
    "Upload an image and apply a skateboard fisheye distortion with VX1000-inspired color and film styling."
)

with st.sidebar:
    st.header("Controls")
    st.selectbox(
        "Preset",
        ["Default", "Classic VX1000", "Soft Skate", "High Contrast"],
        key="preset",
    )
    st.slider("Lens strength", 0.0, 1.5, step=0.05, key="strength")
    st.slider("Image scale", 0.4, 1.0, step=0.01, key="scale")
    st.slider("Vignette", 0.0, 1.0, step=0.05, key="vignette")
    st.slider("Contrast", 0.5, 1.6, step=0.05, key="contrast")
    st.slider("Saturation", 0.6, 1.6, step=0.05, key="saturation")
    st.slider("Exposure", -0.5, 0.5, step=0.05, key="exposure")
    st.slider("Grain", 0.0, 0.5, step=0.02, key="grain")

    with st.expander("Preset URL"):
        st.write("Share or embed these exact parameters:")
        st.code(_preset_url())

preset = st.session_state["preset"]
if preset in PRESET_OVERRIDES:
    overrides = PRESET_OVERRIDES[preset]
    strength = overrides["strength"]
    scale = overrides["scale"]
    vignette = overrides["vignette"]
    contrast = overrides["contrast"]
    saturation = overrides["saturation"]
    exposure = overrides["exposure"]
    grain = overrides["grain"]
else:
    strength = st.session_state["strength"]
    scale = st.session_state["scale"]
    vignette = st.session_state["vignette"]
    contrast = st.session_state["contrast"]
    saturation = st.session_state["saturation"]
    exposure = st.session_state["exposure"]
    grain = st.session_state["grain"]

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
