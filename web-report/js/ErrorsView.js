class ErrorsView {
  constructor(data, parentNode) {
    this._data = data;
    this._parentNode = parentNode;
    this._elements = {
      folder: null,
      artists: null
    }
    //console.log(this._data); // Debug purpose only
    this._buildUi();
    document.body.removeChild(window.overlay);
  }


  _buildUi() {
    const title = document.createElement('H1');
    title.innerHTML = `<em>${this._data.folderInfo.name}</em>`
    this._parentNode.appendChild(title);

    const row = document.createElement('DIV');
    row.classList.add('row');
    this._parentNode.appendChild(row);

    this._elements.folder = document.createElement('DIV');
    this._elements.folder.className = 'col-three align-left';
    this._elements.artists = document.createElement('DIV');
    this._elements.artists.className = 'col-seven align-left';

    row.appendChild(this._elements.folder);
    row.appendChild(this._elements.artists);

    this._buildFolderInfo();
    this._buildArtistsInfo();
  }


  _buildFolderInfo() {
    // Shortcut for folerInfo
    const f = this._data.folderInfo;
    // DOM nodes declaration
    const libQuality = document.createElement('P');
    const libDetails = document.createElement('P');
    const audioDetails = document.createElement('P');
    const pictureDetails = document.createElement('P');
    // HTML markup
    libDetails.innerHTML = `
      <u><em class="lead">Library details</em></u><br>
      <b>${f.folders}</b> folder(s) – <b>${f.files}</b> file(s) – <b>${Math.floor(f.size > 100000000 ? f.size / 1000000000 : f.size / 1000000)} ${f.size > 100000000 ? '</b>Go' : '</b>Mo'}<br>
      <b>${f.artistsCount}</b> artist(s) – <b>${f.albumsCount}</b> albums(s)<br>
      <b>${f.tracksCount}</b> track(s) – <b>${f.coversCount}</b> artwork(s)<br>
    `;
    audioDetails.innerHTML = `
      <u><em class="lead">Audio files details</em></u><br>
      <b>${f.flacCount}</b> flac file(s)<span style="float: right"><b>${f.flacPercentage}</b> %</span><br><b>${f.mp3Count}</b> mp3 file(s)<span style="float: right"><b>${f.mp3Percentage}</b> %</span><br>
    `;
    pictureDetails.innerHTML = `
      <u><em class="lead">Picture files details</em></u><br>
      <b>${f.jpgCount}</b> jpg file(s)<span style="float: right"><b>${f.jpgPercentage}</b> %</span><br><b>${f.pngCount}</b> png file(s)<span style="float: right"><b>${f.pngPercentage}</b> %</span><br>
    `;
    libQuality.innerHTML = `
      <u><em class="lead">Library quality</em></u><br>
      Found <b>${f.errorsCount}</b> error(s)<span style="float: right"><b>${f.possibleErrors}</b> possible error(s)</span><br>
      ~ <b>${(f.errorsCount / f.artistsCount).toFixed(2)}</b> error(s) per artist<br>~ <b>${(f.errorsCount / f.albumsCount).toFixed(2)}</b> error(s) per album<br>
      ~ <b>${(f.errorsCount / f.tracksCount).toFixed(2)}</b> error(s) per track<br><br>Library purity : <b>${f.purity}</b> %
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
    pure.style.width = f.purity + '%';
    impure.style.width = 100 - f.purity + '%';
    // DOM attachement
    this._elements.folder.appendChild(libDetails);
    this._elements.folder.appendChild(audioDetails);
    this._elements.folder.appendChild(pictureDetails);
    this._elements.folder.appendChild(libQuality);
    this._elements.folder.appendChild(purityProgress);
  }


  _buildArtistsInfo() {
    for (let i = 0; i < this._data.artists.length; ++i) {
      window.requestAnimationFrame(() => {
        this._elements.artists.appendChild(this._buildArtist(this._data.artists[i]));
        const lineBreak = document.createElement('BR');
        this._elements.artists.appendChild(lineBreak);
      });
    }
  }


  _buildArtist(a) {
    const fragment = document.createDocumentFragment();
    const artistName = document.createElement('P');
    artistName.className = 'lead';
    artistName.innerHTML = a.name;
    fragment.appendChild(artistName);

    for (let j = 0; j < a.albums.length; ++j) {
      const albumTitle = document.createElement('P');
      albumTitle.innerHTML = `|&nbsp;&nbsp;+&nbsp;${a.albums[j].title}`;
      fragment.appendChild(albumTitle);

      if (a.albums[j].errors.length > 0) {
        const albumErrors = document.createElement('P');
        albumErrors.innerHTML = `|&nbsp;&nbsp;|&nbsp;&nbsp;<em><u>Album errors :</u></em>`;
        fragment.appendChild(albumErrors);

        for (let k = 0; k < a.albums[j].errors.length; ++k) {
          const albumError = document.createElement('P');
          albumError.innerHTML = `|&nbsp;&nbsp;|&nbsp;&nbsp;+&nbsp;<code>Error ${a.albums[j].errors[k].errorCode}</code> : ${a.albums[j].errors[k].errorValue}`;
          fragment.appendChild(albumError);
        }
      }

      if (a.albums[j].tracks.length > 0) {
        const trackErrors = document.createElement('P');
        trackErrors.innerHTML = `|&nbsp;&nbsp;|&nbsp;&nbsp;<em><u>Track errors :</u></em>`;
        fragment.appendChild(trackErrors);

        for (let l = 0; l < a.albums[j].tracks.length; ++l) {
          const trackTitle = document.createElement('P');
          trackTitle.innerHTML = `|&nbsp;&nbsp;|&nbsp;&nbsp;+&nbsp;<b>${a.albums[j].tracks[l].title}</b>`;
          fragment.appendChild(trackTitle);

          for (let m = 0; m < a.albums[j].tracks[l].errors.length; ++m) {
            const trackError = document.createElement('P');
            trackError.innerHTML = `|&nbsp;&nbsp;|&nbsp;&nbsp;|&nbsp;&nbsp;+&nbsp;<code>Error ${a.albums[j].tracks[l].errors[m].errorCode}</code> : ${a.albums[j].tracks[l].errors[m].errorValue}`;
            fragment.appendChild(trackError);
          }
        }
      }
    }

    return fragment;
  }
}


export default ErrorsView;
