import GraphFactory from '../utils/GraphFactory.js';
import Utils from '../utils/Utils.js';
'use strict';


class AnalyzisView {


  constructor(data, parentNode) {
    this._data = data;
    this._parentNode = parentNode;
    this._graphData = this._prepareGraphData();
    // Default graph is the file one, allow to reload same view on filled curve checbox toggle
    this._activeGraph = 'files';
    this._checked = false; // When initiallizing controls, the Filled curves checkbox is unchecked
    this._elements = {
      sumup: null,
      graph: null,
      controls: null,
      views: {
        files: null,
        audio: null,
        quality: null,
        size: null
      }
    }

    this._buildUI();
    document.body.removeChild(window.overlay);
  }


  // Build the analyzis interface, its content and its interactivity
  _buildUI() {
    // Fill title with library path
    const title = document.createElement('H1');
    title.innerHTML = `<em>${this._data.metaAnalyze.folderPath}</em>`
    this._parentNode.appendChild(title);
    // Create row container
    const row = document.createElement('DIV');
    row.classList.add('row');
    this._parentNode.appendChild(row);
    // Create column elements
    this._elements.sumup = document.createElement('DIV');
    this._elements.sumup.className = 'col-three align-left';
    this._elements.graph = document.createElement('DIV');
    this._elements.graph.className = 'col-seven align-left';
    // Create control container
    this._elements.controls = document.createElement('DIV');
    this._elements.controls.className = 'graph-controls';
    // Fill DOM with layout
    this._elements.graph.appendChild(this._elements.controls);
    row.appendChild(this._elements.sumup);
    row.appendChild(this._elements.graph);
    // Fill layout with content
    this._buildAnalyzeSumup();
    this._buildControls();
    this._initGraphWithSize();
  }


  // Build the left column content with variations between first and last dump of the tested dataset
  _buildAnalyzeSumup() {
    // Shortcut for meta analysis, first dump and last dump
    const ma = this._data.metaAnalyze;
    const fd = this._data.dumps[0];
    const ld = this._data.dumps[this._data.dumps.length - 1];
    // DOM nodes declaration
    const header = document.createElement('P');
    const fsInfo = document.createElement('P');
    const lbInfo = document.createElement('P');
    const qDetails = document.createElement('P');
    // HTML markup
    header.innerHTML = `
      <h3 class="center">Meta analyzis sum up</h3><span class="center"><b>${fd.date}</b>&nbsp;→&nbsp;<b>${ld.date}</b></span>
    `;
    fsInfo.innerHTML = `
       <u><em class="lead">File system info</em></u>
       <br>Size: <b>${Utils.convertBytes(fd.folderInfo.size)}</b> → <b>${Utils.convertBytes(ld.folderInfo.size)}</b>
       <b style="float: right">${Utils.convertBytes(ma.sizeDelta)}</b><br>
       Files: <b>${fd.folderInfo.files}</b> → <b>${ld.folderInfo.files}</b>
       ${Utils.setColorFromValue(ma.filesDelta)}<br>
       Folders: <b>${fd.folderInfo.folders}</b> → <b>${ld.folderInfo.folders}</b>
       ${Utils.setColorFromValue(ma.foldersDelta)}<br>
    `;
    lbInfo.innerHTML = `
      <u><em class="lead">Library info</em></u>
      <br>Artists: <b>${fd.folderInfo.artistsCount}</b> → <b>${ld.folderInfo.artistsCount}</b>
      ${Utils.setColorFromValue(ma.artistsDelta)}<br>
      Albums: <b>${fd.folderInfo.albumsCount}</b> → <b>${ld.folderInfo.albumsCount}</b>
      ${Utils.setColorFromValue(ma.albumsDelta)}<br>
      Tracks: <b>${fd.folderInfo.tracksCount}</b> → <b>${ld.folderInfo.tracksCount}</b>
      ${Utils.setColorFromValue(ma.tracksDelta)}<br>
      Covers: <b>${fd.folderInfo.coversCount}</b> → <b>${ld.folderInfo.coversCount}</b>
      ${Utils.setColorFromValue(ma.coversDelta)}<br>
    `;
    qDetails.innerHTML = `
      <u><em class="lead">Quality details</em></u>
      <br>FLAC: <b>${fd.folderInfo.flacCount}</b> → <b>${ld.folderInfo.flacCount}</b>
      ${Utils.setColorFromValue(ma.flacDelta)}<br>
      MP3: <b>${fd.folderInfo.mp3Count}</b> → <b>${ld.folderInfo.mp3Count}</b>
      ${Utils.setColorFromValue(ma.mp3Delta)}<br>
      JPG: <b>${fd.folderInfo.jpgCount}</b> → <b>${ld.folderInfo.jpgCount}</b>
      ${Utils.setColorFromValue(ma.jpgDelta)}<br>
      PNG: <b>${fd.folderInfo.pngCount}</b> → <b>${ld.folderInfo.pngCount}</b>
      ${Utils.setColorFromValue(ma.pngDelta)}<br><br><br>
      Errors: <b>${fd.folderInfo.errorsCount}</b> → <b>${ld.folderInfo.errorsCount}</b>
      ${Utils.setColorFromValue(ma.errorsDelta)}<br>
      Purity: <b>${fd.folderInfo.purity}</b> % → <b>${ld.folderInfo.purity} %</b>
      ${Utils.setColorFromValue(ma.purityDelta)}<br>
    `;
    // DOM attachement
    this._elements.sumup.appendChild(header);
    this._elements.sumup.appendChild(fsInfo);
    this._elements.sumup.appendChild(lbInfo);
    this._elements.sumup.appendChild(qDetails);
    this._elements.sumup.appendChild(Utils.buildPurityProgress(ld.folderInfo.purity));
  }


  // Build graph controls that allow to control displayed data
  _buildControls() {
    // Internal DOM nodes declaration
    this._elements.views.files = document.createElement('BUTTON');
    this._elements.views.audio = document.createElement('BUTTON');
    this._elements.views.quality = document.createElement('BUTTON');
    this._elements.views.size = document.createElement('BUTTON');
    // DOM nodes declaration
    const checkboxContainer = document.createElement('DIV');
    const filledCurvesLabel = document.createElement('P');
    const checkbox = document.createElement('INPUT');
    // DOM content filled with display modes
    this._elements.views.files.innerHTML = 'Files';
    this._elements.views.audio.innerHTML = 'Audio';
    this._elements.views.quality.innerHTML = 'Quality';
    this._elements.views.size.innerHTML = 'Size';
    // Set cheboc internals and default to unchecked
    checkbox.type = 'checkbox';
    checkbox.checked = false;
    filledCurvesLabel.innerHTML = 'Filled curves';
    // DOM attachement
    checkboxContainer.appendChild(filledCurvesLabel);
    checkboxContainer.appendChild(checkbox);
    this._elements.controls.appendChild(this._elements.views.files);
    this._elements.controls.appendChild(this._elements.views.audio);
    this._elements.controls.appendChild(this._elements.views.quality);
    this._elements.controls.appendChild(this._elements.views.size);
    this._elements.controls.appendChild(checkboxContainer);
    // Controls event to change displayed graph
    this._elements.views.files.addEventListener('click', this._changeView.bind(this, 'files'), false);
    this._elements.views.audio.addEventListener('click', this._changeView.bind(this, 'audio'), false);
    this._elements.views.quality.addEventListener('click', this._changeView.bind(this, 'quality'), false);
    this._elements.views.size.addEventListener('click', this._changeView.bind(this, 'size'), false);
    // Check box to fill under curves
    checkbox.addEventListener('click', () => {
      this._checked = checkbox.checked;
      this._changeView(this._activeGraph);
    }, false);
  }


  // Initialize the graph canvas with the Files graph by default
  _initGraphWithSize() {
    // Set file button active from style
    this._elements.views.files.classList.add('active');
    // Build files graph
    const view = new GraphFactory({
      parent: this._elements.graph,
      data: this._graphData,
      type: 'files',
      area: this._checked
    });
  }


  // Replace previous graph with anothe one
  _changeView(type, area) {
    // Clear page state
    this._clearGraph();
    this._unselectAllButtons();
    // Set factory type to be later sent to GraphFactory
    let factoryType = '';
    if (type === 'files') {
      factoryType = 'files';
    } else if (type === 'audio') {
      factoryType = 'audio';
    } else if (type === 'quality') {
      factoryType = 'quality';
    } else if (type === 'size') {
      factoryType = 'size';
    } else {
      // TODO handle error
      return; // Not building any view
    }
    // Save current graph in view class
    this._activeGraph = factoryType;
    this._elements.views[this._activeGraph].classList.add('active');
    // Build graph with given type
    const view = new GraphFactory({
      parent: this._elements.graph,
      data: this._prepareGraphData(),
      type: factoryType,
      area: this._checked
    });
  }


  // Clear the right column from any svg-canvas container if existing
  _clearGraph() {
    if (document.getElementById('svg-canvas')) {
      this._elements.graph.removeChild(document.getElementById('svg-canvas'));
    }
  }


  // Reset all control buttons state and blur them to remove any outline
  _unselectAllButtons() {
    this._elements.views.files.classList.remove('active');
    this._elements.views.audio.classList.remove('active');
    this._elements.views.quality.classList.remove('active');
    this._elements.views.size.classList.remove('active');
    this._elements.views.files.blur();
    this._elements.views.audio.blur();
    this._elements.views.quality.blur();
    this._elements.views.size.blur();
  }


  // Format data from dumps to be sent in d3js graph factory
  _prepareGraphData() {
    // Define output array and date parser (to allow tick formatting later in d3)
    const parseDate = d3.timeParse("%Y-%m-%d");
    const output = [];
    // Iterate over dumps and store all useful keys
    for (let i = 0; i < this._data.dumps.length; ++i) {
      output.push({
        date: parseDate(this._data.dumps[i].date),
        version: this._data.dumps[i].version,
        elapsedSeconds: this._data.dumps[i].elapsedSeconds,
        name: this._data.dumps[i].folderInfo.name,
        files: this._data.dumps[i].folderInfo.files,
        folders: this._data.dumps[i].folderInfo.folders,
        size: this._data.dumps[i].folderInfo.size,
        totalArtists: this._data.dumps[i].folderInfo.artistsCount,
        totalAlbums: this._data.dumps[i].folderInfo.albumsCount,
        totalTracks: this._data.dumps[i].folderInfo.tracksCount,
        totalCovers: this._data.dumps[i].folderInfo.coversCount,
        totalFlac: this._data.dumps[i].folderInfo.flacCount,
        totalMp3: this._data.dumps[i].folderInfo.mp3Count,
        totalJpg: this._data.dumps[i].folderInfo.jpgCount,
        totalPng: this._data.dumps[i].folderInfo.pngCount,
        errors: this._data.dumps[i].folderInfo.errorsCount,
        possibleErrors: this._data.dumps[i].folderInfo.possibleErrors,
        purity: this._data.dumps[i].folderInfo.purity,
        flacPercentage: this._data.dumps[i].folderInfo.flacPercentage,
        mp3Percentage: this._data.dumps[i].folderInfo.mp3Percentage,
        jpgPercentage: this._data.dumps[i].folderInfo.jpgPercentage,
        pngPercentage: this._data.dumps[i].folderInfo.pngPercentage,
      });
    }

    return output;
  }


}


export default AnalyzisView;
