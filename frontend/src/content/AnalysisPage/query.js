// import React from 'react';
// import { Link } from 'carbon-components-react';

const QUERIES = [
  // {
  //   subject: 'Weekly Case Fatality Rate (CFR)',
  //   description: "WHATS GOING ON",
  //   legend: ["Delhi", "West Bengal"],
  //   query: "WITH DL_CFR AS ( select strftime('%Y-%W', date) as WeekNo , SUM(cases_positive) AS total_positive, SUM(deaths) as total_deaths from DL_case_info GROUP by WeekNo ORDER BY WeekNo ), WB_CFR AS ( select strftime('%Y-%W', date) as WeekNo , SUM(cases_new) AS total_positive, SUM(deaths_new) as total_deaths from WB_case_info GROUP by WeekNo ORDER BY WeekNo ) SELECT DL_CFR.WeekNo, DL_CFR.total_deaths * 100.0 / DL_CFR.total_positive, WB_CFR.total_deaths * 100.0 / WB_CFR.total_positive FROM DL_CFR JOIN WB_CFR ON DL_CFR.WeekNo == WB_CFR.WeekNo ORDER BY DL_CFR.WeekNo"
  // },
  {
    subject: 'COVID-19 Bed Occupancy',
    description: 'WHATS GOING ON',
    legend: ['Delhi', 'West Bengal'],
    query:
      'SELECT D1.date, D2.hospital_beds_occupied * 100.0 / D2.hospital_beds_total AS DL_occupancy, W1.covid19_bed_occupancy AS WB_occupancy FROM DL_case_info D1 JOIN DL_patient_mgmt D2 ON D1.date == D2.date JOIN WB_hospital W1 ON D1.date == W1.date ORDER BY D1.date ASC',
  },
  {
    subject: 'COVID-19 Hospitalization Percentage',
    description: 'WHATS GOING ON',
    legend: ['Delhi', 'West Bengal'],
    query:
      'SELECT D1.date, D2.hospital_beds_occupied * 100.0 / D1.active_cases AS DL_hosp, (W2.covid19_bed_occupancy * (W2.covid19_beds + W2.icu_hdu_beds))/( W1.cases_active_total) AS WB_hosp FROM DL_cumulative D1 JOIN DL_patient_mgmt D2 ON D1.date == D2.date JOIN WB_case_info W1 ON D1.date == W1.date JOIN WB_hospital W2 ON D1.date == W2.date ORDER BY D1.date ASC',
  },
];

export { QUERIES };
