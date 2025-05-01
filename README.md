# Oxford Vocabulary Quiz

A vocabulary learning application based on Oxford wordlists (3000 and 5000). This application helps users learn English-Turkish vocabulary through quizzes and spaced repetition.

## Features

- **Quiz-based Learning**: Test your vocabulary knowledge with customizable quizzes
- **Spaced Repetition**: Review words at optimal intervals for better retention
- **Oxford Wordlists**: Built on the Oxford 3000 and Oxford 5000 word lists
- **User Profiles**: Track your progress and personalize your learning experience
- **Favorites System**: Save words for extra practice
- **Leaderboard**: Compare your performance with other learners
- **Word Pronunciation**: Hear how words are pronounced in English
- **Example Sentences**: See words used in context with example sentences
- **Mobile-friendly**: Works seamlessly on both desktop and mobile devices

## Running the Web Application

1. Start the application:
   ```
   gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
   ```

2. Open your browser and navigate to `http://localhost:5000`

## Installing the Android APK

1. Build the APK using the provided script:
   ```
   ./build-apk.sh
   ```

2. The APK will be created at:
   ```
   mobile-app/platforms/android/app/build/outputs/apk/release/app-release-unsigned.apk
   ```

3. Transfer the APK to your Android device and install it.

4. To install an unsigned APK, you need to enable "Unknown sources" in your Android settings.

## Technologies Used

- **Backend**: Python, Flask, SQLAlchemy, PostgreSQL
- **Frontend**: JavaScript, HTML, CSS, Bootstrap
- **Mobile**: Apache Cordova
- **APIs**: Google Text-to-Speech (for pronunciations)

## License

This project is for educational purposes only. Oxford wordlists are the property of Oxford University Press.