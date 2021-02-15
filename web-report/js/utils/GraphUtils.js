import Utils from './Utils.js'


const MonthMap = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const Tooltip = { offset: 16 };


class GraphUtils {


  constructor() {

  }


  /* Graph creation - create an empty graph that must be filled with lines and areas in caller */


  // This method must be called before any other static method presented hereby
  static createGraph(options) {
    // To be passed by caller
    this._parent = options.parent;
    this._data = options.data;
    this._xAxisValue = options.xAxis;
    this._yAxisValue = options.yAxis;
    this._title = options.title;
    // Internally set from passed variables
    this._styles = null;
    this._svg = null;
    this._x = null;
    this._y = null;
    this._displayedDays = [];
    // Legend internals
    this._legends = [];
    this._colors = [];
    // Mouse over
    this._mouseG = null;
    // Function chaining to prepare the graph to be filled
    GraphUtils.defineStyles();
    GraphUtils.createSVG();
    GraphUtils.createAxis(options.yAxis);
  }


  // Extract styles from parent div to adapt the graph to the layout
  static defineStyles() {
    const margin = 50;
    const controlsOffset = this._parent.lastChild.clientHeight;
    this._parent.style.padding = '0';
    this._parent.style.overflowY = 'inherit';
    // Build styles object in a generic way
    this._styles = {
      height: this._parent.clientHeight - (2.5 * margin) - controlsOffset,
      width: this._parent.clientWidth - (2.5 * margin),
      color: 'grey',
      margin: {
        top: margin,
        right: margin,
        bottom: margin,
        left: margin
      }
    }
  }


  // This method set legend and make graph interactive, must be called after
  // every data addition to the graph so events are on top of every vectors
  static makeActive() {
    this.appendAxis();
    this.createGraphElements();
    this.mouseEvents();
    this.setLegend(); // Legend last to keep it above mouse event vectors
  }


  // Create the svg parent element
  static createSVG() {
    this._svg = d3.select(this._parent).append('svg')
      .attr('id', 'svg-canvas')
      .attr('width', (this._styles.width + this._styles.margin.left + this._styles.margin.right))
      .attr('height', (this._styles.height + this._styles.margin.top + this._styles.margin.bottom))
      .append('g')
      .attr('transform', `translate(${(1.3 * this._styles.margin.left)}, ${this._styles.margin.top})`);
  }


  // Create the axis system ; xAxis must always be a Date in this configuration
  static createAxis(type = null) {
    // Create axis range in layout
    this._x = d3.scaleTime().range([0, this._styles.width]);
    this._y = d3.scaleLinear().range([this._styles.height, 0]);
    // Create axis domains according to data type
    this._x.domain(d3.extent(this._data, d => { return d[this._xAxisValue]; })); // Date axis is handled in a different way than min/max concept
    this._y.domain([0, d3.max(this._data, d => { return d[this._yAxisValue]; })]); // Min max scale
    // Display only one date every delta to avoid date overlaping in axis labels
    const delta = Math.floor(this._data.length / 12);
    for (let i = 0; i < this._data.length; i += delta) {
      this._displayedDays.push(this._data[i].date);
    }
  }


  // Method to append axis to the svg graph. Preferable to call after appending data so data doesn't overlap axis
  static appendAxis() {
    const makeYAxisBacklines = () => {
      return d3.axisLeft(this._y)
        .tickSize(-this._styles.width, 0, 0)
        .tickFormat('');
    };

    // Add the X axis
    this._svg.append('g')
      .attr('class', 'x-axis')
      .attr('transform', `translate(0, ${this._styles.height})`)
      .call(d3.axisBottom(this._x) // Call for x axis
        .tickValues(this._displayedDays)
        .tickFormat(d3.timeFormat('%m/%Y'))) // Only keep month and year.
      .attr('dy', '.35em')
      .attr('y', 0)
      .attr('x', 9)
      .style('text-anchor', 'middle')
      .selectAll('text') // Altering label to make them italic and not perpendicular to axis
        .attr('y', 0)
        .attr('x', 9)
        .attr('dy', '.35em')
        .attr('transform', 'rotate(55)')
        .style('text-anchor', 'start');
    // Append x axis label
    this._svg.append('text')
        .attr('transform', `translate(${(this._styles.width)}, ${(this._styles.height - (this._styles.margin.top / 8))})`)
        .style('text-anchor', 'end')
        .style('font-size', '.75rem')
        .style('fill', this._styles.color)
        .text('Date'); // X axis label is always a date so far
    // Add the Y axis
    if (this._yAxisValue === 'size') { // Size is bytes and therefore must be converted
      this._svg.append('g')
        .attr('class', 'y-axis')
        .call(d3.axisLeft(this._y) // Call for y axis
        .tickFormat(d => { return Utils.convertBytes(d); })); // We convert bytes on each tick value
    } else {
      // Default Y axis addition
      this._svg.append('g')
        .call(d3.axisLeft(this._y));
    }
    // Call for grid background line
    this._svg.append('g')
      .attr('class', 'grid')
      .call(makeYAxisBacklines())
    // Text label for the y axis
    this._svg.append('text')
      .attr('transform', 'rotate(90)')
      .attr('y', 0 - (this._styles.margin.left / 2.66))
      .attr('x', 0)
      .attr('dy', '1em')
      .style('text-anchor', 'start')
      .style('text-transform', 'capitalize')
      .style('font-size', '.75rem')
      .style('fill', this._styles.color)
      .text(this._yAxisValue);
  }


  // Set the graph title
  static createGraphElements() {
    // Mouse hover container
    this._mouseG = this._svg.append('g')
      .attr('class', 'mouse-over-effects');
    // Black vertical line
    this._mouseG.append('path')
      .attr('class', 'mouse-line')
      .style('stroke', this._styles.color)
      .style('stroke-width', '1px')
      .style('opacity', '0');
    // This text will contain hovered month
    this._mouseG.append('text')
      .style('fill', this._styles.color)
      .style('font-style', 'italic');
    // Graph title
    this._svg.append('text')
      .attr('x', (this._styles.width / 2))
      .attr('y', -(this._styles.margin.bottom / 3))
      .attr('text-anchor', 'middle')
      .style('font-size', '1.66rem')
      .style('fill', this._styles.color)
      .text(this._title);
  }


  // Set the graph legend : must be called when lines are in graph
  static setLegend() {
    // Create legend container
    const lineLegend = this._svg.selectAll('.lineLegend')
      .data(this._legends)
      .enter().append('g')
      .attr('class','lineLegend')
      .attr('transform', (d, i) => {
        return `translate(${this._styles.margin.left / 1.66}, ${((i + 1) * 20)})`; // i+1 to offset from top (1 item height) and 20 is line height
      });
    // Append line name
    lineLegend.append('text')
      .text(d => d)
      .style('font-size', '.8rem')
      .style('fill', this._styles.color)
      .style('text-transform', 'capitalize')
      .attr('transform', 'translate(15, 9)'); // Align texts with boxes
    // Append colored circle
    lineLegend.append('circle')
      .attr('fill', (d, i) => { return this._colors[i]; })
      .attr('cy', 4) // Offset to match text font resize to .8rem
      .attr('r', 5);
  }


  /* Graph interactivity */


  // Make the graph interactive
  static mouseEvents() {
    GraphUtils.setMousePerLine();
    this._mouseG.append('svg:rect') // append a rect to catch mouse movements on canvas
      .attr('width', this._styles.width) // can't catch mouse events on a g element
      .attr('height', this._styles.height)
      .attr('fill', 'none')
      .attr('pointer-events', 'all')
      .on('mouseout', GraphUtils._mouseOut)
      .on('mouseover', GraphUtils._mouseOver)
      .on('mousemove', GraphUtils._mouseMove);
  }


  // Set the circle and text for each data line
  static setMousePerLine() {
    // Element for each data line
    const mousePerLine = this._mouseG.selectAll('.mouse-per-line').data(this._data).enter()
      .append('g')
      .attr('class', 'mouse-per-line');
    // Circle over matching point on line
    mousePerLine.append('circle')
      .attr('r', 6)
      .style('stroke', (d, i) => { return this._colors[i]; }) // Map circle with colors
      .style('fill', 'none')
      .style('stroke-width', '1px')
      .style('opacity', '0');
    // Y axis value on line
    mousePerLine.append('text')
      .attr('transform', 'translate(10, 3)')
      .style('fill', (d, i) => { return this._colors[i]; }); // Also map text with colors
  }


  // Mouse event when cursor exits the svg area
  static _mouseOut() {
    d3.select('.mouse-line')
      .style('opacity', '0');
    d3.selectAll('.mouse-per-line circle')
      .style('opacity', '0');
    d3.selectAll('.mouse-per-line text')
      .style('opacity', '0');
    d3.select('.mouse-over-effects').select('text')
      .style('opacity', '0');
  }


  // Mouse event when cursor is over the svg area
  static _mouseOver() {
    d3.select('.mouse-line')
      .style('opacity', '1');
    d3.selectAll('.mouse-per-line circle')
      .style('opacity', '1');
    d3.selectAll('.mouse-per-line text')
      .style('opacity', '1');
    d3.select('.mouse-over-effects').select('text')
      .style('opacity', '1');
  }


  // Mouse event when cursor is moving over the svg area
  static _mouseMove() {
    const lines = document.getElementsByClassName('line');
    const mouse = d3.mouse(this);
    const tooltipsYPos = []; // Store tooltips Y pos so they can be adjusted to never overlap
    // Apply svg transformation to mouse line
    d3.select('.mouse-line')
      .attr('d', function() { return `M${mouse[0]}, ${this._styles.height} ${mouse[0]}, 0`; }.bind(GraphUtils)); // Binding bc need to access style value
    // Set hover month on top of vertical bar
    d3.select('.mouse-over-effects').select('text')
      .style('font-size', '.8rem')
      .attr('transform', `translate(${mouse[0] + (GraphUtils._styles.margin.left / 8)}, 10)`)
      .text(`${GraphUtils._x.invert(mouse[0]).getDate()} ${MonthMap[GraphUtils._x.invert(mouse[0]).getMonth()]} ${GraphUtils._x.invert(mouse[0]).getFullYear()}`);
    // Modifications for each data line
    d3.selectAll('.mouse-per-line')
      .attr('transform', function(d, i) { // We use function keyword to keep data line scope
        let translation = null;
        // Check that i has a regular value
        if (i < lines.length) {
          let beginning = 0;
          let end = lines[i].getTotalLength();
          let target = null;
          // Iterate until Y position matching the data line is found
          while (true) {
            target = Math.floor((beginning + end) / 2);
            var pos = lines[i].getPointAtLength(target);
            if ((target === end || target === beginning) && pos.x !== mouse[0]) {
              break;
            }
            // Re-define bounds
            if (pos.x > mouse[0]) {
              end = target;
            } else if (pos.x < mouse[0]) {
              beginning = target;
            } else {
              break; //position found
            }
          }
          // Prepare text data to be displayed
          let displayValue = Math.floor(GraphUtils._y.invert(pos.y));
          if (displayValue < 0) {
            displayValue = 0;
          }
          // Update data line text value
          d3.select(this).select('text') // Scope is consumed here
            .text(GraphUtils._yAxisValue === 'size' ? Utils.convertBytes(displayValue) : displayValue);
          // Set translation according to the Y position found
          translation = `translate(${mouse[0]}, ${pos.y})`;
          tooltipsYPos.push ({ index: i, y: pos.y, offset: 0 });
        }

        return translation;
      })
      .call(sel => { // Handle tooltip overlapping by preparing tooltipYPos array
        tooltipsYPos.sort((a, b) => { return (a.y - b.y); }); // Sort tooltipYPos array by y positions
        tooltipsYPos.forEach((d, i) => {
          if (i > 0) {
            const last = tooltipsYPos[i - 1].y; // From the last tooltip, calculate an offset from their current y value
            tooltipsYPos[i].offset = Math.max(0, (last + Tooltip.offset) - tooltipsYPos[i].y); // Make sure each tooltip is at least `Tooltip.offset` pixels separated
            tooltipsYPos[i].y += tooltipsYPos[i].offset; // Add offset to Y position
          }
        });
        // Then resort tooltip positions by index
        tooltipsYPos.sort((a, b) => { return (a.index - b.index); });
      })
      .select('text') // Use the tooltip offset to move text from it's g element
        .attr('transform', (d, i) => {
          if (i < lines.length) {
            return `translate(10, ${(3 + tooltipsYPos[i].offset)})`;
          }
        });
  }


  /* Graph internal elements factory */


  // Create a smoothed line (using d3 interpolation)
  static createLine(xVal, yVal, color) {
    this._legends.push(yVal);
    // Append dots each value point on graph with given color
    this._svg.selectAll('dot')
      .data(this._data).enter().append('circle')
        .attr('fill', color)
        .attr('stroke', 'none')
        .attr('cx', d => { return this._x(d[xVal]); })
        .attr('cy', d => { return this._y(d[yVal]); })
        .attr('r', 1);

    return d3.line()
      .curve(d3.curveCardinal) // Smooth curve interpolation
      .x(d => { return this._x(d[xVal]); })
      .y(d => { return this._y(d[yVal]); });
  }


  // Create a smoothed line with an area from axis to line (using d3 interpolation)
   static createArea(xVal, yVal) {
    return d3.area()
      .curve(d3.curveCardinal) // Smooth curve interpolation
      .x(d => { return this._x(d[xVal]); })
      .y0(this._styles.height)
      .y1(d => { return this._y(d[yVal]); });
  }


  /* Append graph elements into output svg */


  // Append line svg
  static appendLine(line, color) {
    this._colors.push(color) // We assume append calls are in same order as create calls (map in // color and legend)
    this._svg.append('path')
      .data([this._data])
      .attr('class', 'line')
      .style('fill', 'none')
      .attr('d', line)
      .style('stroke', color);
  }


  // Append area to svg
  static appendArea(area, color) {
    this._svg.append('path')
       .data([this._data])
       .attr('class', 'area')
       .attr('d', area)
       .style('fill', color);
  }


  static getSvg() {
    return this._svg;
  }


}


export default GraphUtils;
