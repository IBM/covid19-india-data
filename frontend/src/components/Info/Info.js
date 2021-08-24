import React from 'react';
import { processName } from '../BasicElement';
import {
  ClickableTile,
  DataTable,
  TableContainer,
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableHeader,
  TableCell,
} from 'carbon-components-react';

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

async function fetchData(URL, short_name, filter_data, sampling_rate, date) {
  var response = await fetch(
    data_server + '/' + URL,
    (requestOptions = {
      ...requestOptions,
      body: JSON.stringify({
        state_short_name: short_name,
        filter_data: filter_data,
        scale_down: sampling_rate,
        date: date,
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
      href={props.props.link}
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

class DataTableElement extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: props.props,
      headers: [],
      rows: [],
    };
  }

  componentDidMount = () => {
    var current_data = this.state.data;
    var headers = [];
    var rows = [];

    if (!current_data.data[0]) {
      headers = [{ header: 'No data for this date', key: 'date' }];
    } else {
      headers = [
        { header: 'Date', key: 'date' },
        { header: current_data.data[0][0], key: 'value' },
      ];

      current_data.columns.forEach(function(e, i) {
        if (e !== 'date') {
          rows.push({
            id: i.toString(),
            date: processName(e),
            value: current_data.data[0][i],
          });
        }
      });
    }

    this.setState({
      ...this.state,
      headers: headers,
      rows: rows,
    });
  };

  render() {
    return (
      <div>
        <DataTable rows={this.state.rows} headers={this.state.headers}>
          {({ rows, headers, getHeaderProps, getTableProps }) => (
            <TableContainer title={processName(this.state.data.title)}>
              <Table {...getTableProps()} size="short">
                <TableHead>
                  <TableRow>
                    {headers.map(header => (
                      <TableHeader {...getHeaderProps({ header })}>
                        {header.header}
                      </TableHeader>
                    ))}
                  </TableRow>
                </TableHead>
                <TableBody>
                  {rows.map(row => (
                    <TableRow key={row.id}>
                      {row.cells.map(cell => (
                        <TableCell key={cell.id}>{cell.value}</TableCell>
                      ))}
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </DataTable>
        <br />
        <br />
      </div>
    );
  }
}

export {
  prepareData,
  prepareOptions,
  fetchData,
  generateStateID,
  Contributing,
  Resource,
  DataTableElement,
};
