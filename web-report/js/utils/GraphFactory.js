import GraphUtils from './GraphUtils.js';


const LineColors = {
  blue: 'rgb(45, 145, 150)',
  green: 'rgb(55, 195, 64)',
  orange: 'rgb(255, 173, 103)',
  red: 'rgb(227, 117, 23)'
};

const AreaColors = {
  blue: 'rgba(72, 171, 175, .3)',
  green: 'rgba(86, 212, 91, .3)',
  orange: 'rgba(255, 173, 103, .3)',
  red: 'rgba(255, 107, 103, .3)'
};


class GraphFactory {


  constructor(options) {
    if (options.type === 'files') {
      this._buildFiles(options);
    } else if (options.type === 'audio') {
      this._buildAudio(options);
    } else if (options.type === 'quality') {
      this._buildQuality(options);
    } else if (options.type === 'size') {
      this._buildSize(options);
    } else {
      return;
    }

    GraphUtils.setLegend();
    return GraphUtils.getSvg();
  }


  // Build file graph
  _buildFiles(options) {
    GraphUtils.createGraph({
      parent: options.parent,
      data: options.data,
      xAxis: 'date',
      yAxis: 'files',
      title: 'Files evolution over time'
    });
    // Define and append lines to the graph
    GraphUtils.appendLine(GraphUtils.createLine('date', 'files'), LineColors.blue);
    GraphUtils.appendLine(GraphUtils.createLine('date', 'folders'), LineColors.green);
    GraphUtils.appendLine(GraphUtils.createLine('date', 'audio'), LineColors.orange);
    GraphUtils.appendLine(GraphUtils.createLine('date', 'images'), LineColors.red);
    // Define and append areas to the graph
    if (options.area === true) {
      GraphUtils.appendArea(GraphUtils.createArea('date', 'files'), AreaColors.blue);
      GraphUtils.appendArea(GraphUtils.createArea('date', 'folders'), AreaColors.green);
      GraphUtils.appendArea(GraphUtils.createArea('date', 'audio'), AreaColors.orange);
      GraphUtils.appendArea(GraphUtils.createArea('date', 'images'), AreaColors.red);
    }
  }


  // Build audio graph
  _buildAudio(options) {
    GraphUtils.createGraph({
      parent: options.parent,
      data: options.data,
      xAxis: 'date',
      yAxis: 'totalTracks',
      title: 'Audio file evolution over time'
    });
    // Define and append lines to the graph
    GraphUtils.appendLine(GraphUtils.createLine('date', 'totalTracks'), LineColors.blue);
    GraphUtils.appendLine(GraphUtils.createLine('date', 'totalFlac'), LineColors.green);
    GraphUtils.appendLine(GraphUtils.createLine('date', 'totalMp3'), LineColors.orange);
    // Define and append areas to the graph if requested
    if (options.area === true) {
      GraphUtils.appendArea(GraphUtils.createArea('date', 'totalTracks'), AreaColors.blue);
      GraphUtils.appendArea(GraphUtils.createArea('date', 'totalFlac'), AreaColors.green);
      GraphUtils.appendArea(GraphUtils.createArea('date', 'totalMp3'), AreaColors.orange);
    }
  }


  // Build quality graph
  _buildQuality(options) {
    GraphUtils.createGraph({
      parent: options.parent,
      data: options.data,
      xAxis: 'date',
      yAxis: 'possibleErrors',
      title: 'Quality evolution over time'
    });
    // Define and append lines to the graph
    GraphUtils.appendLine(GraphUtils.createLine('date', 'possibleErrors'), LineColors.blue);
    GraphUtils.appendLine(GraphUtils.createLine('date', 'errorsCount'), LineColors.green);
    // Define and append areas to the graph if requested
    if (options.area === true) {
      GraphUtils.appendArea(GraphUtils.createArea('date', 'possibleErrors'), AreaColors.blue);
      GraphUtils.appendArea(GraphUtils.createArea('date', 'errorsCount'), AreaColors.green);
    }
  }


  // Build size graph
  _buildSize(options) {
    GraphUtils.createGraph({
      parent: options.parent,
      data: options.data,
      xAxis: 'date',
      yAxis: 'size',
      title: 'Size evolution over time'
    });
    // Define and append lines to the graph
    GraphUtils.appendLine(GraphUtils.createLine('date', 'size'), LineColors.blue);
    // Define and append areas to the graph if requested
    if (options.area === true) {
      GraphUtils.appendArea(GraphUtils.createArea('date', 'size'), AreaColors.blue);
    }
  }


}


export default GraphFactory;
