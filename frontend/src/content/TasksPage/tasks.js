import React from 'react';
import { Link } from 'carbon-components-react';

const references = {
  1: 'https://www.cdc.gov/mmwr/volumes/70/wr/mm7019e3.htm',
  2: 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7685335',
  3: 'https://dl.acm.org/doi/10.5555/3463952.3464047',
  4: 'https://pubmed.ncbi.nlm.nih.gov/33144763',
  5: 'https://europepmc.org/article/PPR/PPR276812',
  6: 'https://pubmed.ncbi.nlm.nih.gov/32995829',
  7: 'https://epubs.siam.org/doi/abs/10.1137/s0036144500371907',
  8: 'https://pubmed.ncbi.nlm.nih.gov/34173439',
  9: 'https://pubmed.ncbi.nlm.nih.gov/32607504',
};

const Reference = props => (
  <span style={{ whiteSpace: 'nowrap' }}>
    [
    <Link href={references[props.href]} target="_blank">
      {props.href}
    </Link>
    ]
  </span>
);

const TASKS = [
  {
    column: 0,
    title: 'OCR on Health Bulletins',
    description:
      'Classic PDF parsers fail when tablular and textual data are embedded as images inside the document. Help enrich the data by extending the automated data extraction pipeline with open-sourced OCR techniques to parse data inside images as well.',
    imageURL: 'cv',
    url:
      'https://github.com/IBM/covid19-india-data/wiki/Challenge-Tasks#-ocr-on-health-bulletins',
    difficulty: {
      level: 'Beginner',
      color: 'green',
    },
    topics: ['CV'],
    states: ['GA', 'KN', 'RJ'],
  },
  {
    column: 1,
    title: 'Translating Health Bulletins from Regional Languages',
    description:
      'Not all Indian states report their data in English. Help enrich the COVID-19 India data by creating translation models and parsers that work with Hindi and other regional languages, and extend the state of the art in "natural language" processing.',
    imageURL: 'translation',
    url:
      'https://github.com/IBM/covid19-india-data/wiki/Challenge-Tasks#-translating-health-bulletins',
    difficulty: {
      level: 'Advanced',
      color: 'red',
    },
    topics: ['NLP'],
    states: ['MP'],
  },
  {
    column: 0,
    title: 'Positional Entity Parser',
    description:
      'In this task, you are required to model a domain-dependent precision parser to extract patient and pandemic data from plain text information in health bulletins.',
    imageURL: 'parse',
    url:
      'https://github.com/IBM/covid19-india-data/wiki/Challenge-Tasks#-positional-entity-parser',
    difficulty: {
      level: 'Intermediate',
      color: 'blue',
    },
    topics: ['NLP'],
    states: ['TN', 'MP'],
  },
  {
    column: 1,
    title: 'Speak to the Data',
    description:
      'Make it easier for everyone to interface with the data through automated Q&A and natural language to SQL translation.',
    imageURL: 'nl2',
    url:
      'https://github.com/IBM/covid19-india-data/wiki/Challenge-Tasks#-speak-to-the-data',
    difficulty: {
      level: 'Beginner',
      color: 'green',
    },
    topics: ['NLP', 'HCI'],
    states: ['ALL'],
  },
  {
    column: 2,
    title: 'Data Aggregation',
    description: (
      <>
        Currently, we use only the daily health bulletins put out by individual
        Indian states on their websites. However, the source of COVID data from
        India is myriad and varied. See{' '}
        <Link
          href="https://blog.covid19india.org/2020/06/15/hornbill/"
          target="_blank">
          here
        </Link>
        , for example. Help us extend the automated data extraction pipeline to
        include other sources of information, from kinds of documents to social
        media posts.
      </>
    ),
    imageURL: 'aggr',
    url:
      'https://github.com/IBM/covid19-india-data/wiki/Challenge-Tasks#-data-aggregation',
    difficulty: {
      level: 'Intermediate',
      color: 'blue',
    },
    topics: ['NLP', 'CV'],
    states: ['ALL'],
  },
  {
    column: 2,
    title: 'Flex Your Brains',
    description: (
      <>
        This is an open-ended task. Contribute your insights in the form of{' '}
        <Link href={'/#/analysis'}>Analysis</Link> or{' '}
        <Link href={'/#/anomalies'}>Anomalies</Link> to this website, or help us
        link this page to your scientific papers and blogs. Check out our{' '}
        <Link href={'/#/contributing#resources'}>resources tab</Link> for ideas.
        <br />
        <br />
        You can use this data to validate or extend models developed for other
        countries to India <Reference href={1} /> <Reference href={2} />{' '}
        <Reference href={3} />; developing epidemiological models which
        integrate additional variables <Reference href={4} />{' '}
        <Reference href={5} /> <Reference href={6} /> <Reference href={7} />;
        understanding various aspects of the pandemic in detail{' '}
        <Reference href={8} /> <Reference href={9} />, among others.
      </>
    ),
    imageURL: 'aa',
    difficulty: {
      level: 'Advanced',
      color: 'red',
    },
    topics: [],
    states: ['ALL'],
  },
  {
    column: 0,
    title: 'Data Validation',
    description: (
      <>
        Validate the data automatcially extracted from public health bulletins
        with manually kept maintained data sources.
      </>
    ),
    imageURL: 'validate',
    url:
      'https://github.com/IBM/covid19-india-data/wiki/Challenge-Tasks#-data-validation',
    difficulty: {
      level: 'Beginner',
      color: 'green',
    },
    topics: [],
    states: ['ALL'],
  },
];

export { TASKS };
