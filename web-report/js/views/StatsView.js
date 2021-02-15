import Utils from '../utils/Utils.js';


class StatsView {


  constructor(data, parentNode) {
    this._data = data;
    this._parentNode = parentNode;

    this._elements = {
      artists: null
    };

    this._buildUI();
    document.body.removeChild(window.overlay);
  }


  _buildUI() {
    const section = document.createElement('H1');
    section.classList.add('center')
    section.innerHTML = `Artists occurences (${this._data.artists.length} unique artists)`;
    this._parentNode.appendChild(section);
    // Fill layout with content
    this._buildArtistsInfo();
  }


  // Build all artists information in right column
  _buildArtistsInfo() {
    this._elements.artists = document.createElement('DIV');
    this._elements.artists.className = 'artists-wrapper';
    // Fill DOM with layout
    this._parentNode.appendChild(this._elements.artists);
    for (let i = 0; i < this._data.artists.length; ++i) {
      window.requestAnimationFrame(() => {
        this._elements.artists.appendChild(this._buildArtist(this._data.artists[i]));
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
