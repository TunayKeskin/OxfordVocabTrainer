#!/bin/bash

# Script to build Android APK for Oxford Vocabulary Quiz
set -e  # Exit on error

echo "===== Building Oxford Vocabulary Quiz APK ====="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Node.js is required but not installed. Please install Node.js and try again."
    exit 1
fi

# Check if Cordova is installed
if ! command -v npx cordova &> /dev/null; then
    echo "Cordova is required but not installed. Installing Cordova..."
    npm install -g cordova
fi

# Step 1: Prepare the mobile app directory
echo "Preparing mobile app directory..."
mkdir -p mobile-app/www/icons
mkdir -p mobile-app/www/css
mkdir -p mobile-app/www/js

# Step 2: Copy static assets
echo "Copying icons..."
cp -r static/icons/* mobile-app/www/icons/ 2>/dev/null || echo "No icons to copy"

echo "Copying CSS files..."
cp static/css/* mobile-app/www/css/ 2>/dev/null || echo "No CSS files to copy"

echo "Copying JS files..."
cp static/js/* mobile-app/www/js/ 2>/dev/null || echo "No JS files to copy"

# Step 3: Copy main icon to other sizes
echo "Preparing icons for different resolutions..."
cp generated-icon.png mobile-app/www/icons/icon-512x512.png 2>/dev/null || echo "Warning: Main icon not found"
cp generated-icon.png mobile-app/res/icon/android/icon-192-xxxhdpi.png 2>/dev/null || echo "Warning: Icon conversion failed"
cp generated-icon.png mobile-app/res/icon/android/icon-144-xxhdpi.png 2>/dev/null || echo "Warning: Icon conversion failed"
cp generated-icon.png mobile-app/res/icon/android/icon-96-xhdpi.png 2>/dev/null || echo "Warning: Icon conversion failed"
cp generated-icon.png mobile-app/res/icon/android/icon-72-hdpi.png 2>/dev/null || echo "Warning: Icon conversion failed"
cp generated-icon.png mobile-app/res/icon/android/icon-48-mdpi.png 2>/dev/null || echo "Warning: Icon conversion failed"
cp generated-icon.png mobile-app/res/icon/android/icon-36-ldpi.png 2>/dev/null || echo "Warning: Icon conversion failed"

# Step 4: Create basic splash screens
echo "Creating splash screens..."
for size in ldpi mdpi hdpi xhdpi xxhdpi xxxhdpi; do
    cp generated-icon.png mobile-app/res/screen/android/screen-${size}-portrait.png 2>/dev/null || echo "Warning: Splash screen conversion failed"
    cp generated-icon.png mobile-app/res/screen/android/screen-${size}-landscape.png 2>/dev/null || echo "Warning: Splash screen conversion failed"
done

# Step 5: Copy manifest
echo "Copying manifest..."
cp static/manifest.json mobile-app/www/ 2>/dev/null || echo "Warning: Manifest not found"

# Step 6: Create a deploy-ready configuration
cd mobile-app

# Add plugins if not already added
if ! grep -q "cordova-plugin-statusbar" config.xml 2>/dev/null; then
    echo "Adding required Cordova plugins..."
    npx cordova plugin add cordova-plugin-statusbar || echo "Warning: Failed to add statusbar plugin"
    npx cordova plugin add cordova-plugin-splashscreen || echo "Warning: Failed to add splashscreen plugin"
    npx cordova plugin add cordova-plugin-inappbrowser || echo "Warning: Failed to add inappbrowser plugin"
    npx cordova plugin add cordova-plugin-network-information || echo "Warning: Failed to add network-information plugin"
fi

# Add Android platform if not already added
if [ ! -d "platforms/android" ]; then
    echo "Adding Android platform..."
    npx cordova platform add android || echo "Warning: Failed to add Android platform"
fi

# Build the APK
echo "Building APK..."
npx cordova build android --release || {
    echo "Build failed. Trying again with --debug flag..."
    npx cordova build android --debug
}

# Check if the build was successful
if [ -f "platforms/android/app/build/outputs/apk/release/app-release-unsigned.apk" ]; then
    APK_PATH="platforms/android/app/build/outputs/apk/release/app-release-unsigned.apk"
elif [ -f "platforms/android/app/build/outputs/apk/debug/app-debug.apk" ]; then
    APK_PATH="platforms/android/app/build/outputs/apk/debug/app-debug.apk"
else
    echo "Failed to build APK. Check the logs for errors."
    exit 1
fi

# Copy the APK to a more accessible location
cp "${APK_PATH}" ../OxfordVocabQuiz.apk

cd ..

echo "===== APK Build Process Complete ====="
echo "APK file is located at: OxfordVocabQuiz.apk"
echo ""
echo "You can install this directly on your Android device."
echo "Note: You may need to enable 'Unknown sources' in your Android settings to install this APK."