// Leaderboard functionality

document.addEventListener('DOMContentLoaded', function() {
    // Load leaderboard data
    loadLeaderboard();
    
    // Setup filter event listeners
    document.querySelectorAll('input[name="leaderboardPeriod"]').forEach(radio => {
        radio.addEventListener('change', loadLeaderboard);
    });
    
    document.querySelectorAll('input[name="leaderboardType"]').forEach(radio => {
        radio.addEventListener('change', loadLeaderboard);
    });
});

// Load leaderboard data from the server
function loadLeaderboard() {
    const leaderboardTable = document.getElementById('leaderboardTable');
    const loadingSpinner = document.getElementById('loadingLeaderboard');
    
    if (!leaderboardTable || !loadingSpinner) return;
    
    // Get filter values
    const period = document.querySelector('input[name="leaderboardPeriod"]:checked').value;
    const type = document.querySelector('input[name="leaderboardType"]:checked').value;
    
    // Show loading spinner
    loadingSpinner.classList.remove('d-none');
    leaderboardTable.classList.add('d-none');
    
    // Fetch leaderboard data
    fetch(`/api/leaderboard?period=${period}&type=${type}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to load leaderboard');
            }
            return response.json();
        })
        .then(leaderboardData => {
            // Hide loading spinner
            loadingSpinner.classList.add('d-none');
            leaderboardTable.classList.remove('d-none');
            
            // Render the leaderboard
            renderLeaderboard(leaderboardData, type);
        })
        .catch(error => {
            console.error('Error loading leaderboard:', error);
            loadingSpinner.classList.add('d-none');
            
            // Show error message
            const errorMessage = document.getElementById('leaderboardError');
            if (errorMessage) {
                errorMessage.textContent = 'Failed to load leaderboard data. Please try again.';
                errorMessage.classList.remove('d-none');
            }
        });
}

// Render the leaderboard data
function renderLeaderboard(leaderboardData, type) {
    const tableBody = document.querySelector('#leaderboardTable tbody');
    const errorMessage = document.getElementById('leaderboardError');
    
    if (!tableBody) return;
    
    // Clear the table
    tableBody.innerHTML = '';
    
    // Hide any previous error message
    if (errorMessage) errorMessage.classList.add('d-none');
    
    // Update table headers based on leaderboard type
    updateTableHeaders(type);
    
    // If no data, show message
    if (leaderboardData.length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = `<td colspan="5" class="text-center">No data available for this period.</td>`;
        tableBody.appendChild(row);
        return;
    }
    
    // Render each row
    leaderboardData.forEach((entry, index) => {
        const row = document.createElement('tr');
        
        let rankClass = '';
        if (index === 0) rankClass = 'text-warning fw-bold'; // Gold
        else if (index === 1) rankClass = 'text-secondary fw-bold'; // Silver
        else if (index === 2) rankClass = 'text-warning-emphasis fw-bold'; // Bronze
        
        // Common columns
        row.innerHTML = `
            <td class="${rankClass}">${index + 1}</td>
            <td>${entry.username}</td>
        `;
        
        // Type-specific columns
        if (type === 'success_rate') {
            row.innerHTML += `
                <td>${entry.success_rate}%</td>
                <td>${entry.quiz_count}</td>
                <td>${entry.word_count}</td>
            `;
        } else if (type === 'words_learned') {
            row.innerHTML += `
                <td>${entry.words_learned}</td>
                <td>${entry.success_rate}%</td>
                <td>${entry.quiz_count}</td>
            `;
        } else if (type === 'quiz_count') {
            row.innerHTML += `
                <td>${entry.quiz_count}</td>
                <td>${entry.success_rate}%</td>
                <td>${entry.word_count}</td>
            `;
        } else if (type === 'speed') {
            row.innerHTML += `
                <td>${entry.avg_time} sec</td>
                <td>${entry.success_rate}%</td>
                <td>${entry.quiz_count}</td>
            `;
        }
        
        tableBody.appendChild(row);
    });
}

// Update table headers based on leaderboard type
function updateTableHeaders(type) {
    const headerRow = document.querySelector('#leaderboardTable thead tr');
    if (!headerRow) return;
    
    // Set base headers
    headerRow.innerHTML = `
        <th scope="col">Rank</th>
        <th scope="col">Username</th>
    `;
    
    // Type-specific headers
    if (type === 'success_rate') {
        headerRow.innerHTML += `
            <th scope="col">Success Rate</th>
            <th scope="col">Quizzes</th>
            <th scope="col">Words</th>
        `;
    } else if (type === 'words_learned') {
        headerRow.innerHTML += `
            <th scope="col">Words Learned</th>
            <th scope="col">Success Rate</th>
            <th scope="col">Quizzes</th>
        `;
    } else if (type === 'quiz_count') {
        headerRow.innerHTML += `
            <th scope="col">Quizzes</th>
            <th scope="col">Success Rate</th>
            <th scope="col">Words</th>
        `;
    } else if (type === 'speed') {
        headerRow.innerHTML += `
            <th scope="col">Avg. Time</th>
            <th scope="col">Success Rate</th>
            <th scope="col">Quizzes</th>
        `;
    }
}
