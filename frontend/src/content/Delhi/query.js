import React from 'react';
import { Link } from 'carbon-components-react';

const QUERIES = [
  {
    subject: 'Daily new cases',
    description: <></>,
    query:
      'SELECT date, cases_positive from DL_case_info WHERE cases_positive is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'Daily new fatalities',
    description: <></>,
    query: 'SELECT date, deaths from DL_case_info WHERE deaths is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'Ratio of RTPCR tests',
    description: (
      <>
        Delhi state uses the cheaper, quicker, but less accurate Rapid Antigen
        tests along with the more reliable and accurate but more time taking
        RTPCR tests to detect COVID-19 cases. The state has been questioned for
        its excessive use of Rapid Antigen Tests in the past leading to a false
        sense of security [
        <Link
          href="https://theprint.in/health/in-delhi-rapid-antigen-tests-fuel-spurt-in-testing-but-false-negatives-a-worry/464235/"
          target="_blank">
          link
        </Link>
        ]. This chart plots the ratio of RTPCR tests to the Rapid Antigen Tests
        in Delhi. In the initial phases of the pandemic, RTPCR tests comprised
        only 20-40% of the total tests performed, implying an excessive reliance
        on Rapid Antigen Tests. This ratio has however improved with time, and
        during the second wave, as much as 80% of the total tests conducted were
        RTPCR tests.
      </>
    ),
    query:
      'Select D1.date, D1.rtpcr_test_24h *1.0/ D2.tests_conducted AS rtpcr_ratio FROM DL_testing_status D1 JOIN DL_case_info D2 ON D1.date == D2.date WHERE rtpcr_ratio is NOT NULL ORDER BY D1.date ASC',
  },
  {
    subject: 'Vacant hospital beds',
    description: <>Number of hospital beds vacant in the state</>,
    query:
      'SELECT date, hospital_beds_vacant FROM DL_patient_mgmt WHERE hospital_beds_vacant is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'Number of individuals in home isolation',
    description: <></>,
    query:
      'SELECT date, home_isolation_count FROM DL_patient_mgmt WHERE home_isolation_count is NOT NULL ORDER BY date ASC',
  },
  {
    subject: 'Hospitalization percentage query',
    description: (
      <>
        {' '}
        This figure looks at the hospitalization rates in Delhi (occupied
        hospital beds / number of active cases). While the hospitalization rate
        during the initial waves of COVID-19 is estimated to be around 40-50%,
        it is comparatively higher during the deadly second wave and is
        estimated to be around 60-65%.
      </>
    ),
    query:
      'SELECT D1.date, (D2.hospital_beds_occupied + D2.covid_care_center_beds_occupied + D2.covid_health_center_beds_occupied) *1.0/ D1.active_cases AS perc_hospitalized from DL_cumulative D1 JOIN DL_patient_mgmt D2 ON D1.date == D2.date WHERE perc_hospitalized is NOT NULL ORDER BY D1.date ASC',
  },
  {
    subject: 'Number of containment zones',
    description: <></>,
    query:
      'SELECT date, containment_zones FROM DL_containment WHERE containment_zones is NOT NULL ORDER BY date ASC',
  },
];

export { QUERIES };
