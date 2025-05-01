# Oxford Vocabulary Quiz - Mobile App

This is the mobile app version of the Oxford Vocabulary Quiz application, built using Apache Cordova.

## About the App

Oxford Vocabulary Quiz is a language learning application designed to help users learn English-Turkish vocabulary using the Oxford 3000 and Oxford 5000 word lists. This mobile version allows users to practice vocabulary on their Android devices.

## Features

- English to Turkish and Turkish to English quizzes
- Multiple difficulty levels
- Word pronunciation
- Spaced repetition learning
- Offline access to vocabulary
- Progress tracking

## Building the App

### Prerequisites

- Node.js and npm
- Apache Cordova
- Android SDK (for Android builds)
- JDK 11 or higher

### Build Process

1. Prepare the project:
   ```
   ./prepare_apk.sh
   ```

2. Add the Android platform (if not already added):
   ```
   cd mobile-app
   cordova platform add android
   ```

3. Build the APK:
   ```
   cordova build android
   ```

4. The APK will be available at:
   ```
   platforms/android/app/build/outputs/apk/debug/app-debug.apk
   ```

For detailed instructions on building with Android Studio, see the `ANDROID_STUDIO_GUIDE.md` file in the project root.

## Development

The mobile app is a Cordova wrapper around the web application, with these key differences:

1. Mobile-specific UI adaptations
2. Offline functionality
3. Native device integration (storage, media)
4. Cordova plugins for enhanced functionality

### Project Structure

- `www/`: Contains the web assets (HTML, CSS, JS)
- `config.xml`: Cordova configuration
- `platforms/`: Native platform-specific code
- `plugins/`: Cordova plugins

## Testing

You can test the application using:

1. Android Emulator (via Android Studio)
2. Physical device connected via USB
3. Cordova's browser platform for quick UI testing:
   ```
   cordova platform add browser
   cordova run browser
   ```

## Distribution

Once built, the APK can be:

1. Installed directly on devices
2. Distributed via app stores (requires signing)
3. Shared via direct download links