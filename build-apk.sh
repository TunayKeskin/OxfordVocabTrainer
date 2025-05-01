#!/bin/bash

# Script to build Android APK for Oxford Vocabulary Quiz

echo "===== Building Oxford Vocabulary Quiz APK ====="

# Step 1: Prepare the mobile app directory
echo "Preparing mobile app directory..."
mkdir -p mobile-app/www/icons
mkdir -p mobile-app/www/css
mkdir -p mobile-app/www/js

# Step 2: Copy static assets
echo "Copying icons..."
cp -r static/icons/* mobile-app/www/icons/ 2>/dev/null || echo "No icons to copy"

echo "Copying CSS files..."
cp -r static/css/* mobile-app/www/css/ 2>/dev/null || echo "No CSS files to copy"

echo "Copying JS files..."
cp -r static/js/* mobile-app/www/js/ 2>/dev/null || echo "No JS files to copy"

# Step 3: Copy main icon to other sizes
echo "Preparing icons for different resolutions..."
cp generated-icon.png mobile-app/res/icon/android/icon-192-xxxhdpi.png
cp generated-icon.png mobile-app/res/icon/android/icon-144-xxhdpi.png
cp generated-icon.png mobile-app/res/icon/android/icon-96-xhdpi.png
cp generated-icon.png mobile-app/res/icon/android/icon-72-hdpi.png
cp generated-icon.png mobile-app/res/icon/android/icon-48-mdpi.png
cp generated-icon.png mobile-app/res/icon/android/icon-36-ldpi.png

# Step 4: Create basic splash screens
echo "Creating splash screens..."
cp generated-icon.png mobile-app/res/screen/android/screen-ldpi-portrait.png
cp generated-icon.png mobile-app/res/screen/android/screen-mdpi-portrait.png
cp generated-icon.png mobile-app/res/screen/android/screen-hdpi-portrait.png
cp generated-icon.png mobile-app/res/screen/android/screen-xhdpi-portrait.png
cp generated-icon.png mobile-app/res/screen/android/screen-xxhdpi-portrait.png
cp generated-icon.png mobile-app/res/screen/android/screen-xxxhdpi-portrait.png

cp generated-icon.png mobile-app/res/screen/android/screen-ldpi-landscape.png
cp generated-icon.png mobile-app/res/screen/android/screen-mdpi-landscape.png
cp generated-icon.png mobile-app/res/screen/android/screen-hdpi-landscape.png
cp generated-icon.png mobile-app/res/screen/android/screen-xhdpi-landscape.png
cp generated-icon.png mobile-app/res/screen/android/screen-xxhdpi-landscape.png
cp generated-icon.png mobile-app/res/screen/android/screen-xxxhdpi-landscape.png

# Step 5: Copy manifest
echo "Copying manifest..."
cp static/manifest.json mobile-app/www/

# Step 6: Add Cordova plugins
echo "Adding required Cordova plugins..."
cd mobile-app
npx cordova plugin add cordova-plugin-statusbar
npx cordova plugin add cordova-plugin-splashscreen
npx cordova plugin add cordova-plugin-inappbrowser
npx cordova plugin add cordova-plugin-network-information

# Step 7: Add Android platform
echo "Adding Android platform..."
npx cordova platform add android

# Step 8: Build the APK
echo "Building APK..."
npx cordova build android --release

# Step 9: Provide the location of the APK
echo "===== APK Build Process Complete ====="
echo "APK file is located at:"
echo "mobile-app/platforms/android/app/build/outputs/apk/release/app-release-unsigned.apk"
echo ""
echo "You can install this directly on your Android device"