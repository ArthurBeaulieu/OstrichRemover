'use strict';


class Utils {


  constructor() {}


  // Format raw string into JSON object
  static formatAsJSON(raw) {
    return JSON.parse(raw);
  }


  // Convert byte value into a human readable string
  static convertBytes(bytes) {
    // Don't wanna try here to do any 0 division
    if (bytes === 0) {
      return '0 bytes';
    }

    const sizes = ['bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)), 10);
    if (i === 0) {
      return `${bytes} ${sizes[i]})`;
    }

    return `${(bytes / (1024 ** i)).toFixed(1)} ${sizes[i]}`;
  }


  // Convert a timestamp in seconds to a readable timecode
  static secondsToTimecode(time) {
    const transformedTime = {
      d: 0,
      h: 0,
      m: 0,
      s: 0
    };
    // Cutting total seconds
    transformedTime.d = Math.floor(time / 86400);
    transformedTime.h = Math.floor((time - (transformedTime.d * 86400)) / 3600);
    transformedTime.m = Math.floor((time - (transformedTime.d * 86400) - (transformedTime.h * 3600)) / 60);
    transformedTime.s = Math.floor(time - (transformedTime.d * 86400) - (transformedTime.h * 3600) - (transformedTime.m * 60)); // Keeping ms ICO
    // Adding an extra 0 for values inferior to 10
    if (transformedTime.d < 10) {
      transformedTime.d = `0${transformedTime.d}`;
    }
    if (transformedTime.h < 10) {
      transformedTime.h = `0${transformedTime.h}`;
    }
    if (transformedTime.m < 10) {
      transformedTime.m = `0${transformedTime.m}`;
    }
    if (transformedTime.s < 10) {
      transformedTime.s = `0${transformedTime.s}`;
    }
    // Formatting output
    if (transformedTime.d > 0) {
      return `${transformedTime.d}d ${transformedTime.h}h ${transformedTime.m}m ${transformedTime.s}s`;
    } else if (transformedTime.h > 0) {
      return `${transformedTime.h}h ${transformedTime.m}m ${transformedTime.s}s`;
    } else {
      return `${transformedTime.m}m ${transformedTime.s}s`;
    }
  }


  // Build a PurityProgress HTML element with a given purity
  static buildPurityProgress(purity) {
    // Create HTML elements
    const purityProgress = document.createElement('DIV');
    const pure = document.createElement('DIV');
    const impure = document.createElement('DIV');
    // Set CSS classes
    purityProgress.className = 'purity-progress';
    pure.className = 'pure';
    impure.className = 'impure';
    // Add layout to DOM
    purityProgress.appendChild(pure);
    purityProgress.appendChild(impure);
    // Set width from given purity for both track pure/impure
    pure.style.width = purity + '%';
    impure.style.width = 100 - purity + '%';
    // Round right borders if pure bar is almost full length
    if (purity > 98) {
      pure.style.borderRadius = 'var(--border-radius)';
    }
    // Return DOM element
    return purityProgress;
  }


  // If input value is below zero, add red color, if equal 0 do nothing for color and above zero, add green color
  // This is to make UX for understand if numbers have raised of fall
  static setColorFromValue(value) {
    let colorClass = '';
    let sign = '';
    if (value > 0) {
      colorClass = 'green';
      sign = '+';
    } else if (value < 0) {
      colorClass = 'red';
    }

    return `<b class="${colorClass}" style="float: right">${sign}${value}</b>`;
  }


}


export default Utils;
