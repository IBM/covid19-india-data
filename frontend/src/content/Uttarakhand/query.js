import React from 'react';
import { Link } from 'carbon-components-react';

const QUERIES = [
  {
    subject: 'Daily new cases',
    description: <></>,
    query:
      'SELECT date, cases_new FROM UK_case_info WHERE cases_new is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'Number of active cases',
    description: <></>,
    query:
      'SELECT date, active_cases FROM UK_case_info WHERE active_cases is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'Daily tests',
    description: <></>,
    query:
      'SELECT date, tests_today FROM UK_case_info WHERE tests_today is NOT NULL ORDER BY date ASC',
  },
];

export { QUERIES };
