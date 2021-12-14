// import React from 'react';
// import { Link } from 'carbon-components-react';

const QUERIES = [
  {
    subject: 'Daily new confirmed cases',
    description: null,
    query:
      'select date, positive_tested_cases from TN_case_info WHERE positive_tested_cases is NOT NULL ORDER BY date',
  },
  {
    subject: 'Number of active cases',
    description: null,
    query:
      'select date, active_cases_today from TN_case_info WHERE active_cases_today is NOT NULL ORDER BY date',
  },
  {
    subject: 'Daily new fatalities',
    description: null,
    query:
      'select date, deaths_today from TN_case_info WHERE deaths_today is NOT NULL ORDER BY date',
  },
];

export { QUERIES };
