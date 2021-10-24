// import React from 'react';
// import { Link } from 'carbon-components-react';

const QUERIES = [
  {
    subject: 'Weekly Case Fatality Rate (CFR)',
    description:
      'We compute the Weekly CFR as the ratio of weekly deaths to weekly new cases. Delhi, in particular, shows a stark difference in the difference in the Weekly CFR between the two waves, with the CFR climbing steeply to over 11% in the second wave as opposed to about 4% maximum in the first wave.',
    legend: ['Delhi', 'West Bengal'],
    query:
      "WITH DL_CFR AS ( select DATE(date, 'weekday 0') as WeekNo , SUM(cases_positive) AS total_positive, SUM(deaths) as total_deaths from DL_case_info GROUP by WeekNo ORDER BY WeekNo ), WB_CFR AS ( select DATE(date, 'weekday 0') as WeekNo , SUM(cases_new) AS total_positive, SUM(deaths_new) as total_deaths from WB_case_info GROUP by WeekNo ORDER BY WeekNo ) SELECT DL_CFR.WeekNo, DL_CFR.total_deaths * 100.0 / DL_CFR.total_positive, WB_CFR.total_deaths * 100.0 / WB_CFR.total_positive FROM DL_CFR JOIN WB_CFR ON DL_CFR.WeekNo == WB_CFR.WeekNo ORDER BY DL_CFR.WeekNo",
  },
];

export { QUERIES };
