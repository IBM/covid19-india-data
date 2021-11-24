const QUERIES = [
  {
    subject: 'New daily cases',
    description: null,
    query:
      'SELECT date, cases_new FROM MH_case_info WHERE cases_new is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'Active cases',
    description: null,
    query:
      'SELECT date, active_cases FROM MH_case_info WHERE active_cases is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'New daily recoveries',
    description: null,
    query:
      'SELECT date, discharged_today FROM MH_case_info WHERE discharged_today is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'New daily fatalities',
    description: null,
    query:
      'SELECT date, deaths_new FROM MH_case_info WHERE deaths_new is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'Number of people under home quarantine',
    description: null,
    query:
      'SELECT date, current_home_quarantine FROM MH_case_info WHERE current_home_quarantine is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'Number of people under institutional quarantine',
    description: null,
    query:
      'SELECT date, current_institutional_quarantine FROM MH_case_info WHERE current_institutional_quarantine is NOT NULL ORDER BY date ASC',
  },
];

export { QUERIES };
