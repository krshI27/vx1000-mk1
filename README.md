# VX1000 Fisheye Simulator

A skateboard fisheye simulator focused on recreating the Sony VX1000 + MK1 lens visual style.

## Project overview

This project is a simulation tool for the distinctive skateboard fisheye look of the Sony VX1000 camcorder paired with the Century Optics MK1 fisheye lens. The goal is to apply realistic lens distortion, color response, and analog video character to input images and video frames.

## Goals

- Simulate the MK1 fisheye lens distortion and field of view
- Recreate Sony VX1000 color rendering, contrast, and video feel
- Add authentic vignette, chromatic aberration, and film grain
- Allow users to preview the effect on images and video frames
- Provide controls for lens strength, exposure, and skateboarding-style framing

## Target users

- Skateboard filmmakers and photographers
- Visual effects and retro video enthusiasts
- Developers interested in lens modeling and analog simulation
- Artists wanting a fast fisheye preview tool

## Core features

1. Input handling
   - Load images or video files
   - Support common formats like JPG, PNG, MP4, MOV
   - Optionally use webcam capture for live preview

2. Lens simulation
   - MK1 fisheye distortion model tuned to reference specs
   - Adjustable field of view and projection type
   - Barrel distortion, vignette, and boundary falloff
   - Chromatic aberration and edge color fringing

3. VX1000 look
   - Color transform to mimic VX1000 video palette
   - Contrast and saturation adjustments
   - Noise/grain, scanline, and analog glow
   - Motion blur / rolling shutter style blur for moving frames

4. Output and sharing
   - Preview result in the web app
   - Export processed frames or video
   - Save presets for lens and film profiles

## Implementation plan

### Phase 1: MVP image simulator

- Create a project scaffold with Streamlit or a lightweight web frontend.
- Add an upload panel for input images.
- Implement a basic fisheye distortion filter using OpenCV or NumPy.
- Add controls for lens strength, image scale, and vignette.
- Show side-by-side before/after preview.

### Phase 2: VX1000 color + film style

- Add a color grading module for VX1000-inspired tones.
- Implement brightness, contrast, and saturation controls.
- Add film grain, vignette, and analog noise overlays.
- Add presets for classic skateboarding looks.

### Phase 3: video support and advanced detail

- Add video frame processing for MP4/MOV files.
- Implement scene-level preview and export.
- Add optional motion blur / frame blending.
- Add chromatic aberration and edge fringing controls.

### Phase 4: accuracy and polish

- Tune distortion parameters to the MK1 fisheye optical behavior.
- Add reference sample presets using Sony VX1000 / MK1 specs.
- Add a comparison mode with original skate footage style.
- Add export options for final frames, GIFs, or processed clips.

## Architecture

### UI

- Upload / capture area
- Parameter controls for lens, film, and output
- Preview panel with before/after or slider comparison
- Presets and save/load controls

### Processing pipeline

- Input decoding and resize
- Lens distortion and projection transform
- Color transform / film emulation
- Overlay effects (vignette, grain, chromatic aberration)
- Output encode and download

### Lens model details

- Use an equidistant or azimuthal fisheye projection tuned around 180° FOV
- Apply a radial distortion map similar to the MK1 behavior
- Add vignette falloff that mimics heavy fisheye edge shading

## Technology choices

- Python + Streamlit for a fast interactive prototype
- OpenCV / NumPy for distortion and pixel remapping
- `imageio` or `moviepy` for video loading and export
- `pillow` for image manipulation and overlay generation
- Optional WebGL / JS fallback for real-time browser preview

## References and research

- Century Optics MK1 fisheye lens specs and appearance
- Sony VX1000 video aesthetic documented by skate media articles
- Skateboard fisheye visual language with barrel-shifted framing

## Extensions

- Add live webcam preview with real-time fisheye simulation
- Add a `digital fisheye` mode based on modern Shineye-style lenses
- Add an interactive calibration tool to match distortion to real footage
- Add a lens library with other skateboarding fisheye profiles

## Feature ideas

- **Camera capture**: `st.camera_input` for instant in-browser snapshot → apply VX1000 effect immediately, no file picker needed

## Quick Start

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the app:

   ```bash
   streamlit run streamlit_app.py
   ```

3. Upload an image and adjust the lens, vignette, and film controls.
