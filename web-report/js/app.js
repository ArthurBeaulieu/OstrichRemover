import DnD from './DnD.js';
import ErrorsView from './ErrorsView.js';


let errorsView = null;


// DnD callback to process the input JSON file
const loadJSON = (fileInfo, data) => {
  // Switch display value of main childNodes
  document.querySelector('.home-container').style.display = 'none';
  document.querySelector('.report-container').style.display = 'block';
  // Create loading overlay
  window.overlay = document.createElement('DIV');
  window.overlay.className = 'overlay';
  document.body.appendChild(window.overlay);
  // Fill view
  window.setTimeout(() => {
    errorsView = new ErrorsView(data, document.querySelector('.report-container'));
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
document.querySelector('#clear-view').addEventListener('click', () => {
  document.querySelector('.home-container').style.display = 'flex';
  document.querySelector('.report-container').style.display = 'none';
  document.querySelector('.report-container').innerHTML = '';
  document.querySelector('#clear-view').blur();
  errorsView = null;
});
