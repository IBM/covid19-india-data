// import React from 'react';
// import { Link } from 'carbon-components-react';

const QUERIES = [
  {
    subject: 'Daily new confirmed cases',
    description: null,
    query:
      'SELECT date, positive_cases FROM KL_daily_summary WHERE positive_cases is NOT NULL ORDER BY date',
  },
  {
    subject: 'Number of active cases',
    description: null,
    query:
      'SELECT date, active_cases FROM KL_cumulative_summary WHERE active_cases is NOT NULL ORDER BY date',
  },
  {
    subject: 'Daily new recoveries',
    description: null,
    query:
      'SELECT date, recovered FROM KL_daily_summary WHERE recovered is NOT NULL ORDER BY date',
  },
  {
    subject: 'Daily new fatalities',
    description: null,
    query:
      'SELECT date, daily_deaths FROM KL_daily_summary WHERE daily_deaths is NOT NULL ORDER BY date',
  },
];

export { QUERIES };
