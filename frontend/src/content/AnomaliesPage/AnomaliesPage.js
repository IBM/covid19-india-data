import React from 'react';
import { Link, ToastNotification } from 'carbon-components-react';
import { HighlightsElement } from '../../components/HighlightsElement';
import { QUERIES } from './query.js';

let config = require('../../config.json');

class AnomaliesPage extends React.Component {
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
                  Find out for yourself! Any time we find inconsistencies in the
                  state bulletins, we will log it in this page. If you find new
                  ones please get in touch.
                </span>
              }
              title="Is the data reliable? You ask."
            />
          </div>
        </div>

        <HighlightsElement props={QUERIES} />
      </>
    );
  }
}

export default AnomaliesPage;
