import React from 'react';
import '@carbon/charts/styles.css';
import { LineChart } from '@carbon/charts-react';
import { prepareData, prepareOptions, fetchData } from '../Info';
import {
  Button,
  MultiSelect,
  Loading,
  NumberInput,
  Link,
  Tabs,
  Tab,
} from 'carbon-components-react';

let config = require('../../config.json');
let sampling_rate = config['config']['sampling_rate'];

const PrimaryLabel = 'Table Name';
const SecondaryLabel = 'Column Name';

function listOfTables(schema) {
  return schema.map(function(item, key) {
    return {
      id: item.title,
      text: processName(item.title),
    };
  });
}

function listOfColumns(schema, table_names = []) {
  var list_of_columns = [];

  schema.map(function(item, key) {
    if (table_names.includes(item.title))
      list_of_columns = list_of_columns.concat(item.columns.slice(1));

    return list_of_columns;
  });

  list_of_columns = list_of_columns.map(function(i, e) {
    return {
      id: i,
      text: processName(i),
    };
  });

  return list_of_columns;
}

function capitalizeFirstLetter(text) {
  return text[0].toUpperCase() + text.substring(1);
}

function processName(name) {
  return capitalizeFirstLetter(name).replaceAll('_', ' ');
}

class BasicElement extends React.Component {
  constructor(props) {
    console.log();
    super(props);
    this.state = {
      name: props.props.name,
      short_name: props.props.short_name,
      link_to_db_schema: props.props.link_to_db_schema,
      data: [],
      schema: [],
      status_flags: {
        fetched_data: true,
        fetching_data: false,
        tables_selected: [],
        columns_selected: [],
        columns_available: [],
        selectedKey: 0,
        sampling_rate: sampling_rate,
      },
    };
  }

  componentDidMount = () => {
    fetchData('fetch_schema', this.state.short_name, {}).then(data => {
      this.setState({
        ...this.state,
        schema: data['data'],
      });
    });
  };

  drawAll = () => {
    this.setState({
      ...this.state,
      status_flags: {
        ...this.state.status_flags,
        fetching_data: true,
        fetched_data: false,
        tables_selected: [],
      },
    });

    fetchData(
      'fetch_data',
      this.state.short_name,
      {},
      this.state.status_flags.sampling_rate
    ).then(data => {
      this.setState(
        {
          ...this.state,
          data: data['data'],
        },
        () => {
          this.resetRefresh();
        }
      );
    });
  };

  drawSelected = () => {
    this.setState({
      ...this.state,
      status_flags: {
        ...this.state.status_flags,
        fetching_data: true,
        fetched_data: false,
      },
    });

    var selectedItems = [];
    const tempState = this.state;
    const columns_selected_to_list = Object.entries(
      tempState.status_flags.columns_selected
    ).map((element, id) => element[1].id);

    tempState.schema.map(function(item, key) {
      if (tempState.status_flags.tables_selected.includes(item.title))
        selectedItems.push({
          title: item.title,
          columns: item.columns.filter(value =>
            columns_selected_to_list.includes(value)
          ),
        });

      return selectedItems;
    });

    fetchData(
      'fetch_data',
      this.state.short_name,
      selectedItems,
      this.state.status_flags.sampling_rate
    ).then(data => {
      console.log(data);
      this.setState(
        {
          ...this.state,
          data: data['data'],
        },
        () => {
          this.resetRefresh();
        }
      );
    });
  };

  resetRefresh = e => {
    this.setState({
      ...this.state,
      status_flags: {
        ...this.state.status_flags,
        fetching_data: false,
        fetched_data: true,
      },
    });
  };

  logTableSelection = e => {
    const selectedItems = Object.entries(e).map((element, id) => element[1].id);
    const columns_available = listOfColumns(this.state.schema, selectedItems);
    const columns_available_to_list = Object.entries(columns_available).map(
      (element, id) => element[1].id
    );
    const tempState = this.state;

    this.setState({
      ...this.state,
      status_flags: {
        ...this.state.status_flags,
        tables_selected: selectedItems,
        columns_available: columns_available,
        columns_selected: tempState.status_flags.columns_selected.filter(
          value => columns_available_to_list.includes(value.id)
        ),
        selectedKey: tempState.status_flags.selectedKey + 1,
      },
    });
  };

  logColumnSelection = e => {
    this.setState({
      ...this.state,
      status_flags: {
        ...this.state.status_flags,
        columns_selected: e,
      },
    });
  };

  handleInputChange = e => {
    this.setState({
      ...this.state,
      status_flags: {
        ...this.state.status_flags,
        sampling_rate: this.textInput.value,
      },
    });
  };

  render() {
    return (
      <div
        className="bx--grid bx--grid--full-width bx--container"
        style={{
          width: '100%',
          minHeight: '100vh',
        }}>
        <div className="bx--col-lg-16">
          <Tabs scrollIntoView={false}>
            <Tab label="Visualize">
              <div className="bx--row">
                <div className="bx--col-lg-8">
                  <p>
                    The data for visualization is being sampled at every{' '}
                    <span className="text-blue">
                      {this.state.status_flags.sampling_rate}
                    </span>{' '}
                    days to save you data. To access and analyze the full data,
                    click <Link href="/#/contributing">here</Link>.
                  </p>

                  <br />
                  <NumberInput
                    id="sampling_rate"
                    light
                    size="sm"
                    min={1}
                    value={this.state.status_flags.sampling_rate}
                    onChange={this.handleInputChange.bind(this)}
                    ref={input => {
                      this.textInput = input;
                    }}
                  />

                  <MultiSelect
                    id="table_name"
                    items={listOfTables(this.state.schema)}
                    itemToString={item => (item ? item.text : '')}
                    onChange={value => {
                      this.logTableSelection(value.selectedItems);
                    }}
                    label={PrimaryLabel}
                  />

                  <MultiSelect
                    id="column_name"
                    key={this.state.status_flags.selectedKey}
                    items={this.state.status_flags.columns_available}
                    initialSelectedItems={
                      this.state.status_flags.columns_selected
                    }
                    itemToString={item => (item ? item.text : '')}
                    onChange={value => {
                      this.logColumnSelection(value.selectedItems);
                    }}
                    label={SecondaryLabel}
                    disabled={
                      this.state.status_flags.tables_selected.length === 0
                    }
                  />

                  <br />

                  <Button
                    kind="primary"
                    disabled={
                      this.state.status_flags.tables_selected.length === 0
                    }
                    size="sm"
                    onClick={this.drawSelected.bind(this)}
                    style={{ marginRight: '10px' }}>
                    Draw Selected
                  </Button>
                  <Button
                    kind="secondary"
                    size="sm"
                    onClick={this.drawAll.bind(this)}>
                    Draw All
                  </Button>

                  <br />
                  <br />
                </div>

                <div className="bx--col-lg-8 state-header">
                  <h1>{this.state.name}</h1>
                </div>
              </div>

              {this.state.status_flags.fetching_data && (
                <>
                  <Loading description="Active loading indicator" withOverlay />
                </>
              )}

              {this.state.data.map(function(item, key) {
                return (
                  <div key={key}>
                    {item.columns.map(function(e, i) {
                      return (
                        <React.Fragment key={i}>
                          {e !== 'Date' && (
                            <>
                              <LineChart
                                key={i}
                                data={prepareData(item.data, e, i)}
                                options={prepareOptions(
                                  item.title,
                                  e
                                )}></LineChart>

                              <br />
                              <hr />
                              <br />
                            </>
                          )}
                        </React.Fragment>
                      );
                    })}
                  </div>
                );
              })}
            </Tab>
            <Tab label="View Data Schema">
              <div className="some-content">
                <img alt="" src={this.state.link_to_db_schema} width="100%" />
                <br />
                <br />
                <Link
                  href={config['metadata']['link_to_schemas']}
                  target="_blank">
                  <Button size="small" kind="secondary">
                    Details
                  </Button>
                </Link>
              </div>
            </Tab>
          </Tabs>
        </div>
      </div>
    );
  }
}

export { BasicElement };
