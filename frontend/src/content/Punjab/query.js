// import React from 'react';
// import { Link } from 'carbon-components-react';

const QUERIES = [
  {
    subject: 'Active cases',
    description: null,
    query:
      'SELECT date, active_cases FROM PB_cases WHERE active_cases is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'Daily new tests',
    description: null,
    query:
      'SELECT date, tests_new FROM PB_cases WHERE tests_new is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'Patients on ventilator support',
    description: null,
    query:
      'SELECT date, ventilator_support_active_patients FROM PB_cases where ventilator_support_active_patients is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'Total Mucormycosis cases',
    description: null,
    query:
      'SELECT date, cases_total FROM PB_mucormycosis_cases WHERE cases_total is NOT NULL ORDER BY date ASC',
  },
];

export { QUERIES };
