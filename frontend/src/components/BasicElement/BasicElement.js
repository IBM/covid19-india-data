import React from 'react';
import '@carbon/charts/styles.css';
import { LineChart } from '@carbon/charts-react';
import {
  prepareData,
  prepareOptions,
  fetchData,
  DataTableElement,
} from '../Info';
import {
  Tag,
  Button,
  MultiSelect,
  Loading,
  NumberInput,
  Link,
  Tabs,
  Tab,
  DatePicker,
  DatePickerInput,
  CodeSnippet,
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

function formatDate(date) {
  return (
    date.getUTCFullYear() +
    '/' +
    (date.getUTCMonth() + 1) +
    '/' +
    date.getUTCDate()
  );
}

class BasicElement extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      name: props.props.name,
      short_name: props.props.short_name,
      link_to_db_schema: props.props.link_to_db_schema,
      data: [],
      dataOnDate: [],
      linkToDailyBulletin: null,
      schema: [],
      status_flags: {
        is_complete: props.props.is_complete,
        date: null,
        date_picker_invalid: false,
        date_picker_status: null,
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
    fetchData({ URL: 'fetch_schema', short_name: this.state.short_name }).then(
      data => {
        this.setState({
          ...this.state,
          schema: data['data'],
        });
      }
    );
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

    fetchData({
      URL: 'fetch_data',
      short_name: this.state.short_name,
      sampling_rate: this.state.status_flags.sampling_rate,
    }).then(data => {
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

  logDateSelection = e => {
    let selected_date = new Date(e);
    let formatted_date_string = formatDate(selected_date);

    this.setState({
      ...this.state,
      status_flags: {
        ...this.state.status_flags,
        date: formatted_date_string,
        date_picker_invalid: false,
        date_picker_status: null,
      },
    });
  };

  fetchDataOnDate = () => {
    if (!this.state.status_flags.date) {
      this.setState({
        ...this.state,
        status_flags: {
          ...this.state.status_flags,
          date_picker_invalid: true,
          date_picker_status: 'No date selected',
        },
      });
    } else {
      this.setState(
        {
          ...this.state,
          dataOnDate: [],
          linkToDailyBulletin: null,
        },
        () => {
          this.showTables();
        }
      );
    }
  };

  showTables = () => {
    fetchData({
      URL: 'fetch_days_data',
      short_name: this.state.short_name,
      date: this.state.status_flags.date,
    }).then(data => {
      this.setState({
        ...this.state,
        dataOnDate: data['data'],
        linkToDailyBulletin: data['bulletin_link'],
      });
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

    fetchData({
      URL: 'fetch_data',
      short_name: this.state.short_name,
      filter_data: selectedItems,
      sampling_rate: this.state.status_flags.sampling_rate,
    }).then(data => {
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
        style={{ width: '100%' }}>
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
                </div>

                <div className="bx--col-lg-8 state-header">
                  <h1>
                    {this.state.name}{' '}
                    <span style={{ fontSize: 'x-large' }}>data</span>
                  </h1>

                  <Tag type="green" className="flattened-tag">
                    {this.state.short_name}
                  </Tag>

                  {this.state.status_flags.is_complete && (
                    <Tag type="blue" className="flattened-tag">
                      {' '}
                      completed{' '}
                    </Tag>
                  )}

                  {!this.state.status_flags.is_complete && (
                    <Tag type="gray" className="flattened-tag">
                      {' '}
                      in progress{' '}
                    </Tag>
                  )}

                  <br />

                  <br />

                  <DatePicker
                    dateFormat="Y/m/d"
                    datePickerType="single"
                    value={this.state.status_flags.date}
                    onChange={this.logDateSelection.bind(this)}>
                    <DatePickerInput
                      id="date-picker-calendar-id"
                      placeholder="yyyy/mm/dd"
                      labelText="Date picker"
                      type="text"
                      invalid={this.state.status_flags.date_picker_invalid}
                      invalidText={this.state.status_flags.date_picker_status}
                      size="sm"
                    />
                  </DatePicker>

                  <br />
                  <Button
                    kind="secondary"
                    size="sm"
                    onClick={this.fetchDataOnDate.bind(this)}>
                    Fetch Data
                  </Button>

                  {this.state.linkToDailyBulletin && (
                    <Link href={this.state.linkToDailyBulletin} target="_blank">
                      <Button kind="primary" size="sm">
                        View Bulletin
                      </Button>
                    </Link>
                  )}
                </div>
              </div>

              <br />
              <br />

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
                                data={prepareData(item.data, [e], [i])}
                                options={prepareOptions(
                                  item.title,
                                  e,
                                  item.title
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

              {this.state.dataOnDate.map(function(item, key) {
                return <DataTableElement key={key} props={item} />;
              })}
            </Tab>
            <Tab label="View Schema">
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
            <Tab label="View API">
              <div className="some-content">
                {this.state.schema.map((item, id) => {
                  const table_link =
                    config['metadata']['data_server'] +
                    '/get_data?state=' +
                    this.state.short_name +
                    '&table=' +
                    item.title;

                  return (
                    <>
                      <CodeSnippet
                        type="single"
                        style={{ marginBottom: '10px', maxWidth: '100%' }}>
                        GET &nbsp;
                        <Link href={table_link} target="_blank">
                          {table_link}
                        </Link>
                      </CodeSnippet>

                      {item.columns.map((c, i) => {
                        const column_link = table_link + '&column=' + c;

                        if (c !== 'date')
                          return (
                            <CodeSnippet
                              type="single"
                              style={{
                                marginBottom: '10px',
                                maxWidth: '100%',
                              }}>
                              GET &nbsp;
                              <Link href={column_link} target="_blank">
                                {column_link}
                              </Link>
                            </CodeSnippet>
                          );
                        return null;
                      })}
                    </>
                  );
                })}
              </div>
            </Tab>
          </Tabs>
        </div>
      </div>
    );
  }
}

export { BasicElement, processName };
