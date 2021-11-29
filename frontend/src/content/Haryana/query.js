const QUERIES = [
  {
    subject: 'Active cases',
    description: null,
    query:
      'SELECT date, active_cases FROM HR_case_info WHERE active_cases is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'Tests conducted daily',
    description: null,
    query:
      'SELECT date, samples_taken_today FROM HR_case_info WHERE samples_taken_today is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'Daily vaccinations',
    description: null,
    query:
      'SELECT date, vax_today_total FROM HR_case_info WHERE vax_today_total is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'Percentage of Male fatalies',
    description: null,
    query:
      'select date, deaths_male / CAST(deaths_total AS REAL) AS perc_deaths_male from HR_case_info WHERE perc_deaths_male is not null ORDER BY date ASC',
  },
  {
    subject: 'Percentage of male samples tested ',
    description: null,
    query:
      'select date, samples_positive_cumulative_male / CAST(samples_positive_cumulative_total AS REAL)  AS perc_male_samples from HR_case_info WHERE perc_male_samples is not null ORDER BY date ASC',
  },
  {
    subject: 'Patients on Oxygen support',
    description: null,
    query:
      'SELECT date, patients_on_oxygen_support FROM HR_critical_case_info WHERE facility_name == "total" ORDER BY date ASC',
  },
];

export { QUERIES };
