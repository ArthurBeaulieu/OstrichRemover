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
      Scan duration : <b>${this.secondsToTimecode(this._data.elapsedSeconds)}</b> seconds<br><br>
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
      });
    }
  }


  _buildArtist(a) {
    // Display artist header
    const fragment = document.createDocumentFragment();
    const artistName = document.createElement('P');
    artistName.className = 'lead';
    artistName.innerHTML = `${a.name} – <i>${a.albums.length} release${(a.albums.length > 1) ? `s</i>` : `</i>`}`;
    fragment.appendChild(artistName);
    // Display album header method created to display the album name when an error is found
    const displayAlbumHeader = (album, frg) => {
      const albumTitle = document.createElement('P');
      albumTitle.innerHTML = `|&nbsp;&nbsp;+&nbsp;${album.title}`;
      frg.appendChild(albumTitle);
    };
    // Iterate over artist albums
    for (let j = 0; j < a.albums.length; ++j) {
      // Display album errors
      if (a.albums[j].errors.length > 0) {
        displayAlbumHeader(a.albums[j], fragment);
        const albumErrors = document.createElement('P');
        albumErrors.innerHTML = `|&nbsp;&nbsp;|&nbsp;&nbsp;<em><u>Album errors :</u></em>`;
        fragment.appendChild(albumErrors);
        // Iterate over album errors
        for (let k = 0; k < a.albums[j].errors.length; ++k) {
          const albumError = document.createElement('P');
          albumError.innerHTML = `|&nbsp;&nbsp;|&nbsp;&nbsp;+&nbsp;<code>Error ${a.albums[j].errors[k].errorCode}</code> : ${a.albums[j].errors[k].errorValue}`;
          fragment.appendChild(albumError);
        }
      }
      // Testing album tracks if existing
      if (a.albums[j].tracks.length > 0) {
        displayAlbumHeader(a.albums[j], fragment);
        const trackErrors = document.createElement('P');
        trackErrors.innerHTML = `|&nbsp;&nbsp;|&nbsp;&nbsp;<em><u>Track errors :</u></em>`;
        fragment.appendChild(trackErrors);
        // Iterate over album tracks
        for (let l = 0; l < a.albums[j].tracks.length; ++l) {
          const trackTitle = document.createElement('P');
          trackTitle.innerHTML = `|&nbsp;&nbsp;|&nbsp;&nbsp;+&nbsp;<b>${a.albums[j].tracks[l].title}</b>`;
          fragment.appendChild(trackTitle);
          // Iterate over track errors
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


  secondsToTimecode(time) {
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
}


export default ErrorsView;
