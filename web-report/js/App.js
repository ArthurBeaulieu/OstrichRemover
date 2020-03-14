import DnD from './utils/DnD.js';
import ErrorsView from './views/ErrorsView.js';
import AnalysisView from './views/AnalysisView.js';
'use strict';


let view = null; // The active view in report-container
const scriptVersion = '1.3.1';


// Method to restore the homepage to its initial state (DnD container displayed)
const restoreHomepage = () => {
  document.querySelector('.home-container').style.display = 'flex';
  document.querySelector('.report-container').style.display = 'none';
  document.querySelector('.report-container').innerHTML = '';
  document.querySelector('#clear-view').blur();
  document.querySelector('#nav-title').innerHTML = `MzkOstrichRemover ${scriptVersion}`;
  view = null;
};


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
    if (data.artists !== undefined) { // The dropped JSON is a scan dump
      document.querySelector('#nav-title').innerHTML += ` – Error scan`;
      view = new ErrorsView(data, document.querySelector('.report-container'));
    } else if (data.dumps !== undefined && data.metaAnalyze !== undefined) { // The dropped JSON is a meta analysis
      document.querySelector('#nav-title').innerHTML += ` – Meta analysis`;
      view = new AnalysisView(data, document.querySelector('.report-container'));
    } else {
      console.error('Invalid dropped JSON')
      document.body.removeChild(window.overlay);
      restoreHomepage();
    }
  }, 100); // Require to force the redraw of the overlay before filling the errors view
};


// Build the DnD controller and set callback
const DnDController = new DnD({
  target: '.dnd-container',
  onDropFile: (fileInfo, data) => {
    loadJSON(fileInfo, DnD.formatAsJSON(data.target.result));
  }
});


document.querySelector('#clear-view').addEventListener('click', restoreHomepage, false); // Clear view event
document.querySelector('#nav-title').innerHTML += ` ${scriptVersion}`; // Append script version to initialize page title
