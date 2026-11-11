# Motion Angle PWA — first iPhone test and validation checklist

## A. Installation and sensor availability (functional)

- [ ] App opens from HTTPS and from the home-screen icon.
- [ ] User-initiated motion permission succeeds.
- [ ] Setup displays live `deviceorientation` samples (check update rate and `absolute` flag).
- [ ] Verify the app can reopen offline *after* successful first online loading and caching.
- [ ] Confirm records survive closing/relaunching the same app context.
- [ ] Confirm CSV export produces the expected rows and numbers.

## B. Static orientation and baseline stability

- [ ] Phone horizontal, stationary, zeroed. Measure 30–60 s of apparent drift and record if the browser reference frame changes.
- [ ] Repeat the test indoors and outdoors (ideally away from ferromagnetic structures) and document the `absolute` flag.
- [ ] Start zeroing while intentionally moving the phone: zeroing must not accept a moving baseline.
- [ ] Device tilted 10°, 15° and 20°: check the tilt indicator and warning behaviour.
- [ ] Rotate slowly through +179° / −179° heading boundary: ensure wrap-around does not create a 360° spike.

## C. Dynamic trunk rotation

- [ ] With the phone held nearly level, rotate it +30°, +60°, +90° around a controlled vertical axis; return to start. The display must retain the peak.
- [ ] Repeat for the opposite direction with consistent axis sign, and compare with known angle/Qualisys reference.
- [ ] Add controlled phone tilt (e.g., 10° and 20°) to assess measurement error and QC flag relevance.
- [ ] Test actual seated subjects with the intended sternum-contact method while checking for hand/forearm rotation independent of thorax.
- [ ] Distinguish **world-relative thorax orientation** from **thorax relative to pelvis**; the iPhone cannot quantify the latter without an additional pelvic reference.
- [ ] Keep an independent reference to measurement start and stop. The tap to end the trial must be possible after returning to neutral.

## D. Inclinometer / joint tools

- [ ] Use calibrated inclines at 0°, 30°, 60°, 90° and >90°, using both long and short iPhone edges.
- [ ] Confirm sign convention when the device is flipped around its normal axis.
- [ ] For two-segment measurement, use a planar mechanical hinge at known angles. Check both adjacent segments within the same plane, oriented consistently.
- [ ] For 3D ROM-from-zero, use known controlled single-axis and compound rotations and compare quaternion magnitude and individual device-axis peaks.
- [ ] If any joint angle is intended as an anatomical measurement, document a joint-specific mounting/axis-alignment protocol before using its labels clinically.

## E. What to quantify against Qualisys

For repeated movements over the expected clinical range, calculate:

- Mean signed error (bias), SD of errors and 95% limits of agreement.
- Within-session repeatability / typical error (e.g. SEM, CV where defensible).
- Between-day reliability if monitoring longitudinal change.
- Error as a function of tilt, movement speed and absolute/relative browser reference flag.
- Sensitivity to device model, iOS/WebKit version and app being installed vs running in Safari.

**Do not mistake 0.1° display resolution for 0.1° accuracy.** The 15° tilt warning and 2.5° zeroing-stability criteria are provisional engineering parameters, not validated clinical thresholds.
