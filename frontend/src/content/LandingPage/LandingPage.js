import React from 'react';
import { Download16 } from '@carbon/icons-react';
import { fetchData } from '../../components/Info';
import {
  Link,
  Button,
  DataTable,
  Table,
  TableHead,
  TableRow,
  TableHeader,
  TableBody,
  TableCell,
} from 'carbon-components-react';

class LandingPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      last_updated: null,
      dashboard_data: {},
    };
  }

  componentDidMount(props) {
    fetchData({ URL: 'fetch_dashboard_data' }).then(data => {
      this.setState({
        ...this.state,
        dashboard_data: this.prepareData(data),
      });
    });

    fetchData({ URL: 'last_updated' }).then(data => {
      this.setState({
        ...this.state,
        last_updated: data['last_updated'],
      });
    });
  }

  prepareData = e => {
    const rowData = [];
    const headerData = e.columns.map((elem, i) => {
      return {
        header: elem,
        key: elem,
      };
    });

    e.data.forEach(function(item, idx) {
      var new_row_data = { id: idx.toString() };
      item.data.forEach(function(data_item, data_idx) {
        var key = e.columns[data_idx];

        if (key === 'Bulletin')
          data_item = (
            <Link href={data_item} target="_blank">
              Link
            </Link>
          );

        new_row_data[key] = data_item;
      });

      rowData.push(new_row_data);
    });

    return {
      headerData: headerData,
      rowData: rowData,
    };
  };

  render() {
    return (
      <div
        className="bx--grid bx--grid--full-width bx--container"
        style={{
          width: '100%',
          minHeight: '100vh',
        }}>
        <div className="bx--row">
          <div className="bx--col-lg-10 state-header">
            <h1 className="title">
              COVID-19 Data <br />
              from <span className="text-blue">India</span>
            </h1>
            <br />
            <span className="text-blue">
              &nbsp;&nbsp;<em>Last Updated: {this.state.last_updated}</em>
            </span>

            {Object.keys(this.state.dashboard_data).length > 0 && (
              <>
                <DataTable
                  rows={this.state.dashboard_data.rowData}
                  headers={this.state.dashboard_data.headerData}
                  isSortable>
                  {({ rows, headers, getHeaderProps, getTableProps }) => (
                    <Table
                      {...getTableProps()}
                      size="short"
                      style={{ marginTop: '35px' }}>
                      <TableHead>
                        <TableRow>
                          {headers.map(header => (
                            <TableHeader
                              key={header.key}
                              {...getHeaderProps({ header })}>
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
                  )}
                </DataTable>
                <br />
                <span style={{ color: 'gray' }}>
                  Scroll right to see more data. &#x1f449;
                </span>
              </>
            )}
          </div>

          <div className="bx--col-lg-6">
            <p>
              Availability of COVID-19 data is crucial for researchers and
              policy makers to understand the progression of the pandemic and
              react to it in real time.{' '}
              <Link
                href="https://www.sciencemag.org/news/2021/05/there-are-so-many-hurdles-indian-scientists-plead-government-unlock-covid-19-data"
                target="_blank">
                Here is recent plea
              </Link>{' '}
              from researchers in India for they urgent access to COVID data
              collected by government agencies. Individual states and cities in
              India provide detailed information in their daily media bulletins
              about the current situation of COVID-19 in their respective
              locations. However, such data (usually in the form of PDF
              documents) is not readily accessible in structured form. While
              there are fantastic{' '}
              <Link href="https://www.covid19india.org/" target="_blank">
                crowd-sourced efforts
              </Link>{' '}
              underway to curate such data, manual approaches cannot scale to
              the volume of the data produced over the long term. Unfortunately,
              although this project originally began anticipating this outcome,
              this eventuality has already{' '}
              <Link
                href="https://blog.covid19india.org/2021/08/07/end/"
                target="_blank">
                come to pass
              </Link>
              .
              <br />
              <br />
              In this project, we use AI-assisted document and image extraction
              techniques to automate the extraction of such data in structured
              (SQL) form from the state-level daily health bulletins; and aim to
              make this data readily (and freely) available for further research
              and analysis. The target is to automate the data extraction and
              curation for each Indian state, so that once the extraction
              process of each state is complete, we can be on "autopilot" for
              that state, requiring little to none continued manual curation
              (other than to respond to changes in schema).
              <br />
              <br />
              Contributions are most welcome!
              <br />
              <br />
            </p>

            <Link href="/#/contributing" className="button-generic">
              <Button size="field">
                Contribute &nbsp; <Download16 />
              </Button>
            </Link>
            <Link
              href="https://arxiv.org/abs/2110.02311"
              target="_blank"
              className="button-generic">
              <Button size="field" kind="secondary">
                Read
              </Button>
            </Link>
          </div>
        </div>
      </div>
    );
  }
}

export default LandingPage;
