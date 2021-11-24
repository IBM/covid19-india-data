const QUERIES = [
  {
    subject: 'Daily new cases',
    description: null,
    query:
      'SELECT date, cases_new FROM UK_case_info WHERE cases_new is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'Number of active cases',
    description: null,
    query:
      'SELECT date, active_cases FROM UK_case_info WHERE active_cases is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'Daily tests',
    description: null,
    query:
      'SELECT date, tests_today FROM UK_case_info WHERE tests_today is NOT NULL ORDER BY date ASC',
  },
];

export { QUERIES };
