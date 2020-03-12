'use strict';


class Utils {


  constructor() {

  }


  static formatAsJSON(raw) {
    return JSON.parse(raw);
  }


  static convertBytes(bytes) {
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
    transformedTime.s = time - (transformedTime.d * 86400) - (transformedTime.h * 3600) - (transformedTime.m * 60); // Keeping ms ICO
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
      return `${transformedTime.h}:${transformedTime.m}:${transformedTime.s}`;
    } else {
      return `${transformedTime.m}:${transformedTime.s}`;
    }
  }


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
