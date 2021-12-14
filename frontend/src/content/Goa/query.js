import React from 'react';
import { Link } from 'carbon-components-react';

const QUERIES = [
  {
    subject: 'Daily new cases',
    description: null,
    query:
      'SELECT date, total_cases_new from GA_overview WHERE total_cases_new is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'Daily new fatalities',
    description: null,
    query:
      'SELECT date, deaths_new from GA_overview WHERE deaths_new is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'Daily new hospitalizations',
    description: null,
    query:
      'SELECT date, hospitalized_patients_new from GA_overview WHERE hospitalized_patients_new is NOT NULL ORDER BY date ASC',
  },
];

export { QUERIES };
