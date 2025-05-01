// This file is a placeholder for the real cordova.js that will be injected by the Cordova build process.
// This is required because we reference cordova.js in our HTML files, 
// but the actual file is generated during the build process.

// If you're testing in a browser that doesn't have the Cordova runtime,
// this will provide a mock implementation of some basic Cordova functionality.

(function() {
    var cordova = window.cordova || {};
    var cordovaPlugins = cordova.plugins || {};
    
    // Create a mock navigator object if it doesn't exist
    if (!window.navigator) {
        window.navigator = {};
    }
    
    // Mock device ready event
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Mock cordova.js loaded - This is not the real Cordova runtime');
        
        // Dispatch deviceready event after a short delay
        setTimeout(function() {
            var event = document.createEvent('Event');
            event.initEvent('deviceready', true, true);
            document.dispatchEvent(event);
            console.log('Fired deviceready event');
        }, 500);
    });
    
    // Mock some common Cordova APIs
    cordova.platformId = 'browser';
    cordova.version = '11.0.0';
    
    // Basic platform detection
    var userAgent = window.navigator.userAgent || '';
    if (/android/i.test(userAgent)) {
        cordova.platformId = 'android';
    } else if (/iphone|ipad|ipod/i.test(userAgent)) {
        cordova.platformId = 'ios';
    }
    
    // Mock device plugin
    cordovaPlugins.device = {
        platform: cordova.platformId,
        version: '1.0.0',
        manufacturer: 'Mock Device',
        isVirtual: true,
        model: 'Mock Model',
        uuid: 'mock-uuid-' + Math.floor(Math.random() * 100000)
    };
    
    // Mock network information plugin
    var connection = {
        type: 'wifi',
        getInfo: function(successCallback, errorCallback) {
            successCallback(this.type);
        }
    };
    
    cordovaPlugins.connection = connection;
    navigator.connection = connection;
    
    // Mock notification plugin
    cordovaPlugins.notification = {
        alert: function(message, alertCallback, title, buttonName) {
            window.alert(message);
            if (alertCallback) alertCallback();
        },
        confirm: function(message, confirmCallback, title, buttonLabels) {
            var result = window.confirm(message);
            if (confirmCallback) confirmCallback(result ? 1 : 2);
        },
        prompt: function(message, promptCallback, title, buttonLabels, defaultText) {
            var result = window.prompt(message, defaultText || '');
            if (promptCallback) promptCallback({ buttonIndex: result ? 1 : 2, input1: result });
        },
        beep: function(times) {
            console.log('BEEP! (times: ' + times + ')');
        }
    };
    
    // Mock the Media plugin
    function Media(src, successCallback, errorCallback, statusCallback) {
        this.src = src;
        this.successCallback = successCallback;
        this.errorCallback = errorCallback;
        this.statusCallback = statusCallback;
        this.position = 0;
        this.duration = 10; // Mock duration in seconds
        
        console.log('Created mock Media for: ' + src);
    }
    
    Media.prototype.play = function() {
        console.log('Mock Media: playing ' + this.src);
        if (this.statusCallback) this.statusCallback(Media.MEDIA_STARTING);
        
        var audio = new Audio(this.src);
        this._audio = audio;
        
        audio.addEventListener('ended', function() {
            if (this.statusCallback) this.statusCallback(Media.MEDIA_STOPPED);
            if (this.successCallback) this.successCallback();
        }.bind(this));
        
        audio.addEventListener('error', function() {
            if (this.statusCallback) this.statusCallback(Media.MEDIA_ERROR);
            if (this.errorCallback) this.errorCallback({ code: 0, message: 'Error playing audio' });
        }.bind(this));
        
        audio.play().catch(function(err) {
            console.error('Error playing audio:', err);
        });
        
        if (this.statusCallback) this.statusCallback(Media.MEDIA_RUNNING);
    };
    
    Media.prototype.pause = function() {
        console.log('Mock Media: pausing ' + this.src);
        if (this._audio) this._audio.pause();
        if (this.statusCallback) this.statusCallback(Media.MEDIA_PAUSED);
    };
    
    Media.prototype.stop = function() {
        console.log('Mock Media: stopping ' + this.src);
        if (this._audio) {
            this._audio.pause();
            this._audio.currentTime = 0;
        }
        if (this.statusCallback) this.statusCallback(Media.MEDIA_STOPPED);
    };
    
    Media.prototype.release = function() {
        console.log('Mock Media: releasing ' + this.src);
        if (this._audio) {
            this._audio.pause();
            this._audio = null;
        }
    };
    
    Media.prototype.getCurrentPosition = function(successCallback, errorCallback) {
        var position = 0;
        if (this._audio) position = this._audio.currentTime;
        if (successCallback) successCallback(position);
    };
    
    Media.prototype.getDuration = function() {
        return this._audio ? this._audio.duration : this.duration;
    };
    
    Media.prototype.seekTo = function(position) {
        if (this._audio) this._audio.currentTime = position / 1000; // Convert ms to seconds
    };
    
    Media.prototype.setVolume = function(volume) {
        if (this._audio) this._audio.volume = volume;
    };
    
    // Media states
    Media.MEDIA_NONE = 0;
    Media.MEDIA_STARTING = 1;
    Media.MEDIA_RUNNING = 2;
    Media.MEDIA_PAUSED = 3;
    Media.MEDIA_STOPPED = 4;
    Media.MEDIA_ERROR = 9;
    
    // Assign to window and cordova objects
    window.Media = Media;
    cordovaPlugins.Media = Media;
    
    // Assign plugins to cordova
    cordova.plugins = cordovaPlugins;
    
    // Assign cordova to window
    window.cordova = cordova;
    
    console.log('Mock Cordova environment initialized');
})();