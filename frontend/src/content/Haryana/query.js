// import React from 'react';
// import { Link } from 'carbon-components-react';

const QUERIES = [
  {
    subject: 'Active cases',
    description: <></>,
    query:
      'SELECT date, active_cases FROM HR_case_info WHERE active_cases is NOT NULL',
  },
  {
    subject: 'Tests conducted daily',
    description: <></>,
    query:
      'SELECT date, samples_taken_today FROM HR_case_info WHERE samples_taken_today is NOT NULL',
  },
  {
    subject: 'Daily vaccinations',
    description: <></>,
    query:
      'SELECT date, vax_today_total FROM HR_case_info WHERE vax_today_total is NOT NULL',
  },
  {
    subject: 'Percentage of Male fatalies',
    description: <></>,
    query:
      'select date, deaths_male / CAST(deaths_total AS REAL) AS perc_deaths_male from HR_case_info WHERE perc_deaths_male is not null ORDER BY date ASC',
  },
  {
    subject: 'Difference in number of male and female sampled',
    description: (
      <>
        We compute the cumulative difference in samples tested for males and females in the state. As is evident, there is a growing
        difference between the two quantities, indicating that over time, more men were tested for COVID-19 then women.
      </>
    ),
    query:
      'select date, samples_positive_cumulative_male  - samples_positive_cumulative_female  AS tests_gender_diff from HR_case_info WHERE tests_gender_diff is not null ORDER BY date ASC',
  }
];

export { QUERIES };
