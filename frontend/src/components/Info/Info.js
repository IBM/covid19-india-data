import React from 'react';
import { ClickableTile } from 'carbon-components-react';

let config = require('../../config.json');
let data_server = config['metadata']['data_server'];

var requestOptions = {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
};

const axis_plot_options = {
  title: null,
  axes: {
    bottom: {
      title: 'Date',
      mapsTo: 'date',
      scaleType: 'time',
    },
    left: {
      mapsTo: 'value',
      title: null,
      scaleType: 'linear',
    },
  },
  curve: 'curveMonotoneX',
  height: '400px',
  width: '80vw',
};

function prepareData(data, legend, key) {
  var new_data = [];

  data.forEach(function(item, id) {
    var new_item = {
      group: legend,
      date: item[0],
      value: item[key],
    };

    new_data.push(new_item);
  });

  return new_data;
}

function prepareOptions(title, key) {
  var new_options = {
    ...axis_plot_options,
    title: title + ' | ' + key,
    axes: {
      ...axis_plot_options.axes,
      left: {
        ...axis_plot_options.axes.left,
        title: key,
      },
    },
  };

  return new_options;
}

async function fetchData(URL, short_name, filter_data, sampling_rate) {
  var response = await fetch(
    data_server + '/' + URL,
    (requestOptions = {
      ...requestOptions,
      body: JSON.stringify({
        state_short_name: short_name,
        filter_data: filter_data,
        scale_down: sampling_rate,
      }),
    })
  );
  return response.json();
}

const generateStateID = stateName => {
  return stateName.replaceAll(' ', '');
};

const Contributing = props => (
  <div className="bx--col-lg-4">
    <ClickableTile
      className="contributing-card-inner"
      href={props.props.title}
      target="_blank">
      <div style={{ padding: '10px' }}>
        <p style={{ fontSize: 'inherit' }}> {props.props.title} </p>
      </div>
      <div className="contributing-card">{props.props.icon}</div>
    </ClickableTile>
  </div>
);

const Resource = props => (
  <div className="bx--col-lg-8">
    <ClickableTile
      className="resource-card-inner"
      href={props.props.link}
      target="_blank">
      <div style={{ padding: '10px' }}>
        <p style={{ fontSize: 'inherit' }}> {props.props.name} </p>
      </div>
    </ClickableTile>
  </div>
);

export {
  prepareData,
  prepareOptions,
  fetchData,
  generateStateID,
  Contributing,
  Resource,
};
