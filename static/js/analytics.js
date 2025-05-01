// Global chart objects to destroy and recreate
let progressChart = null;
let modeChart = null;
let difficultyChart = null;
let wordlistChart = null;
let masteryChart = null;
let weekdayChart = null;
let hourlyChart = null;
let timeTrendChart = null;

// Colors for charts
const colors = {
    primary: '#375a7f',
    success: '#00bc8c',
    info: '#3498db',
    warning: '#f39c12',
    danger: '#e74c3c',
    light: '#adb5bd',
    dark: '#303030'
};

// Initialize analytics dashboard
document.addEventListener('DOMContentLoaded', function() {
    loadAnalytics(7); // Default to 7 days
    
    // Set up time filter buttons
    document.querySelectorAll('.time-filter').forEach(button => {
        button.addEventListener('click', function() {
            document.querySelectorAll('.time-filter').forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            const days = parseInt(this.getAttribute('data-days'));
            loadAnalytics(days);
        });
    });
});

// Load all analytics data
function loadAnalytics(days) {
    showLoading();
    
    // Load summary data
    fetch('/api/analytics/summary')
        .then(response => response.json())
        .then(data => {
            if (data.quiz_count === 0) {
                showNoData();
                return;
            }
            
            updateSummary(data);
            hideLoading();
            document.getElementById('analytics-content').style.display = 'block';
            
            // Load additional analytics data
            loadProgressData(days);
            loadQuizTypeData();
            loadWordMasteryData();
            loadTimeDistributionData(days);
            loadLearningSpeedData(days);
            
            // Generate recommendations based on summary data
            generateRecommendations(data);
        })
        .catch(error => {
            console.error('Error loading analytics summary:', error);
            showError();
        });
}

// Update summary cards
function updateSummary(data) {
    document.getElementById('accuracy').textContent = `${data.accuracy}%`;
    
    // Handle improvement value
    const improvementElem = document.getElementById('improvement');
    if (data.improvement > 0) {
        improvementElem.textContent = `+${data.improvement}%`;
        improvementElem.className = 'badge bg-success';
    } else if (data.improvement < 0) {
        improvementElem.textContent = `${data.improvement}%`;
        improvementElem.className = 'badge bg-danger';
    } else {
        improvementElem.textContent = '0%';
        improvementElem.className = 'badge bg-secondary';
    }
    
    document.getElementById('quiz-count').textContent = data.quiz_count;
    document.getElementById('total-questions').textContent = data.total_questions;
    
    const masteredCount = data.mastery_counts.mastered || 0;
    const learningCount = data.mastery_counts.learning || 0;
    const challengingCount = data.mastery_counts.challenging || 0;
    
    document.getElementById('mastered-count').textContent = masteredCount;
    document.getElementById('mastery-progress').textContent = 
        `${learningCount} öğreniliyor, ${challengingCount} zorluk çekilen`;
    
    // Get average time from API
    fetch('/api/analytics/learning-speed')
        .then(response => response.json())
        .then(speedData => {
            document.getElementById('avg-time').textContent = 
                `${speedData.overall_avg_time}s`;
        });
}

// Load progress over time data
function loadProgressData(days) {
    fetch(`/api/analytics/progress?days=${days}`)
        .then(response => response.json())
        .then(data => {
            renderProgressChart(data);
        })
        .catch(error => {
            console.error('Error loading progress data:', error);
        });
}

// Load quiz type breakdown data
function loadQuizTypeData() {
    fetch('/api/analytics/quiz-types')
        .then(response => response.json())
        .then(data => {
            renderQuizTypeCharts(data);
        })
        .catch(error => {
            console.error('Error loading quiz type data:', error);
        });
}

// Load word mastery data
function loadWordMasteryData() {
    fetch('/api/analytics/word-mastery')
        .then(response => response.json())
        .then(data => {
            renderMasteryChart(data.mastery_counts);
            populateWordTables(data.top_words);
        })
        .catch(error => {
            console.error('Error loading word mastery data:', error);
        });
}

// Load time distribution data
function loadTimeDistributionData(days) {
    fetch(`/api/analytics/time-distribution?days=${days}`)
        .then(response => response.json())
        .then(data => {
            renderWeekdayChart(data.days_of_week);
            renderHourlyChart(data.hours_of_day);
        })
        .catch(error => {
            console.error('Error loading time distribution data:', error);
        });
}

// Load learning speed data
function loadLearningSpeedData(days) {
    fetch(`/api/analytics/learning-speed?days=${days}`)
        .then(response => response.json())
        .then(data => {
            updateLearningSpeedStats(data);
            renderTimeTrendChart(data.time_trend);
        })
        .catch(error => {
            console.error('Error loading learning speed data:', error);
        });
}

// Render progress over time chart
function renderProgressChart(data) {
    const ctx = document.getElementById('progress-chart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (progressChart) {
        progressChart.destroy();
    }
    
    progressChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [
                {
                    label: 'Doğruluk (%)',
                    data: data.accuracies,
                    backgroundColor: colors.success,
                    borderColor: colors.success,
                    tension: 0.1,
                    yAxisID: 'y'
                },
                {
                    label: 'Quiz Sayısı',
                    data: data.quiz_counts,
                    backgroundColor: colors.primary,
                    borderColor: colors.primary,
                    tension: 0.1,
                    yAxisID: 'y1',
                    type: 'bar'
                }
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Doğruluk (%)'
                    },
                    max: 100
                },
                y1: {
                    position: 'right',
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Quiz Sayısı'
                    },
                    grid: {
                        drawOnChartArea: false
                    }
                }
            },
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Zaman İçinde İlerleme'
                }
            }
        }
    });
}

// Render quiz type charts
function renderQuizTypeCharts(data) {
    // Quiz mode chart
    const modeCtx = document.getElementById('mode-chart').getContext('2d');
    if (modeChart) {
        modeChart.destroy();
    }
    
    const modeLabels = {
        'en-tr': 'İngilizce→Türkçe',
        'tr-en': 'Türkçe→İngilizce'
    };
    
    const modeData = Object.entries(data.modes || {}).map(([mode, count]) => ({
        mode: modeLabels[mode] || mode,
        count: count
    }));
    
    modeChart = new Chart(modeCtx, {
        type: 'doughnut',
        data: {
            labels: modeData.map(item => item.mode),
            datasets: [{
                data: modeData.map(item => item.count),
                backgroundColor: [colors.primary, colors.info]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
    
    // Difficulty chart
    const difficultyCtx = document.getElementById('difficulty-chart').getContext('2d');
    if (difficultyChart) {
        difficultyChart.destroy();
    }
    
    const difficultyLabels = {
        'easy': 'Kolay',
        'medium': 'Orta',
        'hard': 'Zor'
    };
    
    const difficultyData = Object.entries(data.difficulties || {}).map(([diff, count]) => ({
        difficulty: difficultyLabels[diff] || diff,
        count: count
    }));
    
    difficultyChart = new Chart(difficultyCtx, {
        type: 'doughnut',
        data: {
            labels: difficultyData.map(item => item.difficulty),
            datasets: [{
                data: difficultyData.map(item => item.count),
                backgroundColor: [colors.success, colors.warning, colors.danger]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
    
    // Word list chart
    const wordlistCtx = document.getElementById('wordlist-chart').getContext('2d');
    if (wordlistChart) {
        wordlistChart.destroy();
    }
    
    const wordlistLabels = {
        'oxford3000': 'Oxford 3000',
        'oxford5000': 'Oxford 5000',
        'combined': 'Kombine'
    };
    
    const wordlistData = Object.entries(data.word_lists || {}).map(([list, count]) => ({
        wordlist: wordlistLabels[list] || list,
        count: count
    }));
    
    wordlistChart = new Chart(wordlistCtx, {
        type: 'doughnut',
        data: {
            labels: wordlistData.map(item => item.wordlist),
            datasets: [{
                data: wordlistData.map(item => item.count),
                backgroundColor: [colors.success, colors.info, colors.warning]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Render mastery chart
function renderMasteryChart(masteryData) {
    const ctx = document.getElementById('mastery-chart').getContext('2d');
    if (masteryChart) {
        masteryChart.destroy();
    }
    
    const mastered = masteryData.mastered || 0;
    const learning = masteryData.learning || 0;
    const challenging = masteryData.challenging || 0;
    
    masteryChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Ustalaşılan', 'Öğreniliyor', 'Zorluk Çekilen'],
            datasets: [{
                data: [mastered, learning, challenging],
                backgroundColor: [colors.success, colors.warning, colors.danger]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right'
                }
            }
        }
    });
}

// Render weekday chart
function renderWeekdayChart(weekdayData) {
    const ctx = document.getElementById('weekday-chart').getContext('2d');
    if (weekdayChart) {
        weekdayChart.destroy();
    }
    
    // Translate day names to Turkish
    const turkishDays = ["Pazar", "Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi"];
    
    weekdayChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: turkishDays,
            datasets: [{
                label: 'Quiz Sayısı',
                data: weekdayData.counts,
                backgroundColor: colors.info
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Quiz Sayısı'
                    }
                }
            }
        }
    });
}

// Render hourly chart
function renderHourlyChart(hourlyData) {
    const ctx = document.getElementById('hourly-chart').getContext('2d');
    if (hourlyChart) {
        hourlyChart.destroy();
    }
    
    // Format hour labels (e.g., "00:00", "01:00", etc.)
    const hourLabels = hourlyData.labels.map(hour => 
        `${hour.toString().padStart(2, '0')}:00`);
    
    hourlyChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: hourLabels,
            datasets: [{
                label: 'Quiz Sayısı',
                data: hourlyData.counts,
                backgroundColor: colors.primary,
                borderColor: colors.primary,
                tension: 0.1,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Quiz Sayısı'
                    }
                }
            }
        }
    });
}

// Update learning speed stats
function updateLearningSpeedStats(data) {
    document.getElementById('correct-time').textContent = 
        `${data.correct_vs_incorrect.correct.avg_time || 0}s`;
    document.getElementById('correct-count').textContent = 
        `${data.correct_vs_incorrect.correct.count || 0} yanıt`;
        
    document.getElementById('incorrect-time').textContent = 
        `${data.correct_vs_incorrect.incorrect.avg_time || 0}s`;
    document.getElementById('incorrect-count').textContent = 
        `${data.correct_vs_incorrect.incorrect.count || 0} yanıt`;
}

// Render time trend chart
function renderTimeTrendChart(trendData) {
    const ctx = document.getElementById('time-trend-chart').getContext('2d');
    if (timeTrendChart) {
        timeTrendChart.destroy();
    }
    
    timeTrendChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: trendData.attempt_numbers,
            datasets: [{
                label: 'Yanıt Süresi (saniye)',
                data: trendData.avg_times,
                backgroundColor: colors.warning,
                borderColor: colors.warning,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Yanıt Süresi (saniye)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Quiz Sırası'
                    }
                }
            }
        }
    });
}

// Populate word tables
function populateWordTables(topWords) {
    // Clear existing table data
    document.getElementById('mastered-words').innerHTML = '';
    document.getElementById('learning-words').innerHTML = '';
    document.getElementById('challenging-words').innerHTML = '';
    
    // Populate mastered words table
    topWords.mastered.forEach(word => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${word.english}</td>
            <td>${word.turkish}</td>
            <td>${word.percentage}% (${word.ratio})</td>
        `;
        document.getElementById('mastered-words').appendChild(row);
    });
    
    // Populate learning words table
    topWords.learning.forEach(word => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${word.english}</td>
            <td>${word.turkish}</td>
            <td>${word.percentage}% (${word.ratio})</td>
        `;
        document.getElementById('learning-words').appendChild(row);
    });
    
    // Populate challenging words table
    topWords.challenging.forEach(word => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${word.english}</td>
            <td>${word.turkish}</td>
            <td>${word.percentage}% (${word.ratio})</td>
        `;
        document.getElementById('challenging-words').appendChild(row);
    });
}

// Generate learning recommendations
function generateRecommendations(summaryData) {
    const recommendationsList = document.getElementById('recommendations');
    recommendationsList.innerHTML = '';
    const recommendations = [];
    
    // Basic recommendations based on summary data
    if (summaryData.quiz_count < 5) {
        recommendations.push({
            text: 'Daha fazla quiz yaparak öğrenme istatistiklerinizi geliştirin.',
            icon: 'bi-graph-up'
        });
    }
    
    if (summaryData.accuracy < 70) {
        recommendations.push({
            text: 'Doğruluk oranınız düşük. Daha kolay quiz seviyesi seçmeyi deneyin.',
            icon: 'bi-speedometer'
        });
    }
    
    // Add recommendations based on word mastery
    const { mastered, learning, challenging } = summaryData.mastery_counts;
    
    if (challenging > (mastered + learning) * 0.5) {
        recommendations.push({
            text: 'Zorlandığınız çok sayıda kelime var. Tekrar sayfasını kullanarak düzenli pratik yapın.',
            icon: 'bi-arrow-repeat'
        });
    }
    
    // Add default recommendations if none were generated
    if (recommendations.length === 0) {
        recommendations.push({
            text: 'Günlük kelime öğrenme hedefinizi belirleyin ve takip edin.',
            icon: 'bi-calendar-check'
        });
        recommendations.push({
            text: 'Farklı türde quizler deneyerek öğrenmenizi çeşitlendirin.',
            icon: 'bi-shuffle'
        });
        recommendations.push({
            text: 'Zorlandığınız kelimeleri Favorilere ekleyerek daha sonra çalışın.',
            icon: 'bi-star'
        });
    }
    
    // Render recommendations
    recommendations.forEach(rec => {
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex align-items-center';
        li.innerHTML = `
            <i class="bi ${rec.icon} me-3 text-primary"></i>
            ${rec.text}
        `;
        recommendationsList.appendChild(li);
    });
}

// Show loading state
function showLoading() {
    document.getElementById('loading-message').style.display = 'block';
    document.getElementById('analytics-content').style.display = 'none';
    document.getElementById('no-data-message').style.display = 'none';
}

// Hide loading state
function hideLoading() {
    document.getElementById('loading-message').style.display = 'none';
}

// Show no data message
function showNoData() {
    document.getElementById('loading-message').style.display = 'none';
    document.getElementById('no-data-message').style.display = 'block';
}

// Show error message
function showError() {
    document.getElementById('loading-message').style.display = 'none';
    document.getElementById('analytics-content').style.display = 'none';
    document.getElementById('no-data-message').innerHTML = `
        <h4 class="alert-heading">Bir hata oluştu!</h4>
        <p>Veriler yüklenirken bir sorun oluştu. Lütfen daha sonra tekrar deneyin.</p>
    `;
    document.getElementById('no-data-message').style.display = 'block';
}