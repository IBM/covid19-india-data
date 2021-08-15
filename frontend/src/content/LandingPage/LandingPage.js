import React from 'react';
import { Link, Button } from 'carbon-components-react';

class LandingPage extends React.Component {
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
          backgroundImage: `url(${process.env.PUBLIC_URL}/images/cover.png)`,
          backgroundPosition: 'right',
          backgroundRepeat: 'no-repeat',
          backgroundSize: 'cover',
        }}>
        <div className="bx--col-lg-12">
          <h1 className="title">
            COVID-19 Data <br />
            from <span className="text-blue">India</span>
          </h1>
          <hr />
          <br />
          <p>
            Availability of COVID-19 data is crucial for researchers and policy
            makers to understand the progression of the pandemic and react to it
            in real time.{' '}
            <Link
              href="https://www.sciencemag.org/news/2021/05/there-are-so-many-hurdles-indian-scientists-plead-government-unlock-covid-19-data"
              target="_blank">
              Here is recent plea
            </Link>{' '}
            from researchers in India for they urgent access to COVID data
            collected by government agencies. Individual states and cities in
            India provide detailed information in their daily media bulletins
            about the current situation of COVID-19 in their respective
            locations. However, such data (usually in the form of PDF documents)
            is not readily accessible in structured form.
            <br />
            <br />
            While there are fantastic{' '}
            <Link href="https://www.covid19india.org/" target="_blank">
              crowd-sourced efforts
            </Link>{' '}
            underway to curate such data, manual approaches cannot scale to the
            volume of the data produced over the long term. Unfortunately,
            although this project originally began anticipating this outcome,
            this eventuality has already{' '}
            <Link
              href="https://blog.covid19india.org/2021/08/07/end/"
              target="_blank">
              come to pass
            </Link>
            .
            <br />
            <br />
            In this project, we use AI-assisted document and image extraction
            techniques to automate the extraction of such data in structured
            (SQL) form from the state-level daily health bulletins; and aim to
            make this data readily (and freely) available for further research
            and analysis. The target is to automate the data extraction and
            curation for each Indian state, so that once the extraction process
            of each state is complete, we can be on "autopilot" for that state,
            requiring little to none continued manual curation (other than to
            respond to changes in schema).
            <br />
            <br />
            Contributions are most welcome!
            <br />
            <br />
          </p>

          <Link href="/#/contributing">
            <Button size="field">Contribute</Button>
          </Link>
        </div>
      </div>
    );
  }
}

export default LandingPage;
