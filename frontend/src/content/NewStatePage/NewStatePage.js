import React from 'react';
import { BasicElement } from '../../components/BasicElement';

let config = require('../../config.json');
let state_config = config['states'][ENTER_STATE_KEY_HERE];

class NewStatePage extends React.Component {
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
      </>
    );
  }
}

export default NewStatePage;
