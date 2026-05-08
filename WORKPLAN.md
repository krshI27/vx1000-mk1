# WORKPLAN — vx1000-mk1

**Status**: DEPLOYED on Streamlit Cloud (2026-04-25). Preset loader done (ZV1-vx1000).
**Output**: VX1000 + MK1 fisheye look on uploaded images — barrel distortion, vignette, chromatic aberration, grain, color grade.
**Params**: `strength`, `scale`, `vignette`, `contrast`, `saturation`, `exposure`, `grain` — all serializable → natural preset target.

---

## Active priorities (2026-05-08 — Zine Vol.1 preset authoring)

### Zine Vol.1 preset rollout

- [x] **ZV1-vx1000** (2026-04-26): `?preset=` URL loader done — `_load_preset()` populates `st.session_state` via `DEFAULTS` keys
- [ ] **ZV1-preset-vx1000** ~30min: Author 1–2 Zine Vol.1 hero presets — pick image + settings that produce strong output; save as `presets/zine-vol1-*.json`

Preset JSON schema:
```json
{
  "name": "Zine Vol.1 — Classic Skate",
  "app": "vx1000-mk1",
  "params": {
    "strength": 1.05,
    "scale": 0.94,
    "vignette": 0.48,
    "contrast": 1.25,
    "saturation": 1.20,
    "exposure": 0.04,
    "grain": 0.18
  }
}
```

### Revenue path (deferred)

- [ ] **VX-EXPORT** ~30min: Add high-res export button — output at 2× or print DPI; currently only screen-res PIL output
- [ ] **VX-PRODIGI** ~1hr: "Order Print" button → high-res render → upload to R2 public bucket → Prodigi order (same pattern as scribe/stairset)
- [ ] **VX-2** ~1hr: Create demo GIF/video showing before → after fisheye transform for marketing

## Notes

- `processing.py`: pure functions; `apply_vx1000_effect(image, params)` pipeline
- Built-in presets (`PRESET_OVERRIDES`): Classic VX1000, Soft Skate, High Contrast — good starting points for Zine preset authoring
- No `presets/` folder yet — create it when authoring ZV1-preset-vx1000
- See `krshi27-scribe/WORKPLAN.md` for shared `upload_to_r2()` + `create_prodigi_order()` pattern
