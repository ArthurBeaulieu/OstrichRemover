import Utils from './Utils.js'
'use strict';


class GraphUtils {


  constructor() {
    // To be passed by caller
    this._parent = null;
    this._data = null;
    this._xAxisValue = null;
    this._yAxisValue = null;
    this._title = null;
    this._type = null;
    // Internally set from passed variables
    this._styles = null;
    this._svg = null;
    this._x = null;
    this._y = null;
  }


  /* Graph creation - create an empty graph that must be filled with lines and areas in caller */


  // This method must be called before any other static method presented hereby
  static createGraph(options) {
    this._parent = options.parent;
    this._data = options.data;
    this._xAxisValue = options.xAxis;
    this._yAxisValue = options.yAxis;
    this._title = options.title;
    // Function chaining to prepare the graph to be filled
    GraphUtils.defineStyles();
    GraphUtils.createSVG();
    GraphUtils.createAxis(options.yAxis);
    GraphUtils.setTitle();
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
      margin: {
        top: margin,
        right: margin,
        bottom: margin,
        left: margin
      }
    }
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
    const displayedDates = [];
    const delta = Math.floor(this._data.length / 12);
    for (let i = 0; i < this._data.length; i += delta) {
      displayedDates.push(this._data[i].date);
    }
    // Add the X axis
    this._svg.append('g')
      .attr('class', 'x-axis')
      .attr('transform', `translate(0, ${this._styles.height})`)
      .call(d3.axisBottom(this._x) // Call for x axis
        .tickValues(displayedDates)
        .tickFormat(d3.timeFormat("%m/%Y"))) // Only keep mont and year.
      .attr('dy', '.35em')
      .attr('y', 0)
      .attr('x', 9)
      .style('text-anchor', 'middle')
      .selectAll('text') // Altering label to make them oblique
        .attr('y', 0)
        .attr('x', 9)
        .attr('dy', '.35em')
        .attr('transform', 'rotate(55)')
        .style('text-anchor', 'start');
    // Add the Y axis
    if (type === 'size') {
      this._svg.append('g')
        .call(d3.axisLeft(this._y) // Call for y axis
        .tickFormat(d => { return Utils.convertBytes(d); })); // We convert bytes on each tick value
      return; // return now to not add again the axis with wrong tick formatting
    }
    // Default Y axis addition
    this._svg.append('g')
      .call(d3.axisLeft(this._y));
  }


  // Set the graph title
  static setTitle() {
    this._svg.append('text')
      .attr('x', (this._styles.width / 2))
      .attr('y', 0)
      .attr('text-anchor', 'middle')
      .style('font-size', '1.66rem')
      .text(this._title);
  }


  /* Graph internal elements factory */


  // Create a smoothed line (using d3 interpolation)
  static createLine(xVal, yVal) {
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
       .style('fill', color)
       .attr('d', area);
  }


  static getSvg() {
    return this._svg;
  }


}


export default GraphUtils;
