import React from 'react';

let config = require('../../config.json');

class AnalysisPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      ...config,
    };
  }

  render() {
    return <></>;
  }
}

export default AnalysisPage;
