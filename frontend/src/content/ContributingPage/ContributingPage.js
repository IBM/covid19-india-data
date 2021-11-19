import React from 'react';
import { Contributing, Resource } from '../../components/Info';
import { LogoGithub32, LogoSlack32, Sql32, Api_132 } from '@carbon/icons-react';
import { Tag, Link, Button, CodeSnippet } from 'carbon-components-react';

let config = require('../../config.json');
let resource_list = [
  {
    name: 'COVID 19 India',
    children: [
      {
        name: <>OG &#128583;</>,
        link: 'https://www.covid19india.org/',
      },
      {
        name: 'IIT-Hyderabad',
        link: 'https://covid19tracker.in',
      },
      {
        name: 'ITT-Madras',
        link: 'https://www.incovid19.org/',
      },
      {
        name: 'DataKind',
        link: 'https://github.com/DataKind-BLR',
      },
    ],
  },
  {
    name: 'COVID Today',
    link: 'https://covidtoday.in/',
  },
  {
    name: "IBM's response to COVID-19",
    link: 'https://www.ibm.com/impact/covid-19',
  },
  {
    name: 'COVID-19 Data Repository from Johns Hopkins University',
    link: 'https://github.com/CSSEGISandData/COVID-19',
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
  {
    name: 'Our World in Data',
    link: 'https://ourworldindata.org',
  },
  {
    name: 'Kaggle Challenges',
    children: [
      {
        name: 'Report',
        link: 'https://www.kaggle.com/imdevskp/corona-virus-report',
      },
      {
        name: 'Uncover',
        link: 'https://www.kaggle.com/roche-data-science-coalition/uncover',
      },
    ],
  },
];

let citation_text = `@article{agarwal2021covid,
  title={COVID-19 India Dataset: Parsing Detailed COVID-19 Data
         in Daily Health Bulletins from States in India},
  author={Agarwal, Mayank and Chakraborti, Tathagata and Grover, Sachin},
  journal={arXiv:2110.02311},
  year={2021}
}`;

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
                title: 'Join our Community on Slack',
                link: config['metadata']['link_to_slack'],
              }}
            />
            <Contributing
              props={{
                icon: <Sql32 />,
                title: (
                  <>
                    Download the Data{' '}
                    <Tag type="green" className="compressed-tag flattened-tag">
                      free
                    </Tag>
                  </>
                ),
                link: config['metadata']['link_to_data'],
              }}
            />
            <Contributing
              props={{
                icon: <Api_132 />,
                title: 'Connect with the API',
                link: '/#/data',
                internal: true,
              }}
            />
          </div>

          <br />
          <br />
          <br />

          <h3>Read the Paper</h3>
          <hr />
          <br />

          <p className="bx--col-lg-8">
            If you are using this data in your reserach, please remember to cite
            us. &#128591;{' '}
            <strong>
              Note that the list of authors will continue to grow over time with
              our OSS contributors.
            </strong>{' '}
            Please make sure to update the citation text in your future papers
            accordingly.
          </p>
          <br />

          <CodeSnippet type="multi">{citation_text}</CodeSnippet>

          <br />

          <Link
            href="https://arxiv.org/abs/2110.02311"
            target="_blank"
            className="button-generic">
            <Button size="field" kind="secondary">
              Read
            </Button>
          </Link>

          <br />
          <br />
          <br />
          <br />
          <br />

          <h3>Additional Resources</h3>
          <hr />
          <br />

          <div className="bx--row" style={{ marginBottom: '100px' }}>
            <div className="bx--col-lg-8">
              {resource_list.map((item, key) => {
                return (
                  <>
                    {key <= resource_list.length / 2 && (
                      <Resource key={key} props={item} />
                    )}
                  </>
                );
              })}
            </div>
            <div className="bx--col-lg-8">
              {resource_list.map((item, key) => {
                return (
                  <>
                    {key > resource_list.length / 2 && (
                      <Resource key={key} props={item} />
                    )}
                  </>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default ContributingPage;
