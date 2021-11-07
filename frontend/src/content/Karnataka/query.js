// import React from 'react';
// import { Link } from 'carbon-components-react';

const QUERIES = [
  {
    subject: 'Daily new confirmed cases',
    description: <></>,
    query:
      'SELECT date, cases_new from KA_case_info WHERE cases_new is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'Number of active cases',
    description: <></>,
    query:
      'SELECT date, cases_active from KA_case_info WHERE cases_active is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'Daily new discharges',
    description: <></>,
    query:
      'SELECT date, discharged_new from KA_case_info WHERE discharged_new is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'Daily new fatalities',
    description: <></>,
    query:
      'SELECT date, deaths_new from KA_case_info WHERE deaths_new is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'Test positivity rate',
    description: <></>,
    query:
      'SELECT date, positivity_rate_percent FROM KA_case_info WHERE positivity_rate_percent is NOT NULL ORDER BY date ASC',
  },
];

export { QUERIES };
