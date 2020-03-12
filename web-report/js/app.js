import DnD from './DnD.js';
import ErrorsView from './ErrorsView.js';
import AnalyzisView from './AnalyzisView.js';


let view = null;
const scriptVersion = '1.2.8';

// Method to restore the homepage
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
      document.querySelector('#nav-title').innerHTML += ` – Meta analyzis`;
      view = new AnalyzisView(data, document.querySelector('.report-container'));
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


// Clear view action
document.querySelector('#clear-view').addEventListener('click', restoreHomepage, false);
document.querySelector('#nav-title').innerHTML += ` ${scriptVersion}`;
