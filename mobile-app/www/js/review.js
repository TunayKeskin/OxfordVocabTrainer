// Spaced repetition review system

document.addEventListener('DOMContentLoaded', function() {
    // Load words due for review
    loadWordsForReview();
    
    // Set up event listeners
    setupReviewEventListeners();
});

// Current review state
let reviewWords = [];
let currentWordIndex = 0;
let reviewMode = 'en-tr'; // Default to English to Turkish

// Setup event listeners for the review system
function setupReviewEventListeners() {
    // Review mode toggle
    const modeToggle = document.getElementById('reviewModeToggle');
    if (modeToggle) {
        modeToggle.addEventListener('change', toggleReviewMode);
    }
    
    // Show answer button
    const showAnswerBtn = document.getElementById('showAnswerBtn');
    if (showAnswerBtn) {
        showAnswerBtn.addEventListener('click', showAnswer);
    }
    
    // Feedback buttons
    document.querySelectorAll('.feedback-btn').forEach(button => {
        button.addEventListener('click', function() {
            const feedback = this.dataset.feedback;
            submitFeedback(feedback);
        });
    });
    
    // Start review button
    const startReviewBtn = document.getElementById('startReviewBtn');
    if (startReviewBtn) {
        startReviewBtn.addEventListener('click', startReview);
    }
    
    // Pronunciation button
    const pronBtn = document.getElementById('reviewPronunciationBtn');
    if (pronBtn) {
        pronBtn.addEventListener('click', playCurrentWordPronunciation);
    }
}

// Load words that are due for review
function loadWordsForReview() {
    const reviewContainer = document.getElementById('reviewContainer');
    const setupContainer = document.getElementById('reviewSetupContainer');
    const loadingSpinner = document.getElementById('loadingReview');
    const noWordsMessage = document.getElementById('noWordsForReview');
    
    if (!reviewContainer || !setupContainer) return;
    
    // Show loading spinner
    if (loadingSpinner) loadingSpinner.classList.remove('d-none');
    if (noWordsMessage) noWordsMessage.classList.add('d-none');
    
    // Fetch words due for review
    fetch('/api/words-for-review')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to load review words');
            }
            return response.json();
        })
        .then(words => {
            // Hide loading spinner
            if (loadingSpinner) loadingSpinner.classList.add('d-none');
            
            // Store words for review
            reviewWords = words;
            
            // Update word count
            const wordCountEl = document.getElementById('reviewWordCount');
            if (wordCountEl) {
                wordCountEl.textContent = words.length;
            }
            
            // Enable/disable start button based on word count
            const startBtn = document.getElementById('startReviewBtn');
            if (startBtn) {
                startBtn.disabled = words.length === 0;
            }
            
            // Show appropriate message if no words
            if (words.length === 0 && noWordsMessage) {
                noWordsMessage.classList.remove('d-none');
            }
        })
        .catch(error => {
            console.error('Error loading review words:', error);
            if (loadingSpinner) loadingSpinner.classList.add('d-none');
            
            // Show error message
            const errorEl = document.createElement('div');
            errorEl.className = 'alert alert-danger';
            errorEl.textContent = 'Failed to load words for review. Please try again.';
            setupContainer.appendChild(errorEl);
        });
}

// Toggle between English-Turkish and Turkish-English review modes
function toggleReviewMode() {
    const modeToggle = document.getElementById('reviewModeToggle');
    if (!modeToggle) return;
    
    reviewMode = modeToggle.checked ? 'tr-en' : 'en-tr';
    
    // Update mode label
    const modeLabel = document.getElementById('reviewModeLabel');
    if (modeLabel) {
        modeLabel.textContent = reviewMode === 'en-tr' ? 'English → Turkish' : 'Turkish → English';
    }
}

// Start the review session
function startReview() {
    if (reviewWords.length === 0) {
        alert('No words available for review.');
        return;
    }
    
    // Reset current index
    currentWordIndex = 0;
    
    // Hide setup, show review
    document.getElementById('reviewSetupContainer').classList.add('d-none');
    document.getElementById('reviewContainer').classList.remove('d-none');
    
    // Show first word
    showCurrentWord();
}

// Show the current word
function showCurrentWord() {
    if (currentWordIndex >= reviewWords.length) {
        // Review completed
        finishReview();
        return;
    }
    
    const currentWord = reviewWords[currentWordIndex];
    
    // Update progress
    document.getElementById('reviewProgress').textContent = 
        `Word ${currentWordIndex + 1} of ${reviewWords.length}`;
    
    // Show the question word based on mode
    const wordEl = document.getElementById('reviewWord');
    if (wordEl) {
        wordEl.textContent = reviewMode === 'en-tr' ? currentWord.english : currentWord.turkish;
    }
    
    // Hide answer initially
    const answerEl = document.getElementById('reviewAnswer');
    if (answerEl) {
        answerEl.textContent = '';
        answerEl.classList.add('d-none');
    }
    
    // Show examples if available
    const examplesContainer = document.getElementById('reviewExamples');
    if (examplesContainer) {
        examplesContainer.innerHTML = '';
        examplesContainer.classList.add('d-none');
    }
    
    // Reset buttons
    document.getElementById('showAnswerBtn').classList.remove('d-none');
    document.getElementById('feedbackButtons').classList.add('d-none');
}

// Show the answer for the current word
function showAnswer() {
    const currentWord = reviewWords[currentWordIndex];
    
    // Show the answer
    const answerEl = document.getElementById('reviewAnswer');
    if (answerEl) {
        answerEl.textContent = reviewMode === 'en-tr' ? currentWord.turkish : currentWord.english;
        answerEl.classList.remove('d-none');
    }
    
    // Hide show answer button, show feedback buttons
    document.getElementById('showAnswerBtn').classList.add('d-none');
    document.getElementById('feedbackButtons').classList.remove('d-none');
    
    // Load and show examples
    loadExamplesForCurrentWord();
}

// Load examples for the current word
function loadExamplesForCurrentWord() {
    const currentWord = reviewWords[currentWordIndex];
    const examplesContainer = document.getElementById('reviewExamples');
    
    if (!examplesContainer) return;
    
    const english = currentWord.english;
    
    // Show loading indicator
    examplesContainer.innerHTML = '<div class="text-center"><div class="spinner-border spinner-border-sm text-secondary" role="status"></div> Loading examples...</div>';
    examplesContainer.classList.remove('d-none');
    
    // Fetch examples from the API
    fetch(`/api/examples?word=${encodeURIComponent(english)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to load examples');
            }
            return response.json();
        })
        .then(examples => {
            // Display examples
            if (examples.length > 0) {
                examplesContainer.innerHTML = '<h5 class="mt-3">Examples:</h5>';
                
                const list = document.createElement('ul');
                list.className = 'list-group';
                
                examples.forEach(example => {
                    const item = document.createElement('li');
                    item.className = 'list-group-item';
                    item.innerHTML = `
                        <p class="mb-1"><strong>EN:</strong> ${example.english_sentence}</p>
                        <p class="mb-0"><strong>TR:</strong> ${example.turkish_sentence}</p>
                    `;
                    list.appendChild(item);
                });
                
                examplesContainer.appendChild(list);
            } else {
                examplesContainer.innerHTML = '<p class="text-muted">No examples available for this word.</p>';
            }
        })
        .catch(error => {
            console.error('Error loading examples:', error);
            examplesContainer.innerHTML = '<p class="text-danger">Failed to load examples.</p>';
        });
}

// Submit user feedback on word recall
function submitFeedback(feedback) {
    const currentWord = reviewWords[currentWordIndex];
    
    // Send feedback to the server
    fetch('/api/review-feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            word_id: currentWord.id,
            feedback: feedback,
            review_mode: reviewMode
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to submit feedback');
        }
        return response.json();
    })
    .then(data => {
        // Move to next word
        currentWordIndex++;
        showCurrentWord();
    })
    .catch(error => {
        console.error('Error submitting feedback:', error);
        alert('Failed to save your progress. Please try again.');
    });
}

// Finish the review session
function finishReview() {
    // Hide review container, show completion message
    document.getElementById('reviewContainer').classList.add('d-none');
    
    // Show congratulatory message
    const completionMessage = document.createElement('div');
    completionMessage.className = 'alert alert-success text-center my-4';
    completionMessage.innerHTML = `
        <h4>Review Complete!</h4>
        <p>You've reviewed ${reviewWords.length} words. Great job!</p>
        <button class="btn btn-primary mt-2" onclick="restartReview()">Return to Review Setup</button>
    `;
    
    // Add to page
    const mainContainer = document.querySelector('.container');
    mainContainer.appendChild(completionMessage);
}

// Restart the review process
function restartReview() {
    // Remove completion message
    const completionMessage = document.querySelector('.alert.alert-success');
    if (completionMessage) {
        completionMessage.remove();
    }
    
    // Show setup container
    document.getElementById('reviewSetupContainer').classList.remove('d-none');
    
    // Reload words for review
    loadWordsForReview();
}

// Play pronunciation for the current word
function playCurrentWordPronunciation() {
    if (!reviewWords || currentWordIndex >= reviewWords.length) {
        return;
    }
    
    const currentWord = reviewWords[currentWordIndex];
    const word = reviewMode === 'en-tr' ? currentWord.english : currentWord.english; // Always use English for pronunciation
    
    // Create audio element
    const audio = new Audio(`/api/pronunciation?word=${encodeURIComponent(word)}`);
    audio.play();
}
