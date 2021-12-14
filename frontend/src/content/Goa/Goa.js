import React from 'react';
import { BasicElement } from '../../components/BasicElement';
import { HighlightsElement } from '../../components/HighlightsElement';
import { QUERIES } from './query.js';

let config = require('../../config.json');
let state_config = config['states']['GA'];

class Goa extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      ...state_config,
    };
  }

  render() {
    return (
      <>
        <BasicElement props={this.state} />
        <HighlightsElement props={QUERIES} />
      </>
    );
  }
}

export default Goa;
