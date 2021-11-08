import React, { Component } from 'react';
import './app.scss';

import { Content } from 'carbon-components-react/lib/components/UIShell';
import { Route, Switch } from 'react-router-dom';
// import { generateStateID } from './components/Info';

import PageHeader from './components/PageHeader';
import LandingPage from './content/LandingPage';
import ContributingPage from './content/ContributingPage';
import DataAccessPage from './content/DataAccessPage';

import AnalysisPage from './content/AnalysisPage';
import AnomaliesPage from './content/AnomaliesPage';

import Delhi from './content/Delhi';
import WestBengal from './content/WestBengal';
import Telangana from './content/Telangana';
import Haryana from './content/Haryana';
import Maharashtra from './content/Maharashtra/Maharashtra';
import Karnataka from './content/Karnataka/Karnataka';
import Uttarakhand from './content/Uttarakhand';

// let config = require('./config.json');
// let states = config['states'];

// let loadEntries = entries =>
//   Promise.all(
//     Object.keys(states).map(entry => import(`./content/` + generateStateID(states[entry]["name"])))
//   );

// loadEntries(states);

class App extends Component {
  render() {
    return (
      <>
        <PageHeader />
        <Content>
          <Switch>
            <Route exact path="/" component={LandingPage} />
            <Route exact path="/introduction" component={LandingPage} />
            <Route exact path="/contributing" component={ContributingPage} />
            <Route exact path="/data" component={DataAccessPage} />

            <Route exact path="/analysis" component={AnalysisPage} />
            <Route exact path="/anomalies" component={AnomaliesPage} />

            <Route exact path="/Delhi" component={Delhi} />
            <Route exact path="/Haryana" component={Haryana} />
            <Route exact path="/Telangana" component={Telangana} />
            <Route exact path="/WestBengal" component={WestBengal} />
            <Route exact path="/Maharashtra" component={Maharashtra} />
            <Route exact path="/Karnataka" component={Karnataka} />
            <Route exact path="/Uttarakhand" component={Uttarakhand} />

            {/*
              {Object.keys(states).map((key, index) => (
                <Route
                  exact
                  key={index}
                  path={'/' + generateStateID(states[key]["name"])}
                  component={generateStateID(states[key]["name"])}
                />
              ))}
            */}
          </Switch>
        </Content>
      </>
    );
  }
}

export default App;
