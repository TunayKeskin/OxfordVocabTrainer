# Android APK Deployment Guide

This document provides step-by-step instructions for building and deploying the Oxford Vocabulary Quiz application as an Android APK.

## Prerequisites

- Node.js and npm
- Apache Cordova
- JDK 11 or higher (for Android builds)
- Android SDK (for Android builds)
- Gradle (for Android builds)
- Android Studio (for Option 3)

## Building the APK

### Option 1: Using the Build Script (Recommended)

1. Make sure you have all the prerequisites installed.
2. Run the prepare script first:
   ```
   ./prepare_apk.sh
   ```
3. Then run the build script:
   ```
   ./build-apk.sh
   ```
4. The script will handle all the necessary steps and create an APK file at `OxfordVocabQuiz.apk`.

### Option 2: Manual Build Process

1. Prepare the mobile app directory:
   ```
   mkdir -p mobile-app/www/icons mobile-app/www/css mobile-app/www/js
   cp -r static/icons/* mobile-app/www/icons/
   cp -r static/css/* mobile-app/www/css/
   cp -r static/js/* mobile-app/www/js/
   cp static/manifest.json mobile-app/www/
   ```

2. Add Cordova plugins:
   ```
   cd mobile-app
   cordova plugin add cordova-plugin-statusbar
   cordova plugin add cordova-plugin-splashscreen
   cordova plugin add cordova-plugin-inappbrowser
   cordova plugin add cordova-plugin-network-information
   ```

3. Add Android platform:
   ```
   cordova platform add android
   ```

4. Build the APK:
   ```
   cordova build android --release
   ```

5. The APK will be created at:
   ```
   platforms/android/app/build/outputs/apk/release/app-release-unsigned.apk
   ```

### Option 3: Using Android Studio

1. First, run the preparation script to ensure all mobile app files are ready:
   ```
   ./prepare_apk.sh
   ```

2. Download and install Android Studio from [developer.android.com](https://developer.android.com/studio).

3. Open Android Studio and select "Open an Existing Project"

4. Navigate to and select the Android project located at:
   ```
   mobile-app/platforms/android
   ```
   Note: If this directory doesn't exist, you need to add the Android platform first:
   ```
   cd mobile-app
   cordova platform add android
   ```

5. Once the project is open in Android Studio:
   - Wait for the Gradle sync to complete
   - Resolve any dependencies or SDK issues (Android Studio will guide you)
   - You may need to update the Gradle version if prompted

6. Build the APK:
   - Click on "Build" in the top menu
   - Select "Build Bundle(s) / APK(s)"
   - Choose "Build APK(s)"

7. When the build completes, click on the notification that appears or locate the APK at:
   ```
   mobile-app/platforms/android/app/build/outputs/apk/debug/app-debug.apk
   ```

8. For a signed release version:
   - Click on "Build" in the top menu
   - Select "Generate Signed Bundle / APK"
   - Choose "APK"
   - Create or use an existing keystore
   - Fill in the required keystore information
   - Select a destination folder
   - Click "Finish"

## Installing the APK on Android Devices

### Method 1: Direct Installation

1. Transfer the APK file to your Android device (via USB, email, cloud storage, etc.).
2. On your Android device, navigate to the APK file and tap on it.
3. If prompted, enable "Install from Unknown Sources" in your device settings.
4. Follow the on-screen instructions to complete the installation.

### Method 2: ADB Installation (For Developers)

1. Enable Developer Options and USB Debugging on your Android device.
2. Connect your device to your computer via USB.
3. Run the following command to install the APK:
   ```
   adb install OxfordVocabQuiz.apk
   ```

## Troubleshooting

### App Crashes on Startup
- Check if the web service is running and accessible.
- Verify that the URL in the app is correct.
- Check internet connectivity on the device.

### Installation Fails
- Make sure "Install from Unknown Sources" is enabled.
- Check if you have sufficient storage space.
- Try uninstalling any previous version of the app.

### App Shows Blank Screen
- Check if the service worker is properly configured.
- Verify that all necessary static files are included in the APK.

## Distribution

To distribute your app to users:

1. Share the APK file directly with users.
2. Host the APK on a website or file-sharing service.
3. For official distribution, consider publishing to the Google Play Store (requires signing the APK).