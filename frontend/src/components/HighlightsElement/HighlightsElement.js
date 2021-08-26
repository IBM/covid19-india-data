import React from 'react';
import '@carbon/charts/styles.css';
import { LineChart } from '@carbon/charts-react';
import { Accordion, AccordionItem } from 'carbon-components-react';
import { prepareData, prepareOptions, fetchData } from '../Info';

class HighlightsElement extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      query_data: {},
      query: props.props,
    };
  }

  componentDidMount = () => {
    let query_data = {};
    var promises = [];

    this.state.query.forEach(function(q, index) {
      var promise = fetchData({ URL: 'query', query: q.query }).then(data => {
        query_data[index] = data['data'];
      });

      promises.push(promise);
    });

    Promise.all(promises).then(() => {
      this.setState({
        ...this.state,
        query_data: query_data,
      });
    });
  };

  render() {
    return (
      <div
        className="bx--grid bx--grid--full-width bx--container"
        style={{ width: '100%' }}>
        <div className="bx--col-lg-16">
          {Object.keys(this.state.query_data).length > 0 && (
            <div>
              <h3>Highlights</h3>
              <br />

              <Accordion align="start">
                {this.state.query.map((q, i) => {
                  var data = this.state.query_data[i];
                  return (
                    <AccordionItem
                      title={<strong>{q.subject}</strong>}
                      key={i}
                      open>
                      <p>{q.description}</p>

                      <br />
                      <br />
                      {data && (
                        <LineChart
                          key={i}
                          data={prepareData(data, q.subject, 1)}
                          options={prepareOptions(
                            data[0][0],
                            data[data.length - 1][0]
                          )}></LineChart>
                      )}
                    </AccordionItem>
                  );
                })}
              </Accordion>
            </div>
          )}
        </div>
      </div>
    );
  }
}

export { HighlightsElement };
