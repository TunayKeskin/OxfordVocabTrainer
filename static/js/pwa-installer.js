// PWA Installer for Oxford Vocabulary Quiz
document.addEventListener('DOMContentLoaded', function() {
    // Check if service worker is supported
    if ('serviceWorker' in navigator) {
        // Register the service worker
        navigator.serviceWorker.register('/static/js/service-worker.js')
            .then(registration => {
                console.log('Service Worker registered with scope:', registration.scope);
            })
            .catch(error => {
                console.error('Service Worker registration failed:', error);
            });
        
        // Handle 'Add to Home Screen' functionality
        let deferredPrompt;
        const installPrompt = document.getElementById('installPrompt');
        const installBtn = document.getElementById('installBtn');

        // Store the install prompt event
        window.addEventListener('beforeinstallprompt', (e) => {
            // Prevent Chrome 76+ from automatically showing the prompt
            e.preventDefault();
            // Stash the event so it can be triggered later
            deferredPrompt = e;
            // Show the install prompt if it exists in the DOM
            if (installPrompt) {
                installPrompt.style.display = 'block';
            }
        });

        // Trigger the install prompt when the user clicks the install button
        if (installBtn) {
            installBtn.addEventListener('click', async () => {
                if (!deferredPrompt) return;
                // Show the install prompt
                deferredPrompt.prompt();
                // Wait for the user to respond to the prompt
                const { outcome } = await deferredPrompt.userChoice;
                console.log(`User response to install prompt: ${outcome}`);
                // We no longer need the prompt
                deferredPrompt = null;
                // Hide the install button
                if (installPrompt) {
                    installPrompt.style.display = 'none';
                }
            });
        }

        // Hide the install UI when the app is installed
        window.addEventListener('appinstalled', (e) => {
            console.log('App was installed', e);
            if (installPrompt) {
                installPrompt.style.display = 'none';
            }
            deferredPrompt = null;
        });
    } else {
        console.log('Service workers are not supported in this browser');
    }
});