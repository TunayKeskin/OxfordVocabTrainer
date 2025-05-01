// Oxford Vocabulary Quiz Application

// Global variables
let words = [];
let currentQuiz = [];
let currentQuestionIndex = 0;
let quizStartTime = 0;
let quizSettings = {
    mode: 'en-tr',  // en-tr or tr-en
    difficulty: 'easy',  // easy, medium, hard
    wordList: 'oxford3000'  // oxford3000 or oxford5000 or combined
};
let score = 0;
let quizInProgress = false;
let questionStartTime = 0;
let questionTimes = [];

// Initialize the quiz application
document.addEventListener('DOMContentLoaded', function() {
    // Setup UI event listeners
    setupEventListeners();
    
    // Load quiz settings from localStorage if available
    loadQuizSettings();
    
    // Update UI based on settings
    updateSettingsUI();
});

// Setup all event listeners
function setupEventListeners() {
    // Settings change listeners
    document.querySelectorAll('input[name="quizMode"]').forEach(radio => {
        radio.addEventListener('change', handleQuizModeChange);
    });
    
    document.querySelectorAll('input[name="difficulty"]').forEach(radio => {
        radio.addEventListener('change', handleDifficultyChange);
    });
    
    document.querySelectorAll('input[name="wordList"]').forEach(radio => {
        radio.addEventListener('change', handleWordListChange);
    });
    
    // Start quiz button
    const startButton = document.getElementById('startQuizBtn');
    if (startButton) {
        startButton.addEventListener('click', startQuiz);
    }
    
    // Answer submission
    const answerForm = document.getElementById('quizForm');
    if (answerForm) {
        answerForm.addEventListener('submit', handleAnswerSubmission);
    }
    
    // Next question button
    const nextButton = document.getElementById('nextBtn');
    if (nextButton) {
        nextButton.addEventListener('click', showNextQuestion);
    }
    
    // Add to favorites button
    const favoriteButton = document.getElementById('addToFavoritesBtn');
    if (favoriteButton) {
        favoriteButton.addEventListener('click', addCurrentWordToFavorites);
    }
    
    // Hear pronunciation button
    const pronunciationButton = document.getElementById('hearPronunciationBtn');
    if (pronunciationButton) {
        pronunciationButton.addEventListener('click', playWordPronunciation);
    }
}

// Load quiz settings from localStorage
function loadQuizSettings() {
    const savedSettings = localStorage.getItem('quizSettings');
    if (savedSettings) {
        quizSettings = JSON.parse(savedSettings);
    }
}

// Save quiz settings to localStorage
function saveQuizSettings() {
    localStorage.setItem('quizSettings', JSON.stringify(quizSettings));
}

// Update UI based on current settings
function updateSettingsUI() {
    // Update mode selection
    document.querySelectorAll('input[name="quizMode"]').forEach(radio => {
        radio.checked = (radio.value === quizSettings.mode);
    });
    
    // Update difficulty selection
    document.querySelectorAll('input[name="difficulty"]').forEach(radio => {
        radio.checked = (radio.value === quizSettings.difficulty);
    });
    
    // Update word list selection
    document.querySelectorAll('input[name="wordList"]').forEach(radio => {
        radio.checked = (radio.value === quizSettings.wordList);
    });
}

// Handle quiz mode change
function handleQuizModeChange(event) {
    quizSettings.mode = event.target.value;
    saveQuizSettings();
}

// Handle difficulty change
function handleDifficultyChange(event) {
    quizSettings.difficulty = event.target.value;
    saveQuizSettings();
}

// Handle word list change
function handleWordListChange(event) {
    quizSettings.wordList = event.target.value;
    saveQuizSettings();
}

// Start a new quiz
async function startQuiz() {
    // Reset quiz state
    currentQuiz = [];
    currentQuestionIndex = 0;
    score = 0;
    quizInProgress = true;
    questionTimes = [];
    
    // Show loading state
    document.getElementById('quizSetup').classList.add('d-none');
    document.getElementById('quizLoading').classList.remove('d-none');
    document.getElementById('quizContainer').classList.add('d-none');
    document.getElementById('quizResults').classList.add('d-none');
    
    try {
        // Fetch words from the API
        const response = await fetch(`/api/words?list=${quizSettings.wordList}`);
        if (!response.ok) {
            throw new Error('Failed to fetch words');
        }
        
        words = await response.json();
        
        // Create the quiz based on settings
        createQuiz();
        
        // Record the start time
        quizStartTime = Date.now();
        
        // Show the first question
        showQuestion(0);
        
        // Hide loading, show quiz
        document.getElementById('quizLoading').classList.add('d-none');
        document.getElementById('quizContainer').classList.remove('d-none');
    } catch (error) {
        console.error('Error starting quiz:', error);
        document.getElementById('quizLoading').classList.add('d-none');
        document.getElementById('quizSetup').classList.remove('d-none');
        alert('Failed to load quiz. Please try again.');
    }
}

// Create a quiz based on current settings
function createQuiz() {
    // Number of questions based on difficulty
    let questionCount = 10;  // Default for easy
    if (quizSettings.difficulty === 'medium') {
        questionCount = 20;
    } else if (quizSettings.difficulty === 'hard') {
        questionCount = 30;
    }
    
    // Shuffle the words array
    const shuffledWords = [...words].sort(() => Math.random() - 0.5);
    
    // Take the first questionCount words
    const selectedWords = shuffledWords.slice(0, questionCount);
    
    // Create the quiz questions
    currentQuiz = selectedWords.map(word => {
        // For each question, create answer options
        const correctAnswer = quizSettings.mode === 'en-tr' ? word.turkish : word.english;
        
        // Get 3 random incorrect answers
        const incorrectAnswers = getRandomIncorrectAnswers(word, 3);
        
        // Combine and shuffle all answers
        const options = [correctAnswer, ...incorrectAnswers].sort(() => Math.random() - 0.5);
        
        return {
            word: quizSettings.mode === 'en-tr' ? word.english : word.turkish,
            translation: quizSettings.mode === 'en-tr' ? word.turkish : word.english,
            options: options,
            correct: correctAnswer,
            userAnswer: null,
            timeTaken: 0,
            isCorrect: false
        };
    });
}

// Get random incorrect answers
function getRandomIncorrectAnswers(currentWord, count) {
    const field = quizSettings.mode === 'en-tr' ? 'turkish' : 'english';
    const correctAnswer = quizSettings.mode === 'en-tr' ? currentWord.turkish : currentWord.english;
    
    // Filter out the current word
    const otherWords = words.filter(word => {
        return quizSettings.mode === 'en-tr' ? 
            word.turkish !== correctAnswer : 
            word.english !== correctAnswer;
    });
    
    // Shuffle and take the required number
    return otherWords
        .sort(() => Math.random() - 0.5)
        .slice(0, count)
        .map(word => quizSettings.mode === 'en-tr' ? word.turkish : word.english);
}

// Show a specific question
function showQuestion(index) {
    if (index >= currentQuiz.length) {
        finishQuiz();
        return;
    }
    
    const question = currentQuiz[index];
    currentQuestionIndex = index;
    
    // Update progress indicator
    document.getElementById('quizProgress').textContent = `Question ${index + 1} of ${currentQuiz.length}`;
    
    // Update word display
    document.getElementById('questionWord').textContent = question.word;
    
    // Clear previous selections
    document.querySelectorAll('input[name="answer"]').forEach(radio => {
        radio.checked = false;
    });
    
    // Generate answer options
    const optionsContainer = document.getElementById('answerOptions');
    optionsContainer.innerHTML = '';
    
    question.options.forEach((option, i) => {
        const optionId = `option${i}`;
        const html = `
            <div class="form-check mb-2">
                <input class="form-check-input" type="radio" name="answer" id="${optionId}" value="${option}">
                <label class="form-check-label" for="${optionId}">${option}</label>
            </div>
        `;
        optionsContainer.insertAdjacentHTML('beforeend', html);
    });
    
    // Reset form and buttons
    document.getElementById('answerFeedback').classList.add('d-none');
    document.getElementById('submitAnswerBtn').disabled = false;
    document.getElementById('nextBtn').classList.add('d-none');
    document.getElementById('addToFavoritesBtn').classList.add('d-none');
    document.getElementById('hearPronunciationBtn').classList.add('d-none');
    
    // Record question start time
    questionStartTime = Date.now();
}

// Handle answer submission
function handleAnswerSubmission(event) {
    event.preventDefault();
    
    // Get selected answer
    const selectedOption = document.querySelector('input[name="answer"]:checked');
    if (!selectedOption) {
        alert('Please select an answer');
        return;
    }
    
    const userAnswer = selectedOption.value;
    const question = currentQuiz[currentQuestionIndex];
    const timeTaken = (Date.now() - questionStartTime) / 1000; // in seconds
    
    // Record the answer
    question.userAnswer = userAnswer;
    question.timeTaken = timeTaken;
    question.isCorrect = (userAnswer === question.correct);
    
    // Store the question time
    questionTimes.push(timeTaken);
    
    // Update score if correct
    if (question.isCorrect) {
        score++;
    }
    
    // Show feedback
    const feedbackEl = document.getElementById('answerFeedback');
    feedbackEl.innerHTML = question.isCorrect ? 
        '<div class="alert alert-success">Correct!</div>' : 
        `<div class="alert alert-danger">Incorrect. The correct answer is: ${question.correct}</div>`;
    feedbackEl.classList.remove('d-none');
    
    // Disable submit button and show next button
    document.getElementById('submitAnswerBtn').disabled = true;
    document.getElementById('nextBtn').classList.remove('d-none');
    
    // Show additional buttons
    document.getElementById('addToFavoritesBtn').classList.remove('d-none');
    document.getElementById('hearPronunciationBtn').classList.remove('d-none');
}

// Show the next question
function showNextQuestion() {
    showQuestion(currentQuestionIndex + 1);
}

// Finish the quiz and show results
function finishQuiz() {
    quizInProgress = false;
    const quizTime = (Date.now() - quizStartTime) / 1000; // in seconds
    
    // Hide quiz container, show results
    document.getElementById('quizContainer').classList.add('d-none');
    document.getElementById('quizResults').classList.remove('d-none');
    
    // Update results
    document.getElementById('quizScore').textContent = score;
    document.getElementById('quizTotal').textContent = currentQuiz.length;
    document.getElementById('quizPercentage').textContent = 
        Math.round((score / currentQuiz.length) * 100) + '%';
    document.getElementById('quizTime').textContent = 
        Math.round(quizTime) + ' seconds';
    
    // Calculate average time per question
    const avgTime = questionTimes.reduce((sum, time) => sum + time, 0) / questionTimes.length;
    document.getElementById('avgQuestionTime').textContent = 
        Math.round(avgTime * 10) / 10 + ' seconds';
    
    // Show incorrect answers if any
    const incorrectContainer = document.getElementById('incorrectAnswers');
    incorrectContainer.innerHTML = '';
    
    const incorrectQuestions = currentQuiz.filter(q => !q.isCorrect);
    
    if (incorrectQuestions.length > 0) {
        incorrectContainer.innerHTML = '<h5 class="mt-4">Words to review:</h5>';
        const list = document.createElement('ul');
        list.className = 'list-group';
        
        incorrectQuestions.forEach(q => {
            const item = document.createElement('li');
            item.className = 'list-group-item d-flex justify-content-between align-items-center';
            item.innerHTML = `
                <span>${q.word}: <strong>${q.translation}</strong></span>
                <span>Your answer: <span class="text-danger">${q.userAnswer}</span></span>
            `;
            list.appendChild(item);
        });
        
        incorrectContainer.appendChild(list);
    }
    
    // Save results to server if user is logged in
    saveQuizResults();
}

// Add current word to favorites
function addCurrentWordToFavorites() {
    if (!currentQuiz || currentQuestionIndex >= currentQuiz.length) {
        return;
    }
    
    const question = currentQuiz[currentQuestionIndex];
    const word = {
        english: quizSettings.mode === 'en-tr' ? question.word : question.translation,
        turkish: quizSettings.mode === 'en-tr' ? question.translation : question.word,
        word_list: quizSettings.wordList
    };
    
    // Send request to add to favorites
    fetch('/api/favorites', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(word)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to add to favorites');
        }
        return response.json();
    })
    .then(data => {
        alert('Word added to favorites');
    })
    .catch(error => {
        console.error('Error adding to favorites:', error);
        alert('Failed to add to favorites. Please try again or make sure you are logged in.');
    });
}

// Play the pronunciation of the current word
function playWordPronunciation() {
    if (!currentQuiz || currentQuestionIndex >= currentQuiz.length) {
        return;
    }
    
    const question = currentQuiz[currentQuestionIndex];
    const word = quizSettings.mode === 'en-tr' ? question.word : question.translation;
    
    // Create an audio element
    const audio = new Audio(`/api/pronunciation?word=${encodeURIComponent(word)}`);
    audio.play();
}

// Save quiz results to the server
function saveQuizResults() {
    // Check if user is logged in
    const isLoggedIn = document.body.classList.contains('logged-in');
    if (!isLoggedIn) {
        document.getElementById('loginPrompt').classList.remove('d-none');
        return;
    }
    
    // Prepare data
    const quizData = {
        mode: quizSettings.mode,
        difficulty: quizSettings.difficulty,
        wordList: quizSettings.wordList,
        score: score,
        timeTaken: Math.round((Date.now() - quizStartTime) / 1000),
        questions: currentQuiz.map(q => ({
            word: q.word,
            translation: q.translation,
            correct: q.isCorrect,
            timeTaken: q.timeTaken
        }))
    };
    
    // Send data to server
    fetch('/api/quiz-results', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(quizData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to save quiz results');
        }
        return response.json();
    })
    .then(data => {
        console.log('Quiz results saved:', data);
    })
    .catch(error => {
        console.error('Error saving quiz results:', error);
    });
}

// Return to setup screen
function restartQuiz() {
    document.getElementById('quizResults').classList.add('d-none');
    document.getElementById('quizSetup').classList.remove('d-none');
}

// Document event listeners for restart button
document.addEventListener('DOMContentLoaded', function() {
    const restartButton = document.getElementById('restartQuizBtn');
    if (restartButton) {
        restartButton.addEventListener('click', restartQuiz);
    }
});
