import React from 'react';
import { Link } from 'carbon-components-react';

const QUERIES = [
  {
    subject: 'Hospitalization percentage query',
    compare_across_states: true,
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
      'SELECT D1.date, (D2.hospital_beds_occupied + D2.covid_care_center_beds_occupied + D2.covid_health_center_beds_occupied) *1.0/ D1.active_cases AS perc_hospitalized from DL_cumulative D1 JOIN DL_patient_mgmt D2 ON D1.date == D2.date WHERE perc_hospitalized is NOT NULL',
  },
  {
    subject: 'Ratio of RTPCR tests',
    compare_across_states: false,
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
      'Select D1.date, D1.rtpcr_test_24h *1.0/ D2.tests_conducted AS rtpcr_ratio FROM DL_testing_status D1 JOIN DL_case_info D2 ON D1.date == D2.date WHERE rtpcr_ratio is NOT NULL',
  },
  {
    subject: 'Vacant beds to new active cases ratio',
    compare_across_states: true,
    description: (
      <>
        This plot looks at the ratio of vacant hospital beds to the number of
        newly added active cases that day, and gives us an idea of the stress on
        the hospital infrastructure. At the height of the first wave, Delhi had
        enough vacant hospital beds to accommodate for 4-5 days of newly active
        (confirmed - recovered) cases. However, during the second wave (April
        2021), this ratio reduced to less than a day. This implies that vacant
        hospital beds as a percentage of newly added active cases were extremely
        scarce, and especially during the second wave [
        <Link
          href="https://www.bbc.com/news/av/world-asia-india-56864789"
          target="_blank">
          link
        </Link>
        ]
      </>
    ),
    query:
      'SELECT D1.date, (D1.hospital_beds_vacant * 1.0 / (D2.cases_positive - D2.cases_recovered - D2.deaths)) AS beds_cases_ratio from DL_patient_mgmt D1 JOIN DL_case_info D2 on D1.date == D2.date where beds_cases_ratio is not NULL and beds_cases_ratio >= 0',
  },
];

export { QUERIES };
