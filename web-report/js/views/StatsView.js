import Utils from '../utils/Utils.js';


class StatsView {


  constructor(data, parentNode) {
    this._data = data;
    this._parentNode = parentNode;

    this._elements = {
      nav: null,
      view: null
    };

    this._buildUI();
    document.body.removeChild(window.overlay);
  }


  _buildUI() {
    // Create row container
    const row = document.createElement('DIV');
    row.classList.add('row', 'lib-analysis');
    this._parentNode.appendChild(row);
    // Create column elements
    this._elements.nav = document.createElement('DIV');
    this._elements.nav.className = 'col-three align-left';
    this._elements.view = document.createElement('DIV');
    this._elements.view.className = 'col-seven align-left';
    // Fill DOM with layout
    row.appendChild(this._elements.nav);
    row.appendChild(this._elements.view);
    // Fill layout with content
    this._buildNav();
    this._buildArtistsInfo();
  }


  _buildNav() {
    const header = document.createElement('P');
    const artistSection = document.createElement('DIV');
    const labelSection = document.createElement('DIV');
    const genreSection = document.createElement('DIV');

    artistSection.classList.add('active')
    artistSection.classList.add('nav-item');
    labelSection.classList.add('nav-item');
    genreSection.classList.add('nav-item');

    header.innerHTML = `
      <h3 class="center">Library analysis sum up</h3>
      <em class="center">${this._data.folderPath}</em>
      <span class="center">Library analysis duration :&nbsp;<b>${Utils.secondsToTimecode(this._data.elapsedSeconds)}</b></span>
      <span class="center">${this._data.date}</span>
    `;
    artistSection.innerHTML = `
      <p><em class="lead">Artists</em></p>
      <p><b>${this._data.count.artists}</b> unique occurence(s)</p>
    `;
    labelSection.innerHTML = `
      <p><em class="lead">Label</em></p>
      <p><b>${this._data.count.labels}</b> unique occurence(s)</p>
    `;
    genreSection.innerHTML = `
      <p><em class="lead">Genres</em></p>
      <p><b>${this._data.count.genres}</b> unique occurence(s)</p>
    `;

    this._elements.nav.appendChild(header);
    this._elements.nav.appendChild(artistSection);
    this._elements.nav.appendChild(labelSection);
    this._elements.nav.appendChild(genreSection);

    artistSection.addEventListener('click', () => {
      if (!artistSection.classList.contains('active')) {
        labelSection.classList.remove('active');
        genreSection.classList.remove('active');
        artistSection.classList.add('active');
        this._elements.view.innerHTML = '';
        this._buildArtistsInfo();
      }
    });
    labelSection.addEventListener('click', () => {
      if (!labelSection.classList.contains('active')) {
        artistSection.classList.remove('active');
        genreSection.classList.remove('active');
        labelSection.classList.add('active');
        this._elements.view.innerHTML = '';
      }
    });
    genreSection.addEventListener('click', () => {
      if (!genreSection.classList.contains('active')) {
        artistSection.classList.remove('active');
        labelSection.classList.remove('active');
        genreSection.classList.add('active');
        this._elements.view.innerHTML = '';
      }
    });
  }


  // Build all artists information in right column
  _buildArtistsInfo() {
    const wrapper = document.createElement('DIV');
    wrapper.className = 'artists-wrapper';
    // Fill DOM with layout
    this._elements.view.appendChild(wrapper);
    for (let i = 0; i < this._data.artists.length; ++i) {
      window.requestAnimationFrame(() => {
        wrapper.appendChild(this._buildArtist(this._data.artists[i]));
      });
    }
  }


  // Build a single artist stat scan report
  _buildArtist(a) {
    const fragment = document.createDocumentFragment();
    const container = document.createElement('DIV');
    const artistName = document.createElement('P');
    const apparitionCount = document.createElement('P');

    container.classList.add('artist');
    artistName.innerHTML = a.artist;
    apparitionCount.innerHTML = `<i>${a.info.length} occurence(s)</i>`;

    container.addEventListener('click', this._artistModal.bind(this, a));

    container.appendChild(artistName);
    container.appendChild(apparitionCount);
    fragment.appendChild(container);
    return fragment;
  }


  _artistModal(artist) {
    const close = () => {
      window.overlay.removeEventListener('click', close);
      closeButton.removeEventListener('click', close);
      document.body.removeChild(modalBody);
      document.body.removeChild(window.overlay);
    };

    document.body.appendChild(window.overlay);

    const modalBody = document.createElement('DIV');
    const artistName = document.createElement('H1');
    const appearencesWrapper = document.createElement('DIV');
    const closeButton = document.createElement('BUTTON');

    modalBody.classList.add('modal');
    artistName.innerHTML = JSON.stringify(artist.artist);
    appearencesWrapper.classList.add('artists-wrapper');
    closeButton.innerHTML = 'Close';

    for (let i = 0; i < artist.info.length; ++i) {
      const occurence = document.createElement('DIV');
      const albumArtist = document.createElement('P');
      const albumTitle = document.createElement('P');
      const occurenceType = document.createElement('P');

      occurence.classList.add('artist');
      albumArtist.innerHTML = artist.info[i].albumArtist;
      albumTitle.innerHTML = artist.info[i].album;
      occurenceType.innerHTML = artist.info[i].as.toUpperCase();

      occurence.appendChild(albumArtist);
      occurence.appendChild(albumTitle);
      occurence.appendChild(occurenceType);
      appearencesWrapper.appendChild(occurence);
    }

    modalBody.appendChild(artistName);
    modalBody.appendChild(appearencesWrapper);
    modalBody.appendChild(closeButton);
    document.body.appendChild(modalBody);

    window.overlay.addEventListener('click', close);
    closeButton.addEventListener('click', close);
  }


}


export default StatsView;
