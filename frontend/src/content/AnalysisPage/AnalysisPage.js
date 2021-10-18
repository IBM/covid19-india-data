import React from 'react';
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
        <HighlightsElement props={QUERIES} />
      </>
    );
  }
}

export default AnalysisPage;
