# Creating an APK with Android Studio - Detailed Guide

This guide provides step-by-step instructions for creating an APK for the Oxford Vocabulary Quiz application using Android Studio.

![APK Creation Workflow](/static/img/apk_creation_workflow.svg)

The diagram above illustrates the overall APK creation process. Follow the detailed steps below to create your APK.

## Prerequisites

1. [Android Studio](https://developer.android.com/studio) installed on your computer
2. JDK 11 or higher
3. A copy of the project files from Replit

## Step 1: Prepare Project Files

Before opening Android Studio, you need to prepare the project files:

1. In your Replit project, run the preparation script:
   ```
   ./prepare_apk.sh
   ```

2. If the mobile-app/platforms/android directory doesn't exist, initialize it:
   ```
   cd mobile-app
   cordova platform add android
   ```

3. Download the entire project folder from Replit, which should now include:
   - mobile-app/platforms/android (the main Android project)
   - mobile-app/www (contains HTML, CSS, JS files)
   - mobile-app/config.xml (configuration file)

## Step 2: Open Project in Android Studio

1. Launch Android Studio
2. Select "Open an Existing Project"
3. Navigate to the downloaded project folder
4. Select the `mobile-app/platforms/android` directory
5. Click "Open"

## Step 3: Configure the Project

Android Studio may need to sync and update various components:

1. If prompted to update Gradle, click "Update"
2. Wait for the Gradle sync to complete
3. If you see any error messages about missing SDK components:
   - Go to Tools → SDK Manager
   - Install any missing SDK versions
   - Install the required NDK version if prompted

## Step 4: Resolve Dependencies

You may need to resolve dependencies:

1. In the Project navigator (left sidebar), expand the "Gradle Scripts" folder
2. Open the `build.gradle` file (the one at the project level, not the app level)
3. Check the repositories section has Google and Maven repositories:
   ```gradle
   repositories {
       google()
       mavenCentral()
   }
   ```
4. Open the app-level `build.gradle` file to check dependency versions
5. Click "Sync Now" if you make any changes

## Step 5: Build a Debug APK

For testing purposes, start with a debug build:

1. From the menu bar, select Build → Build Bundle(s) / APK(s) → Build APK(s)
2. Wait for the build process to complete
3. When finished, a notification will appear with a link to the APK file
4. Click on "locate" in the notification to find the APK file, or navigate to:
   ```
   mobile-app/platforms/android/app/build/outputs/apk/debug/app-debug.apk
   ```

## Step 6: Build a Release APK (Optional)

For distribution, create a signed release version:

1. From the menu bar, select Build → Generate Signed Bundle / APK
2. Select "APK" and click "Next"
3. Create a new keystore or use an existing one:
   - If creating new: click "Create new..." and fill in the required information
   - Key store path: Choose a location to save the keystore file
   - Password: Create a strong password
   - Alias: Create a key alias
   - Key password: Create a key password
   - Validity: 25+ years recommended
   - Certificate: Fill in your name and organization details
4. Click "Next"
5. Select release build type
6. Check both "V1 (Jar Signature)" and "V2 (Full APK Signature)"
7. Click "Finish"
8. The signed APK will be generated at:
   ```
   mobile-app/platforms/android/app/build/outputs/apk/release/app-release.apk
   ```

## Step 7: Install the APK on a Device

You can install the APK on an Android device in several ways:

### Using adb (Android Debug Bridge):

1. Connect your Android device to your computer via USB
2. Enable USB debugging on your device (in Developer options)
3. Open a terminal or command prompt and run:
   ```
   adb install path/to/your/app-debug.apk
   ```

### Directly on the device:

1. Transfer the APK file to your Android device (via USB, email, cloud storage)
2. On your device, navigate to the file and tap on it
3. If prompted, enable "Install from Unknown Sources" in settings
4. Follow the on-screen instructions to install

## Troubleshooting

### Build Errors

1. **Gradle sync failed**: 
   - Update Android Studio
   - Update Gradle plugin version in project structure settings
   - Clear caches (File → Invalidate Caches / Restart)

2. **Missing SDK components**:
   - Open SDK Manager (Tools → SDK Manager)
   - Install required components

3. **Java version issues**:
   - Ensure you're using compatible JDK (11+)
   - Set JAVA_HOME environment variable correctly

### Runtime Errors

1. **App crashes on startup**:
   - Check logcat in Android Studio for detailed error messages
   - Verify the app has proper permissions
   - Ensure all required plugins are installed

2. **UI rendering issues**:
   - Verify all HTML, CSS, and JS files are included in the APK
   - Check for console errors in Android Studio's logcat

## Additional Resources

- [Android Developer Documentation](https://developer.android.com/docs)
- [Cordova Android Platform Guide](https://cordova.apache.org/docs/en/latest/guide/platforms/android/)
- [App Signing in Android](https://developer.android.com/studio/publish/app-signing)

## Need More Help?

If you encounter specific issues not covered in this guide, check the following:

1. Android Studio logs (View → Tool Windows → Logcat)
2. Gradle console output (View → Tool Windows → Build)
3. Event Log (View → Tool Windows → Event Log)

---

Good luck with your Android app development!