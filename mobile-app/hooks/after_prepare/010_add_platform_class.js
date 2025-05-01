#!/usr/bin/env node

// Add Platform Class
// v1.0
// Automatically adds the platform class to the body tag
// after the `prepare` command. By placing the platform CSS classes
// directly in the HTML, it speeds up the rendering process for
// the web platform.

var fs = require('fs');
var path = require('path');

var rootdir = process.argv[2];

function addPlatformBodyTag(indexPath, platform) {
  // Add the platform class to the body tag
  try {
    var platformClass = 'platform-' + platform;
    var cordovaClass = 'cordova';
    
    var html = fs.readFileSync(indexPath, 'utf8');
    
    var bodyTag = findBodyTag(html);
    if(!bodyTag) return; // No opening body tag, something wrong
    
    if(bodyTag.indexOf(platformClass) > -1) return; // Already added
    
    var newBodyTag = bodyTag;
    
    var classAttr = findClassAttr(bodyTag);
    if(classAttr) {
      // Body tag already has attributes and class
      if(classAttr.indexOf(platformClass) > -1) return; // Already added
      if(classAttr.indexOf(cordovaClass) > -1) return; // Already added
      newBodyTag = bodyTag.replace(classAttr, classAttr + ' ' + platformClass + ' ' + cordovaClass);
    } else {
      // Add class attribute to the body tag
      newBodyTag = bodyTag.replace('>', ' class="' + platformClass + ' ' + cordovaClass + '">');
    }
    
    html = html.replace(bodyTag, newBodyTag);
    
    fs.writeFileSync(indexPath, html, 'utf8');
    
    process.stdout.write('Added platform class (' + platform + ') to body tag.\n');
  } catch(e) {
    process.stdout.write(e);
  }
}

function findBodyTag(html) {
  // Find the body tag
  var bodyTag = html.match(/<body(?=[\s>])(.*?)>/i);
  if(!bodyTag) return null;
  return bodyTag[0];
}

function findClassAttr(bodyTag) {
  // Find the class attribute in the body tag
  var classAttr = bodyTag.match(/class\s*=\s*["'](.*)["']/i);
  if(!classAttr) return null;
  return classAttr[0];
}

if (rootdir) {
  // Go through each platform
  var platforms = process.env.CORDOVA_PLATFORMS.split(',');
  for(var x=0; x<platforms.length; x++) {
    // Open up the index.html file
    try {
      var platform = platforms[x].trim().toLowerCase();
      var indexPath;
      
      if(platform == 'android') {
        indexPath = path.join('platforms', platform, 'assets', 'www', 'index.html');
      } else {
        indexPath = path.join('platforms', platform, 'www', 'index.html');
      }
      
      if(fs.existsSync(indexPath)) {
        addPlatformBodyTag(indexPath, platform);
      }
    } catch(e) {
      process.stdout.write(e);
    }
  }
}