'use strict';


class DnD {


	/** @summary <h1>A DnD simple implementation to convert any DOM element into a drop content handler</h1>
   * @author Arthur Beaulieu
   * @since March 2019
   * @description <blockquote>This class aims to propose a drag and drop abstraction, so you can focus on the dropped content handling only.
   * Instantiate this with a DOM target, and a file handler callback in which you might do your treatments with the dropped file(s).</blockquote>
   * @param {Object} options - The DnD class arguments object
   * @param {String} options.target - The DnD target DOM element query selector
   * @param {Function} options.onDropFile - The callback to call when a file is handled */	
	constructor(options) {
		try {
			/** @private
       * @member {Object} - The DnD container DOM node */
			this._container = document.querySelector(options.target); // Get given target from the DOM
			/** @private
       * @member {Function} - The file handler callback */			
			this._onDropFileCB = options.onDropFile; // Assign the onDropFile callback to an internal
			/** @private
       * @member {String} - The target default border rule (to properly restor border on leave/end) */			
			this._borderStyle = this._container.style.border; // Back target border style to restore it on leave/drop events
			this._events(); // Attach all drag events
		} catch(error) { // Mostly handle the case in which the target selector given as an argument is wrong
			console.error(`Unable to build the DnD class.\n${error}`);
		}
	}


	/** @method
   * @name formatAsJSON
   * @static
   * @memberof DnD
   * @description <blockquote>Convert a raw dropped content into a JSON object</blockquote> */
  static formatAsJSON(raw) {
  	return JSON.parse(raw);
  }	


	/** @method
   * @name _events
   * @private
   * @memberof DnD
   * @description <blockquote>Attach to the container all the needed drag/drop events</blockquote> */
	_events() {
		this._container.addEventListener('dragenter', this._dragEnter.bind(this), false);
		this._container.addEventListener('dragover', this._dragOver.bind(this), false);
		this._container.addEventListener('dragleave', this._dragLeave.bind(this), false);
  	this._container.addEventListener('drop', this._drop.bind(this), false);
	}


	/** @method
   * @name _eventBehavior
   * @private
   * @memberof DnD
   * @description <blockquote>Stops the given event propagation and default behavior</blockquote>
   * @param {Event} event - The event to change behavior from */
  _eventBehavior(event) {
    event.stopPropagation();
    event.preventDefault();  	
  }


	/** @method
   * @name _dragEnter
   * @private
   * @memberof DnD
   * @description <blockquote>User entered the target div with a dragged content under mouse</blockquote>
   * @param {Event} event - The event to handle */
	_dragEnter(event) {
		this._eventBehavior(event);
  	this._container.style.border = 'dashed 3px rgb(255, 100, 100)';
  }	


	/** @method
   * @name _dragOver
   * @private
   * @memberof DnD
   * @description <blockquote>User hovers the target div with a dragged content under mouse</blockquote>
   * @param {Event} event - The event to handle */
	_dragOver(event) {
		this._eventBehavior(event);
    event.dataTransfer.dropEffect = 'copy';
  }	


	/** @method
   * @name _dragLeave
   * @private
   * @memberof DnD
   * @description <blockquote>User left the target div with a dragged content under mouse</blockquote>
   * @param {Event} event - The event to handle */
	_dragLeave(event) {
		this._eventBehavior(event);
		this._container.style.border = this._borderStyle;
  }


	/** @method
   * @name _drop
   * @private
   * @memberof DnD
   * @description <blockquote>User dropped content on the target div</blockquote>
   * @param {Event} event - The event to handle */
	_drop(event) {
		this._eventBehavior(event);
		this._container.style.border = this._borderStyle;

    const files = event.dataTransfer.files;
    for (let i = 0, file; file = files[i]; ++i) {
      const reader = new FileReader();
      reader.onload = (theFile => {
        return raw => {
          this._onDropFileCB(files[i], raw);
        };
      })(file);
      reader.readAsText(file);
    }
  }
}


export default DnD;
