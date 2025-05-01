// Favorites management

document.addEventListener('DOMContentLoaded', function() {
    // Load favorites on page load
    loadFavorites();
    
    // Set up event delegation for delete buttons
    const favoritesList = document.getElementById('favoritesList');
    if (favoritesList) {
        favoritesList.addEventListener('click', function(event) {
            // Check if click was on a delete button
            if (event.target.classList.contains('delete-favorite') || 
                event.target.closest('.delete-favorite')) {
                const button = event.target.closest('.delete-favorite');
                const favoriteId = button.dataset.favoriteId;
                deleteFavorite(favoriteId);
            }
            
            // Check if click was on a pronunciation button
            if (event.target.classList.contains('play-pronunciation') ||
                event.target.closest('.play-pronunciation')) {
                const button = event.target.closest('.play-pronunciation');
                const word = button.dataset.word;
                playPronunciation(word);
            }
        });
    }
    
    // Set up search functionality
    const searchInput = document.getElementById('searchFavorites');
    if (searchInput) {
        searchInput.addEventListener('input', filterFavorites);
    }
});

// Load user favorites from the server
function loadFavorites() {
    const favoritesList = document.getElementById('favoritesList');
    const loadingSpinner = document.getElementById('loadingFavorites');
    const emptyMessage = document.getElementById('emptyFavorites');
    
    if (!favoritesList) return;
    
    // Show loading spinner
    if (loadingSpinner) loadingSpinner.classList.remove('d-none');
    if (emptyMessage) emptyMessage.classList.add('d-none');
    favoritesList.innerHTML = '';
    
    // Fetch favorites from API
    fetch('/api/favorites')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to load favorites');
            }
            return response.json();
        })
        .then(favorites => {
            // Hide loading spinner
            if (loadingSpinner) loadingSpinner.classList.add('d-none');
            
            // If no favorites, show empty message
            if (favorites.length === 0) {
                if (emptyMessage) emptyMessage.classList.remove('d-none');
                return;
            }
            
            // Store favorites in data attribute for filtering
            favoritesList.dataset.favorites = JSON.stringify(favorites);
            
            // Render favorites
            renderFavorites(favorites);
        })
        .catch(error => {
            console.error('Error loading favorites:', error);
            if (loadingSpinner) loadingSpinner.classList.add('d-none');
            favoritesList.innerHTML = '<div class="alert alert-danger">Failed to load favorites. Please try again.</div>';
        });
}

// Render favorites list
function renderFavorites(favorites) {
    const favoritesList = document.getElementById('favoritesList');
    favoritesList.innerHTML = '';
    
    favorites.forEach(favorite => {
        const card = document.createElement('div');
        card.className = 'card mb-3';
        card.innerHTML = `
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-center">
                    <h5 class="card-title mb-0">${favorite.english}</h5>
                    <div>
                        <button class="btn btn-sm btn-outline-info play-pronunciation" 
                                data-word="${favorite.english}">
                            <i class="fas fa-volume-up"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger delete-favorite" 
                                data-favorite-id="${favorite.favorite_id}">
                            <i class="fas fa-trash-alt"></i>
                        </button>
                    </div>
                </div>
                <p class="card-text mt-2">${favorite.turkish}</p>
                <div class="badge bg-secondary">${favorite.word_list}</div>
            </div>
        `;
        favoritesList.appendChild(card);
    });
}

// Delete a favorite
function deleteFavorite(favoriteId) {
    // Confirm deletion
    if (!confirm('Are you sure you want to remove this word from favorites?')) {
        return;
    }
    
    // Send delete request
    fetch('/api/favorites', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ favorite_id: favoriteId })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to delete favorite');
        }
        return response.json();
    })
    .then(data => {
        // Reload favorites after successful deletion
        loadFavorites();
    })
    .catch(error => {
        console.error('Error deleting favorite:', error);
        alert('Failed to delete favorite. Please try again.');
    });
}

// Play pronunciation for a word
function playPronunciation(word) {
    const audio = new Audio(`/api/pronunciation?word=${encodeURIComponent(word)}`);
    audio.play();
}

// Filter favorites based on search input
function filterFavorites() {
    const searchInput = document.getElementById('searchFavorites');
    const favoritesList = document.getElementById('favoritesList');
    const emptyMessage = document.getElementById('emptyFavorites');
    
    if (!searchInput || !favoritesList) return;
    
    const searchTerm = searchInput.value.toLowerCase().trim();
    
    // Get all favorites from data attribute
    const allFavorites = JSON.parse(favoritesList.dataset.favorites || '[]');
    
    if (searchTerm === '') {
        // If search is empty, show all favorites
        renderFavorites(allFavorites);
        if (allFavorites.length === 0 && emptyMessage) {
            emptyMessage.classList.remove('d-none');
        }
    } else {
        // Filter favorites based on search term
        const filteredFavorites = allFavorites.filter(favorite => 
            favorite.english.toLowerCase().includes(searchTerm) || 
            favorite.turkish.toLowerCase().includes(searchTerm)
        );
        
        renderFavorites(filteredFavorites);
        
        // Show empty message if no results
        if (filteredFavorites.length === 0) {
            favoritesList.innerHTML = '<div class="alert alert-info">No matching favorites found.</div>';
        }
        
        // Always hide the empty favorites message when searching
        if (emptyMessage) emptyMessage.classList.add('d-none');
    }
}
