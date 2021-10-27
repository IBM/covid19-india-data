// import React from 'react';
// import { Link } from 'carbon-components-react';

const QUERIES = [
  {
    subject: 'Weekly Case Fatality Rate (CFR)',
    description:
      'We compute the Weekly CFR as the ratio of weekly deaths to weekly new cases. Delhi, in particular, shows a stark difference in the difference in the Weekly CFR between the two waves, with the CFR climbing steeply to over 11% in the second wave as opposed to about 4% maximum in the first wave.',
    legend: ['Delhi', 'West Bengal', 'Telangana'],
    query:
      "WITH DL_CFR AS ( select DATE(date, 'weekday 0') as WeekNo , SUM(cases_positive) AS total_positive, SUM(deaths) as total_deaths from DL_case_info GROUP by WeekNo ORDER BY WeekNo ), WB_CFR AS ( select DATE(date, 'weekday 0') as WeekNo , SUM(cases_new) AS total_positive, SUM(deaths_new) as total_deaths from WB_case_info GROUP by WeekNo ORDER BY WeekNo ) , TG_CFR AS (select DATE(date, 'weekday 0') as WeekNo , SUM(cases_new) AS total_positive, SUM(deaths_new) as total_deaths from TG_case_info GROUP by WeekNo ORDER BY WeekNo) SELECT DL_CFR.WeekNo, DL_CFR.total_deaths * 100.0 / DL_CFR.total_positive, WB_CFR.total_deaths * 100.0 / WB_CFR.total_positive, TG_CFR.total_deaths * 100.0 /TG_CFR.total_positive FROM DL_CFR JOIN WB_CFR ON DL_CFR.WeekNo == WB_CFR.WeekNo JOIN TG_CFR on DL_CFR.WeekNo == TG_CFR.WeekNo ORDER BY DL_CFR.WeekNo",
  },
  {
    subject: 'COVID-19 Bed Occupancy',
    description:
      'COVID-19 Bed Occupancy represents the percentage of COVID-19 dedicated beds occupied in the state. In the second wave, Delhi saw over 90% bed occupancy for about 2 weeks in late April 2021, signifying the extreme pressure on the hospital infrastructure and the lack of beds available for COVID-19 patients in the state.',
    legend: ['Delhi', 'West Bengal'],
    query:
      'SELECT D1.date, D2.hospital_beds_occupied * 100.0 / D2.hospital_beds_total AS DL_occupancy, W1.covid19_bed_occupancy AS WB_occupancy FROM DL_case_info D1 JOIN DL_patient_mgmt D2 ON D1.date == D2.date JOIN WB_hospital W1 ON D1.date == W1.date ORDER BY D1.date ASC',
  },
  {
    subject: 'COVID-19 Hospitalization Percentage',
    description:
      'We compute the hospitalization percentage as the ratio of the number of occupied hospital beds to the number of active cases. This is an estimate of how many of the currently active COVID-19 patients are in hospitals versus home isolation.',
    legend: ['Delhi', 'West Bengal'],
    query:
      'SELECT D1.date, D2.hospital_beds_occupied * 100.0 / D1.active_cases AS DL_hosp, (W2.covid19_bed_occupancy * (W2.covid19_beds + W2.icu_hdu_beds))/( W1.cases_active_total) AS WB_hosp FROM DL_cumulative D1 JOIN DL_patient_mgmt D2 ON D1.date == D2.date JOIN WB_case_info W1 ON D1.date == W1.date JOIN WB_hospital W2 ON D1.date == W2.date ORDER BY D1.date ASC',
  },
];

export { QUERIES };
