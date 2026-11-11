# LIHPS Motion Angle — PWA v0.2.0

An experimental, offline-capable, installable **Progressive Web App** for iPhone. Inspired by the minimal measurement-oriented interaction pattern of handheld sports testing devices; no VALD assets or branding are used. Red, white and sky blue follow Luxembourg's flag colour scheme.

**Important:** This is **not a clinically validated measurement instrument**. It is a testable software prototype. Its measurements have not been compared against a reference instrument on a physical iPhone. The PWA relies on browser-provided orientation events, not native Core Motion; its characteristics may vary by iPhone, iOS and browser version.

## Contents

- `index.html` — all app screens (trunk, joint, records, setup)
- `styles.css` — LIHPS-inspired colours and UI
- `math.js` — tested sensor-frame mathematics (W3C Z-X-Y device orientation, gravity, quaternions)
- `app.js` — permissions, trials, filtering/QC, state machine, local storage, CSV export
- `manifest.webmanifest` and `icons/` — home-screen installation
- `sw.js` — service worker for offline static assets
- `.nojekyll` — facilitates static GitHub Pages deployment
- `DEPLOY_AND_INSTALL.md` — detailed installation instructions
- `VALIDATION_CHECKLIST.md` — protocol for first measurement checks
- `tests/` — mathematical unit test and mocked desktop-browser smoke test

## Supported workflows

### Trunk axial rotation

- Place iPhone *screen up*, one **long edge** in contact with the sternum.
- Choose optional trial label (left/right/either). **Labels are user-selected, not inferred anatomically.**
- One screen tap starts zeroing; the application waits until ~0.5 s of sufficiently stable orientation samples are available (up to 4.5 s).
- Audible start tone is attempted, but may be unavailable or muted on some devices; **the screen always shows MEASURING**.
- The largest absolute rotation achieved in the trial is **continuously retained**, even if the subject returns to neutral.
- A second tap finishes and saves the peak. Third tap starts a new trial.
- Peak is computed for every received event, not only on UI refresh.
- Internally stores signed and unsigned peaks, peak phone tilt, reported orientation reference type, duration and selected direction.
- QC warning when screen tilt exceeds a provisional **15°** threshold. Severe heading discontinuities or data gaps interrupt a measurement.
- Current-session trial count, mean and range, plus deletion of the most recent trial.

### Joint / limb tools

- **Inclinometer:** phone long/short edge; signed angle in phone's vertical measurement plane and out-of-plane warning; stable snapshot capture.
- **ROM from zero:** baseline-relative 3D quaternion motion; 3D rotation magnitude and independent device X/Y/Z peaks (not anatomical axes). State-machine and peak capture as above.
- **Two-segment angle:** sequential proximal and distal static inclinations; planar angle difference in 0–180° range. **Requires co-planar segments, consistent edge orientation and screen facing. It is not dynamic 3D joint motion.**

### Records and diagnostics

- Local per-origin `localStorage`; no cloud upload, user account or athlete names.
- CSV export (Excel/Visual3D-compatible plain CSV with a UTF-8 BOM).
- Session creation, trial history and setup diagnostics (sample frequency, reported `absolute` flag, measured tilt, heading spread).
- Offline app assets after first successful service-worker installation while online.

## Technical notes

- Device orientation: [W3C Device Orientation and Motion](https://www.w3.org/TR/orientation-event/), Z(alpha)–X′(beta)–Y″(gamma) intrinsic rotations. Axes are the phone's **portrait-native** axes, even when the screen rotates.
- The trunk angle is computed from the **world-horizontal projection of the device's native Y axis**. Its heading is continuously unwrapped across ±180°, then zeroed. The peak is the maximum absolute accumulated excursion, while the signed peak is also saved.
- Phone tilt is measured via the orientation of the screen normal relative to world vertical. A small tilt does not automatically imply equivalent angle error, but may indicate poor standardisation.
- Joint mode's relative quaternion is `inverse(baseline) × current`. Its Z-X-Y decomposition is *device-based*, affected by rotation order and singularities; no anatomical interpretation is implied.
- Inclinometer angles are calculated from gravity components in the device frame with `atan2`, not a single `asin`. Interpretation is planar.
- Diagnostic heading spread over 10 s represents **movement + sensor variation**, not sensor-only noise unless the phone is held motionless.
- Browser motion/orientation permission must be granted by a user tap and on HTTPS. The application requests relative (non-absolute) orientation permission where supported and does not request compass heading or geolocation.
- On Apple platforms, `DeviceOrientationEvent` may be provided with a magnetic or arbitrary reference, and sensor fusion is controlled by WebKit. Magnetometer interference and discontinuities remain possible.
- Some iOS versions may not play tones or produce haptic vibration from a web app. Rely on the visible state, not solely sound.
- Use the **same installed app** to retrieve data. Browser and home-screen web app storage may not be shared in all circumstances; do not assume it is synced between devices.

## Development / tests

No Swift, Xcode, paid developer account or Mac-specific build tooling is needed. The files are plain HTML, CSS and JavaScript.

Unit tests (if Node.js is installed):

```bash
node --test tests/math.test.mjs
```

Optional local desktop preview:

```bash
python3 -m http.server 8080
```

Then visit `http://localhost:8080` **on the same computer**. `localhost` can be treated as a trustworthy origin for browser development, but the web app **will not access iPhone motion sensors through a Mac's insecure LAN HTTP address**. Use a real HTTPS URL for iPhone testing.

The `tests/browser_smoke.py` automated interface test was run in a desktop Chromium browser using synthetic orientation events. It is not evidence of sensor validity on an iPhone.

## Data handling and deployment security

All data records are written locally in the browser. They are not stored in the GitHub repository or sent to a server by this app. Static hosting providers may still log ordinary HTTP access metadata. Do not store identifiable athlete notes or protected health information in this prototype. Export CSV regularly; clearing Safari/website data or OS storage eviction may remove records.

**Publishing a GitHub Pages site using a free public repository makes this source code public.** To keep application source private, use an organisation-controlled HTTPS static hosting service or a paid/private hosting solution instead.

See `DEPLOY_AND_INSTALL.md` and `VALIDATION_CHECKLIST.md` before first use.
