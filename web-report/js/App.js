import DnD from './utils/DnD.js';
import ErrorsView from './views/ErrorsView.js';
import AnalysisView from './views/AnalysisView.js';
import StatsView from './views/StatsView.js';
'use strict';


let view = null; // The active view in report-container
const scriptVersion = '1.6.1';


// Display notification global method that can accessed through window object
let timeoutIdOpacity = -1;
let timeoutIdReset = -1;
window.DisplayNotification = (type, value) => {
  clearTimeout(timeoutIdOpacity);
  clearTimeout(timeoutIdReset);
  const container = document.querySelector('.notification');
  container.classList.remove('success', 'failure'); // Clear previously set box shadows
  container.classList.add(type); // Set box shadow to notification type
  container.style.opacity = 1; // Make notification visible
  container.innerHTML = value; // Fill its text value
  timeoutIdOpacity = setTimeout(() => { container.style.opacity = 0; }, 5000); // Timeout to dim notification off
  timeoutIdReset = setTimeout(() => { container.innerHTML = ''; container.classList.remove(type); }, 5400); // Delay notification reset to match CSS animation duration
};


// Methods to restore the homepage to its initial state (DnD container displayed)
const restoreHomepage = () => {
  document.querySelector('.home-container').style.display = 'flex';
  document.querySelector('.report-container').style.display = 'none';
  document.querySelector('.report-container').innerHTML = '';
  document.querySelector('#home').blur();
  document.querySelector('#clear-view').blur();
  document.querySelector('#nav-title').innerHTML = `OstrichRemover ${scriptVersion}`;
  view = null;
};


// Method to clear view from button (display a Clear success notification too)
const clearView = () => {
  DisplayNotification('success', 'View cleared');
  restoreHomepage();
}


// Handle the UI theme
let theme = 'LIGHT';
const switchTheme = () => {
  if (theme === 'LIGHT') {
    theme = 'DARK';
    document.body.classList.remove('light-theme');
    document.body.classList.add('dark-theme');
  } else {
    theme = 'LIGHT';
    document.body.classList.remove('dark-theme');
    document.body.classList.add('light-theme');
  }
  window.localStorage.setItem('theme', theme);
};
// Init view with local storage value
if (window.localStorage.getItem('theme') === 'DARK') {
  theme = 'LIGHT'; // Force switching to dark
  switchTheme();
  document.querySelector('#theme-switch').checked = true;
}


// DnD callback to process the input JSON file
const loadJSON = (fileInfo, data) => {
  // Switch display value of main childNodes
  document.querySelector('.home-container').style.display = 'none';
  document.querySelector('.report-container').style.display = 'flex';
  // Create loading overlay
  window.overlay = document.createElement('DIV');
  window.overlay.className = 'overlay';
  document.body.appendChild(window.overlay); // Overlay must be removed in ViewClass
  // Fill view
  window.setTimeout(() => {
    if (data.artists !== undefined) {
      if (data.count !== undefined) { // The dropped JSON is a stats dump
        document.querySelector('#nav-title').innerHTML += ` – Library stats`;
        view = new StatsView(data, document.querySelector('.report-container'));
        DisplayNotification('success', 'Stats loaded');
      } else { // The dropped JSON is a scan dump
        document.querySelector('#nav-title').innerHTML += ` – Error scan`;
        view = new ErrorsView(data, document.querySelector('.report-container'));
        DisplayNotification('success', 'Error scan loaded');
      }
    } else if (data.dumps !== undefined && data.metaAnalyze !== undefined) { // The dropped JSON is a meta analysis
      document.querySelector('#nav-title').innerHTML += ` – Meta analysis`;
      view = new AnalysisView(data, document.querySelector('.report-container'));
      DisplayNotification('success', 'Meta analysis loaded');
    } else {
      DisplayNotification('failure', 'Invalid JSON file');
      document.body.removeChild(window.overlay);
      restoreHomepage();
    }
  }, 100); // Require to force the redraw of the overlay before filling the errors view
};


// Build the DnD controller and set callback
const DnDController = new DnD({
  target: '.dnd-container',
  onDropFile: (fileInfo, data) => {
    if (fileInfo.type === 'application/json') {
      loadJSON(fileInfo, DnD.formatAsJSON(data.target.result));
    } else {
      DisplayNotification('failure', 'Dropped file is not a JSON');
    }
  }
});


// Clear view events, update title and listen to theme switch
document.querySelector('#home').addEventListener('click', clearView, false); // Clear view event
document.querySelector('#clear-view').addEventListener('click', clearView, false); // Clear view event
document.querySelector('#nav-title').innerHTML += ` ${scriptVersion}`; // Append script version to initialize page title
document.querySelector('#theme-switch').addEventListener('click', switchTheme, false); // React to theme switching
