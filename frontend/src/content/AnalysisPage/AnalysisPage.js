import React from 'react';
import { Link, ToastNotification } from 'carbon-components-react';
import { HighlightsElement } from '../../components/HighlightsElement';
import { QUERIES } from './query.js';

let config = require('../../config.json');

class AnalysisPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      ...config,
    };
  }

  render() {
    return (
      <>
        <div
          className="bx--grid bx--grid--full-width bx--container"
          style={{ width: '100%' }}>
          <div className="bx--col-lg-16">
            <ToastNotification
              kind="info"
              hideCloseButton
              lowContrast
              caption={
                <Link href={config['metadata']['link_to_code']} target="_blank">
                  GitHub
                </Link>
              }
              subtitle={
                <span>
                  If you would like to add your own analysis, please open an
                  issue with the description and we will help you get added.
                </span>
              }
              title="Adding your own insights"
            />
          </div>
        </div>
        <br />
        <br />

        <HighlightsElement props={QUERIES} />
      </>
    );
  }
}

export default AnalysisPage;
