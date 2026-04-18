# VX1000 + Century MK1 Fisheye Resource Guide

This document compiles the useful sources and evidence gathered during the project research phase. It is intended to help distinguish between what is documented, what is inferred, and what still needs empirical calibration.

## 1. Project scope

The current simulator is best described as a stylized VX1000-inspired fisheye effect, not a scientifically exact replica of the Sony DCR-VX1000 + Century MK1 lens pair.

### Current repository status

- `processing.py`: generic radial distortion + color/vignette/grain pipeline
- `fisheye_calibration.py`: OpenCV fisheye calibration helper for real footage
- `README.md`: project overview and design goals
- `environment.yml`: Conda environment with required Python dependencies

## 2. Verified documented camera/lens details

### Sony DCR-VX1000

- Uses `3 × 1/3-inch CCDs`
- Built-in zoom lens: `5.9–59 mm`, `10x`
- Maximum aperture: `F1.6`
- Macro focus distance: about `1 cm` at wide end, about `80 cm` at tele end
- Likely `52 mm` filter thread on the front lens assembly, based on common user material
- The body and native lens are documented enough to constrain the camera geometry side of a replica

### Century MK1 Ultra Fisheye

- Known as the `0.3X Ultra Fisheye MKI` or "Death Lens"
- Designed as an extreme fisheye adapter for skate videography
- Reported field of view when mounted on VX1000:
  - `~180° diagonal`
  - `~125° horizontal`
- Proper mounting should avoid visible hard mechanical vignetting
- The VX1000 bayonet mount is specific for the Sony VX1000/DSR200/DSR200A/DSR250/PD150 family

## 3. Useful qualitative references

### Streetwar ultra fisheye guide

- Confirms the MK1’s practical reputation: extreme barrel distortion, wide view, and skateboarding usage
- Reinforces the FOV estimates and correct mounting behavior
- Does not provide optical formulas, projection class, or coefficient data

### Shineye app

- Useful as a modern style reference for extreme fisheye/retro video aesthetics
- Confirms the kind of effect people expect from a digital" death lens" simulation
- Not a scientific or calibration source for MK1 optics

### YouTube/DaVinci Resolve transcript

- Helpful as a practical, post-process fisheye styling workflow
- Demonstrates how users fake fisheye with generic lens distortion tools and color grading
- Does not add any hard optical model or calibrated lens data

## 4. What is still missing for a scientific replica

These are the details that were not found in public manufacturer or primary sources:

- exact MK1 projection class (`equidistant`, `equisolid-angle`, `stereographic`, `orthographic`, etc.)
- exact MK1 distortion coefficients
- exact MK1 vignette / relative illumination falloff curve
- exact MK1 chromatic aberration curve
- exact Sony VX1000 gamma/transfer curve or DSP color matrix
- precise VX1000 active sensor dimensions and image circle diameter

## 5. Best practical approach

### Use empirical calibration

For a defensible scientific model, the MK1 should be treated as an unknown fisheye adapter and solved from measured footage.

Recommended measurements:

- checkerboard or ChArUco calibration footage to estimate projection and distortion
- flat-field shots for vignette / illumination falloff
- high-contrast edge/grid shots for lateral chromatic aberration
- color chart and grayscale ramp shots for response/gamma characterization

### OpenCV fisheye model

The best Python/OpenCV starting point is the `cv2.fisheye` module:

- `cv2.fisheye.calibrate`
- `cv2.fisheye.undistortImage`
- `cv2.fisheye.initUndistortRectifyMap`

Suggested initial distortion coefficient seeds:

- `[0.05, -0.10, 0.10, -0.05]`
- `[0.08, -0.16, 0.35, -0.26]`
- `[0.12, -0.25, 0.45, -0.30]`

These should be treated as starting guesses, not universal MK1 values.

## 6. Recommended next steps

1. Collect actual VX1000 + MK1 calibration images.
2. Run `fisheye_calibration.py` with checkerboard or ChArUco views.
3. Compare fitted results visually and with reprojection RMS.
4. Use flat-field and color-target shots to refine vignette and color response.
5. If `cv2.fisheye` is insufficient, evaluate omnidirectional/Kannala-Brandt models.

## 7. Summary

- This project currently models the look, not the exact optics.
- Public sources provide strong qualitative evidence but not exact optical data.
- Empirical calibration is the correct path for a scientific VX1000+MK1 replica.
- The OpenCV fisheye approach is the most practical starting point in Python.
