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

let default_contributors = ['stevemar', 'ImgBotApp'];

let citation_text = `@inproceedings{agarwal2021covid,
  title={COVID-19 India Dataset: Parsing Detailed COVID-19 Data
         in Daily Health Bulletins from States in India},
  author={Mayank Agarwal and Tathagata Chakraborti and Sachin Grover 
          and Arunima Chaudhary},
  booktitle={NeurIPS 2021 Workshop on Machine Learning in Public Health},
  year={2021}
}`;

async function fetchRepoData() {
  var response = await fetch(
    'https://api.github.com/repos/IBM/covid19-india-data/contributors'
  );
  return response.json();
}

function filterContributors(contributorsList) {
  var new_contributors_list = [];

  Array.from(contributorsList).forEach(function(item, index) {
    if (default_contributors.indexOf(item.login) < 0)
      new_contributors_list.push(item);
  });

  return new_contributors_list;
}

const Contributor = props => (
  <div
    className="bx--col-sm-1 bx--col-md-2 bx--col-lg-2"
    style={{ padding: '10px' }}>
    <Link href={props.props.html_url} target="_blank">
      <img
        alt="Contributor Info"
        src={props.props.avatar_url}
        className="contributors"
      />
    </Link>
  </div>
);

class ContributingPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      contributors: [],
    };
  }

  componentDidMount(props) {
    fetchRepoData().then(data => {
      this.setState({
        ...this.state,
        contributors: filterContributors(data),
      });
    });
  }

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

          <div className="bx--row">
            <div className="bx--col-lg-8">
              <h3>Read the Paper</h3>
              <hr />
              <br />

              <p>
                If you are using this data in your reserach, please remember to
                cite us. &#128591;{' '}
                <strong>
                  Note that the list of authors will continue to grow over time
                  with our OSS contributors.
                </strong>{' '}
                Please make sure to update the citation text in your future
                papers accordingly.
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
            </div>

            <div className="bx--col-lg-8">
              <h3>
                Top Contributors{' '}
                <span style={{ fontSize: 'large', fontWeight: '100' }}>
                  <Link
                    href={config['metadata']['link_to_code']}
                    target="_blank">
                    See all
                  </Link>
                </span>
              </h3>
              <hr />
              <br />

              <div className="bx--row">
                {this.state.contributors.map((item, index) => {
                  return <Contributor props={item} />;
                })}
              </div>
            </div>
          </div>

          <br />
          <br />
          <br />
          <br />
          <br />

          <h3 id="resources">Additional Resources</h3>
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
