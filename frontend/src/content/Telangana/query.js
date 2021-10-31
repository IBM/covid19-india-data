// import React from 'react';
// import { Link } from 'carbon-components-react';

const QUERIES = [
  {
    subject: 'Daily new cases',
    description: <></>,
    query:
      'SELECT date, cases_new FROM TG_case_info WHERE cases_new is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'Daily new fatalities',
    description: <></>,
    query:
      'SELECT date, deaths_new FROM TG_case_info WHERE deaths_new is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'Tests conducted daily',
    description: <></>,
    query:
      'SELECT date, tests_today FROM TG_testing_info WHERE tests_today is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'Percentage of symptomatic cases',
    description: (
      <>
        Percentage of total cases reported to be symptomatic in the state health
        bulletin. The number of asymptomatic individuals is (100 - number of
        symptomatic individuals).
      </>
    ),
    query:
      'SELECT date, perc_symptomatic FROM TG_symptomatic WHERE perc_symptomatic is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'Cases in home isolation',
    description: <></>,
    query:
      'SELECT date, cases_in_isolation FROM TG_case_info WHERE cases_in_isolation is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'Percentage of active cases in home isolation',
    description: <></>,
    query:
      'WITH TG_caseinfo AS (SELECT date, cases_in_isolation, cases_total - recovered_total - deaths_total AS active FROM TG_case_info) SELECT date, cases_in_isolation/CAST(active AS REAL) FROM TG_caseinfo ORDER BY date ASC',
  },
];

export { QUERIES };
