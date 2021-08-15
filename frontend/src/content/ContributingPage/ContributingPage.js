import React from 'react';
import { Contributing, Resource } from '../../components/Info';
import { LogoGithub32, LogoSlack32, Sql32 } from '@carbon/icons-react';

let config = require('../../config.json');
console.log(config['metadata']['link_to_code']);
let resource_list = [
  {
    name: 'COVID 19 India',
    link: 'https://www.covid19india.org/',
  },
  {
    name: "IBM's response to COVID-19",
    link: 'https://www.ibm.com/impact/covid-19',
  },
  {
    name: 'Our World in Data',
    link: 'https://ourworldindata.org/',
  },
  {
    name: 'DDL COVID India',
    link: 'http://www.devdatalab.org/covid',
  },
  {
    name: 'WNTRAC: Worldwide Non-pharmaceutical Interventions Tracker',
    link: 'https://ibm.github.io/wntrac/',
  },
  {
    name: 'India COVID SOS',
    link: 'https://www.indiacovidsos.org/',
  },
  {
    name: 'AI Against COVID EXPO @ NeurIPS 2020',
    link: 'https://nips.cc/Conferences/2020/ScheduleMultitrack?event=21301',
  },
];

class ContributingPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  componentDidMount(props) {}

  render() {
    return (
      <div
        className="bx--grid bx--grid--full-width bx--container"
        style={{
          width: '100%',
          minHeight: '100vh',
        }}>
        <div className="bx--col-lg-16">
          <h3>Contributing</h3>
          <hr />
          <br />
          <div className="bx--row">
            <Contributing
              props={{
                icon: <LogoGithub32 />,
                title: 'GitHub',
                link: config['metadata']['link_to_code'],
              }}
            />
            <Contributing
              props={{
                icon: <LogoSlack32 />,
                title: 'Community',
                link: config['metadata']['link_to_slack'],
              }}
            />
            <Contributing
              props={{
                icon: <Sql32 />,
                title: 'Data',
                link: config['metadata']['link_to_data'],
              }}
            />
          </div>

          <br />
          <br />
          <br />

          <h3>Additional Resources</h3>
          <hr />
          <br />

          <div className="bx--row">
            {resource_list.map(function(item, key) {
              return (
                <Resource
                  key={key}
                  props={{ link: item.link, name: item.name }}
                />
              );
            })}
          </div>
        </div>
      </div>
    );
  }
}

export default ContributingPage;
