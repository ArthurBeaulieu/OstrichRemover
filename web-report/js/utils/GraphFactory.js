import GraphUtils from './GraphUtils.js';


const LineColors = {
  blue: 'rgb(45, 145, 150)',
  green: 'rgb(55, 195, 64)',
  orange: 'rgb(255, 173, 103)',
  red: 'rgb(227, 117, 23)'
};

const DotColors = {
  blue: 'rgba(72, 171, 175, .8)',
  green: 'rgba(86, 212, 91, .8)',
  orange: 'rgba(255, 173, 103, .8)',
  red: 'rgba(255, 107, 103, .8)'
};

const AreaColors = {
  blue: 'rgb(194, 225, 231)',
  green: 'rgb(199, 237, 205)',
  orange: 'rgb(250, 225, 209)',
  red: 'rgb(250, 205, 209)'
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

    GraphUtils.makeActive();
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
    // Define and append areas to the graph
    if (options.area === true) {
      GraphUtils.appendArea(GraphUtils.createArea('date', 'files'), AreaColors.blue);
      GraphUtils.appendArea(GraphUtils.createArea('date', 'audio'), AreaColors.orange);
      GraphUtils.appendArea(GraphUtils.createArea('date', 'folders'), AreaColors.green);
      GraphUtils.appendArea(GraphUtils.createArea('date', 'images'), AreaColors.red);
    }
    // Define and append lines to the graph
    GraphUtils.appendLine(GraphUtils.createLine('date', 'files', DotColors.blue), LineColors.blue);
    GraphUtils.appendLine(GraphUtils.createLine('date', 'audio', DotColors.orange), LineColors.orange);
    GraphUtils.appendLine(GraphUtils.createLine('date', 'folders', DotColors.green), LineColors.green);
    GraphUtils.appendLine(GraphUtils.createLine('date', 'images', DotColors.red), LineColors.red);
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
    // Define and append areas to the graph if requested
    if (options.area === true) {
      GraphUtils.appendArea(GraphUtils.createArea('date', 'totalTracks'), AreaColors.blue);
      GraphUtils.appendArea(GraphUtils.createArea('date', 'totalFlac'), AreaColors.green);
      GraphUtils.appendArea(GraphUtils.createArea('date', 'totalMp3'), AreaColors.orange);
    }
    // Define and append lines to the graph
    GraphUtils.appendLine(GraphUtils.createLine('date', 'totalTracks', DotColors.blue), LineColors.blue);
    GraphUtils.appendLine(GraphUtils.createLine('date', 'totalFlac', DotColors.green), LineColors.green);
    GraphUtils.appendLine(GraphUtils.createLine('date', 'totalMp3', DotColors.orange), LineColors.orange);
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
    // Define and append areas to the graph if requested
    if (options.area === true) {
      GraphUtils.appendArea(GraphUtils.createArea('date', 'possibleErrors'), AreaColors.blue);
      GraphUtils.appendArea(GraphUtils.createArea('date', 'errorsCount'), AreaColors.red);
    }
    // Define and append lines to the graph
    GraphUtils.appendLine(GraphUtils.createLine('date', 'possibleErrors', DotColors.blue), LineColors.blue);
    GraphUtils.appendLine(GraphUtils.createLine('date', 'errorsCount', DotColors.red), LineColors.red);
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
    // Define and append areas to the graph if requested
    if (options.area === true) {
      GraphUtils.appendArea(GraphUtils.createArea('date', 'size'), AreaColors.blue);
    }
    // Define and append lines to the graph
    GraphUtils.appendLine(GraphUtils.createLine('date', 'size', DotColors.blue), LineColors.blue);
  }


}


export default GraphFactory;
