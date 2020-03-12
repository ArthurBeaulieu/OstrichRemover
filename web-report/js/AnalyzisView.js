import Utils from './Utils.js';


class AnalyzisView {


  constructor(data, parentNode) {
    this._data = data;
    this._parentNode = parentNode;
    this._elements = {
      sumup: null,
      graph: null
    }

    this._buildUI();
    document.body.removeChild(window.overlay);
  }


  _buildUI() {
    const title = document.createElement('H1');
    title.innerHTML = `<em>${this._data.metaAnalyze.folderPath}</em>`
    this._parentNode.appendChild(title);

    const row = document.createElement('DIV');
    row.classList.add('row');
    this._parentNode.appendChild(row);

    this._elements.sumup = document.createElement('DIV');
    this._elements.sumup.className = 'col-three align-left';
    this._elements.graph = document.createElement('DIV');
    this._elements.graph.className = 'col-seven align-left';

    row.appendChild(this._elements.sumup);
    row.appendChild(this._elements.graph);

    this._buildAnalyzeSumup();
    this._buildGraph();
  }


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
      Purity: <b>${fd.folderInfo.purity}</b> → <b>${ld.folderInfo.purity}</b>
      ${Utils.setColorFromValue(ma.purityDelta)}<br>
    `;
    // Purity progress
    const purityProgress = document.createElement('DIV');
    purityProgress.className = 'purity-progress';
    const pure = document.createElement('DIV');
    pure.className = 'pure';
    const impure = document.createElement('DIV');
    impure.className = 'impure';
    purityProgress.appendChild(pure);
    purityProgress.appendChild(impure);
    pure.style.width = ld.folderInfo.purity + '%';
    impure.style.width = 100 - ld.folderInfo.purity + '%';
    // DOM attachement
    this._elements.sumup.appendChild(header);
    this._elements.sumup.appendChild(fsInfo);
    this._elements.sumup.appendChild(lbInfo);
    this._elements.sumup.appendChild(qDetails);
    this._elements.sumup.appendChild(purityProgress);
  }


  _buildGraph() {
    // TODO : implement d3js graphes
  }


}


export default AnalyzisView;
