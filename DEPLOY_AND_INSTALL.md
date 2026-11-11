# Deploying Motion Angle to an iPhone — free PWA route

**You do not need Xcode, Codex, TestFlight, an Apple Developer Program membership or an `.ipa` file.**

Unlike a native app, the PWA must first be hosted at a working **HTTPS** website. Opening `index.html` from the Files app or emailing the ZIP to yourself will **not** grant the iPhone's motion sensors to the web page.

## Recommended route: GitHub Pages (no hosting charge)

1. On your Mac, download `LIHPS_Motion_Angle_PWA_v0.2.zip` and unzip it.
2. Sign in to [github.com](https://github.com/) (a free account is sufficient).
3. Create a new **public** repository, for example `lihps-motion-angle` (you may use any available name).
4. Choose **Add file → Upload files**. Upload the **contents** of the unzipped `LIHPS_Motion_Angle_PWA` folder so that `index.html`, `app.js`, `math.js`, `styles.css`, `sw.js`, `manifest.webmanifest`, `.nojekyll` and the `icons/` folder sit in the repository root. If the GitHub browser uploader skips hidden `.nojekyll`, the app should still work; for more reliable deployment upload it using Git or GitHub Desktop.
5. Commit the files.
6. Open the repository's **Settings → Pages**. Under **Build and deployment**, set **Source = Deploy from a branch**, branch **main**, folder **/(root)**. Save.
7. GitHub will show the resulting site URL in the Pages settings once deployment is complete. It normally follows `https://YOUR-USERNAME.github.io/YOUR-REPOSITORY/`. **This is an example format, not an already-deployed URL.**
8. Open the HTTPS site in **Safari** on the iPhone. Tap **Enable** on the sensor banner, then approve the Motion & Orientation request. Check **Setup** to verify that device-orientation samples arrive.
9. In Safari tap **Page menu / Share → Add to Home Screen**; make sure **Open as Web App** is enabled and tap **Add**. Apple may rearrange the Share option depending on Safari layout and iOS version.
10. Launch the new **Motion Angle** icon on the Home Screen. If the installed app asks for sensor access again, tap **Enable** there as well.
11. Keep the PWA open in the foreground during measurements. Once the service worker has installed successfully, the static app should also open without an internet connection; verify this yourself by testing Airplane Mode after first opening online.

**GitHub Pages privacy:** GitHub Free requires a public repository for Pages, and the deployed site's source can be inspected by anyone. No trial measurements are uploaded by the application, but the app files themselves are public. For LIHPS internal code, prefer an institutional HTTPS site.

## Option: use an existing LIHPS HTTPS web server

Ask IT to upload all the static app files into one path on an HTTPS domain under LIHPS control, preserving `icons/` and the root files. No backend/database is necessary. Granting motion permission, saving trials and CSV export all happen on the iPhone. Confirm the server serves the `manifest.webmanifest` file and `sw.js` correctly and does not embed the app inside a third-party iframe.

## What changes compared with the old SwiftUI package?

| Native SwiftUI version | This PWA |
|---|---|
| Xcode compilation and Apple signing | None |
| Seven-day expiry on Apple's free signing | No provisioning expiry |
| Direct Core Motion | Browser `DeviceOrientationEvent` |
| Install via Xcode/TestFlight | Safari → Add to Home Screen |
| Offline supported by installed native package | Offline supported after successful service-worker caching |
| High control of sensor reference frame | Browser-controlled orientation fusion, requires additional validation |

## Updating the PWA

Replace the hosted files, increment the static cache version in `sw.js` and the visible app version. A new service worker will refresh the offline application. Existing locally stored trials are intended to remain if the same origin and path are used, but you should **export CSV before major updates**. Avoid changing the hosting URL unnecessarily, because local browser storage is origin-dependent.

## Troubleshooting

- **"Sensors not enabled":** Tap Enable while viewing the installed app (or Safari), then approve Motion & Orientation access. A permission prompt must be initiated by your tap.
- **"No orientation samples":** Use a real iPhone in Safari rather than a Mac browser. Try opening the hosted URL directly in Safari and granting permission there. Also check any browser/iPhone sensor-access restrictions.
- **Site opens but never activates sensors:** Confirm HTTPS; test in Safari rather than an embedded in-app browser. Sensor access can be restricted by browser settings or device management.
- **App stops while rotating:** Keep screen awake, app foregrounded and phone relatively level. Safari may suspend sensor events when the app leaves the foreground.
- **Offline unavailable:** Open once while connected, leave it open long enough for its first cache installation, then retry. Offline service-worker behaviour must be verified on your iPhone.
- **Data seems missing:** Safari and installed web apps may use different storage areas; return to the exact app context where trials were recorded. Export after each testing session.

Official documentation:
- Apple: https://support.apple.com/guide/iphone/turn-a-website-into-an-app-iphea86e5236/ios
- GitHub: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- MDN: https://developer.mozilla.org/en-US/docs/Web/API/DeviceOrientationEvent/requestPermission_static
