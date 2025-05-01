#!/bin/bash
set -e

echo "=== Preparing for APK generation ==="

# Step 1: Cleanup previous build artifacts
echo "Cleaning up previous build artifacts..."
rm -rf mobile-app/platforms/android/build 2>/dev/null || true
rm -rf mobile-app/platforms/android/app/build 2>/dev/null || true
rm -rf mobile-app/platforms/android/CordovaLib/build 2>/dev/null || true
rm -rf mobile-app/www/js/* 2>/dev/null || true
rm -rf mobile-app/www/css/* 2>/dev/null || true
rm -rf mobile-app/www/img/* 2>/dev/null || true
rm -rf mobile-app/www/audio/* 2>/dev/null || true

# Step 2: Create necessary directories
echo "Creating necessary directories..."
mkdir -p mobile-app/www/js
mkdir -p mobile-app/www/css
mkdir -p mobile-app/www/img
mkdir -p mobile-app/www/audio/pronunciations

# Step 3: Copy web assets to mobile app
echo "Copying web assets to mobile app..."
cp -r static/js/* mobile-app/www/js/ 2>/dev/null || true
cp -r static/css/* mobile-app/www/css/ 2>/dev/null || true
cp -r static/img/* mobile-app/www/img/ 2>/dev/null || true
cp -r static/icons/* mobile-app/www/img/ 2>/dev/null || true
cp -r static/audio/pronunciations/* mobile-app/www/audio/pronunciations/ 2>/dev/null || true

# Step 4: Create/update main HTML file for mobile
echo "Creating main HTML file for mobile..."
cat > mobile-app/www/index.html << 'EOL'
<!DOCTYPE html>
<html lang="en" data-bs-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Oxford Vocabulary Quiz</title>
    <link rel="stylesheet" href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <link rel="stylesheet" href="css/main.css">
    <link rel="stylesheet" href="css/mobile.css">
</head>
<body>
    <div id="app">
        <header class="py-2 px-3 bg-dark">
            <h1 class="h5 text-white mb-0"><i class="fas fa-book me-2"></i>Oxford Vocab Quiz</h1>
        </header>
        
        <main id="main-content" class="container">
            <!-- Quiz content will be loaded here -->
            <div class="loading-spinner">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p>Loading quiz data...</p>
            </div>
        </main>
        
        <nav class="mobile-nav">
            <a href="#home" class="nav-item active">
                <i class="fas fa-home nav-icon"></i>
                <span>Home</span>
            </a>
            <a href="#quiz" class="nav-item">
                <i class="fas fa-question-circle nav-icon"></i>
                <span>Quiz</span>
            </a>
            <a href="#favorites" class="nav-item">
                <i class="fas fa-star nav-icon"></i>
                <span>Favorites</span>
            </a>
            <a href="#settings" class="nav-item">
                <i class="fas fa-cog nav-icon"></i>
                <span>Settings</span>
            </a>
        </nav>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="cordova.js"></script>
    <script src="js/index.js"></script>
    <script src="js/quiz.js"></script>
</body>
</html>
EOL

# Step 5: Update Cordova configuration
echo "Updating Cordova configuration..."
cat > mobile-app/config.xml << 'EOL'
<?xml version='1.0' encoding='utf-8'?>
<widget id="com.oxfordvocabquiz.app" version="1.0.0" xmlns="http://www.w3.org/ns/widgets" xmlns:cdv="http://cordova.apache.org/ns/1.0">
    <name>OxfordVocabQuiz</name>
    <description>Learn English-Turkish vocabulary with the Oxford 3000 and 5000 word lists</description>
    <author email="support@oxfordvocabquiz.com" href="https://oxfordvocabquiz.com">
        OxfordVocabQuiz Team
    </author>
    <content src="index.html" />
    <access origin="*" />
    <allow-intent href="http://*/*" />
    <allow-intent href="https://*/*" />
    <allow-intent href="tel:*" />
    <allow-intent href="sms:*" />
    <allow-intent href="mailto:*" />
    <allow-intent href="geo:*" />
    <platform name="android">
        <allow-intent href="market:*" />
        <icon src="img/icon-192x192.png" density="xxxhdpi" />
        <icon src="img/icon-144x144.png" density="xxhdpi" />
        <icon src="img/icon-96x96.png" density="xhdpi" />
        <icon src="img/icon-72x72.png" density="hdpi" />
        <icon src="img/icon-48x48.png" density="mdpi" />
        <preference name="AndroidWindowSplashScreenAnimatedIcon" value="img/icon-192x192.png" />
    </platform>
    <plugin name="cordova-plugin-whitelist" spec="1" />
    <plugin name="cordova-plugin-device" spec="2.0.3" />
    <plugin name="cordova-plugin-media" spec="5.0.3" />
    <plugin name="cordova-plugin-network-information" spec="2.0.2" />
</widget>
EOL

# Step 6: Create mobile-specific JavaScript
echo "Creating mobile-specific JavaScript..."
cat > mobile-app/www/js/index.js << 'EOL'
// Mobile app initialization
document.addEventListener('deviceready', onDeviceReady, false);

function onDeviceReady() {
    console.log('Cordova initialized: Device is ready');
    
    // Add event listeners
    document.querySelector('.mobile-nav').addEventListener('click', handleNavigation);
    
    // Initialize app
    loadMainPage();
}

// Navigation handler
function handleNavigation(event) {
    const target = event.target.closest('.nav-item');
    if (!target) return;
    
    event.preventDefault();
    
    // Remove active class from all nav items
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Add active class to clicked nav item
    target.classList.add('active');
    
    // Handle navigation based on href
    const href = target.getAttribute('href');
    
    switch (href) {
        case '#home':
            loadMainPage();
            break;
        case '#quiz':
            loadQuizPage();
            break;
        case '#favorites':
            loadFavoritesPage();
            break;
        case '#settings':
            loadSettingsPage();
            break;
    }
}

// Load main page
function loadMainPage() {
    const mainContent = document.getElementById('main-content');
    mainContent.innerHTML = `
        <div class="mt-4">
            <h2 class="mb-4">Oxford Vocabulary Quiz</h2>
            
            <div class="card mb-4">
                <div class="card-body">
                    <h5 class="card-title">Welcome to Oxford Vocabulary Quiz!</h5>
                    <p class="card-text">Learn English-Turkish vocabulary with the Oxford 3000 and 5000 word lists.</p>
                    <button id="start-quiz-btn" class="btn btn-primary">Start Quiz</button>
                </div>
            </div>
            
            <div class="row">
                <div class="col-6">
                    <div class="card mb-3">
                        <div class="card-body text-center">
                            <i class="fas fa-trophy fa-2x mb-2 text-warning"></i>
                            <h5 class="card-title">Oxford 3000</h5>
                            <p class="card-text">Essential words for learners</p>
                        </div>
                    </div>
                </div>
                <div class="col-6">
                    <div class="card mb-3">
                        <div class="card-body text-center">
                            <i class="fas fa-graduation-cap fa-2x mb-2 text-info"></i>
                            <h5 class="card-title">Oxford 5000</h5>
                            <p class="card-text">Advanced vocabulary</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Add event listener to start quiz button
    document.getElementById('start-quiz-btn').addEventListener('click', () => {
        loadQuizPage();
        // Also update the navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        document.querySelector('a[href="#quiz"]').classList.add('active');
    });
}

// Load quiz page
function loadQuizPage() {
    const mainContent = document.getElementById('main-content');
    mainContent.innerHTML = `
        <div class="mt-4">
            <h2 class="mb-4">Quiz</h2>
            
            <div id="quiz-settings" class="card mb-4">
                <div class="card-body">
                    <h5 class="card-title">Quiz Settings</h5>
                    
                    <div class="mb-3">
                        <label class="form-label">Quiz Mode</label>
                        <div class="btn-group w-100" role="group" id="quiz-mode-group">
                            <input type="radio" class="btn-check" name="quiz-mode" id="mode-en-tr" autocomplete="off" checked>
                            <label class="btn btn-outline-primary" for="mode-en-tr">English → Turkish</label>
                            
                            <input type="radio" class="btn-check" name="quiz-mode" id="mode-tr-en" autocomplete="off">
                            <label class="btn btn-outline-primary" for="mode-tr-en">Turkish → English</label>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Difficulty</label>
                        <div class="btn-group w-100" role="group" id="difficulty-group">
                            <input type="radio" class="btn-check" name="difficulty" id="difficulty-easy" autocomplete="off" checked>
                            <label class="btn btn-outline-success" for="difficulty-easy">Easy</label>
                            
                            <input type="radio" class="btn-check" name="difficulty" id="difficulty-medium" autocomplete="off">
                            <label class="btn btn-outline-warning" for="difficulty-medium">Medium</label>
                            
                            <input type="radio" class="btn-check" name="difficulty" id="difficulty-hard" autocomplete="off">
                            <label class="btn btn-outline-danger" for="difficulty-hard">Hard</label>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Word List</label>
                        <div class="btn-group w-100" role="group" id="word-list-group">
                            <input type="radio" class="btn-check" name="word-list" id="list-oxford3000" autocomplete="off" checked>
                            <label class="btn btn-outline-primary" for="list-oxford3000">Oxford 3000</label>
                            
                            <input type="radio" class="btn-check" name="word-list" id="list-oxford5000" autocomplete="off">
                            <label class="btn btn-outline-info" for="list-oxford5000">Oxford 5000</label>
                            
                            <input type="radio" class="btn-check" name="word-list" id="list-combined" autocomplete="off">
                            <label class="btn btn-outline-secondary" for="list-combined">Combined</label>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label for="question-count" class="form-label">Number of Questions: <span id="question-count-value">10</span></label>
                        <input type="range" class="form-range" min="5" max="50" step="5" id="question-count" value="10">
                    </div>
                    
                    <button id="start-quiz-button" class="btn btn-primary w-100">Start Quiz</button>
                </div>
            </div>
            
            <div id="quiz-container" style="display: none;">
                <!-- Quiz content will be dynamically inserted here -->
            </div>
        </div>
    `;
    
    // Update question count value when slider changes
    const questionCountSlider = document.getElementById('question-count');
    const questionCountValue = document.getElementById('question-count-value');
    questionCountSlider.addEventListener('input', () => {
        questionCountValue.textContent = questionCountSlider.value;
    });
    
    // Add event listener to start quiz button
    document.getElementById('start-quiz-button').addEventListener('click', () => {
        // Hide settings, show quiz
        document.getElementById('quiz-settings').style.display = 'none';
        document.getElementById('quiz-container').style.display = 'block';
        
        // Show placeholder - for mobile app, we'd need to implement offline capabilities
        document.getElementById('quiz-container').innerHTML = `
            <div class="alert alert-info">
                <p>In the mobile app version, the quiz would be fully functional here.</p>
                <p>The web version supports:</p>
                <ul>
                    <li>Multiple choice questions based on Oxford wordlists</li>
                    <li>English to Turkish and Turkish to English modes</li>
                    <li>Progress tracking and analytics</li>
                    <li>Spaced repetition learning</li>
                </ul>
                <button id="back-to-settings" class="btn btn-primary mt-2">Back to Settings</button>
            </div>
        `;
        
        // Add back button functionality
        document.getElementById('back-to-settings').addEventListener('click', () => {
            document.getElementById('quiz-settings').style.display = 'block';
            document.getElementById('quiz-container').style.display = 'none';
        });
    });
}

// Load favorites page (placeholder)
function loadFavoritesPage() {
    document.getElementById('main-content').innerHTML = `
        <div class="mt-4">
            <h2 class="mb-4">Favorites</h2>
            <div class="alert alert-info">
                <p>Your favorite words would be displayed here.</p>
                <p>The favorited words can be reviewed offline in the mobile app.</p>
            </div>
        </div>
    `;
}

// Load settings page (placeholder)
function loadSettingsPage() {
    document.getElementById('main-content').innerHTML = `
        <div class="mt-4">
            <h2 class="mb-4">Settings</h2>
            
            <div class="card mb-3">
                <div class="card-body">
                    <h5 class="card-title">App Settings</h5>
                    
                    <div class="form-check form-switch mb-3">
                        <input class="form-check-input" type="checkbox" id="offline-mode" checked>
                        <label class="form-check-label" for="offline-mode">Offline Mode</label>
                    </div>
                    
                    <div class="form-check form-switch mb-3">
                        <input class="form-check-input" type="checkbox" id="pronunciations" checked>
                        <label class="form-check-label" for="pronunciations">Word Pronunciations</label>
                    </div>
                    
                    <div class="form-check form-switch mb-3">
                        <input class="form-check-input" type="checkbox" id="vibration" checked>
                        <label class="form-check-label" for="vibration">Haptic Feedback</label>
                    </div>
                    
                    <hr>
                    
                    <div class="mb-3">
                        <label for="data-sync" class="form-label">Data Synchronization</label>
                        <select class="form-select" id="data-sync">
                            <option value="auto">Automatic (Wi-Fi only)</option>
                            <option value="manual">Manual</option>
                            <option value="never">Never</option>
                        </select>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">About</h5>
                    <p class="card-text">Oxford Vocabulary Quiz v1.0.0</p>
                    <p class="card-text">Learn English-Turkish vocabulary with the Oxford 3000 and 5000 word lists.</p>
                </div>
            </div>
        </div>
    `;
}
EOL

echo "=== Preparation complete ==="
echo "You can now run ./build-apk.sh to build the APK"
echo "After building, the APK will be available at:"
echo "mobile-app/platforms/android/app/build/outputs/apk/debug/app-debug.apk"