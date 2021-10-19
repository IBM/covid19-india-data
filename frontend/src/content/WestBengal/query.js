const QUERIES = [
  {
    subject: 'Total COVID-19 beds in the state',
    description: (
      <>
        This plot looks at the total COVID-19 beds available in the state as the
        pandemic progressed. As is evident, the state nearly doubled the number
        of beds during the second wave as compared to the first wave.
      </>
    ),
    query:
      'SELECT date, covid19_beds FROM WB_hospital WHERE covid19_beds is NOT NULL ORDER BY date',
  },
  {
    subject: 'COVID-19 Bed Occupancy',
    description: (
      <>
        This plot looks at the percentage of occupied COVID-19 beds. It gives us
        an idea of the stress on the hospital infrastructure and how difficult
        it would have been for a COVID-19 patient to get a bed in the state.
      </>
    ),
    query:
      'SELECT date, covid19_bed_occupancy FROM WB_hospital where covid19_bed_occupancy is NOT NULL ORDER BY date',
  },
  {
    subject: 'Ambulances assigned daily',
    description: (
      <>
        This plots looks at the number of ambulances assigned daily in the
        state, as reported in the state's daily bulletin. In the second wave,
        the number of ambulances assigned doubled as compared to the daily
        numbers assigned in the first wave.
      </>
    ),
    query:
      'SELECT date, ambulances_assigned_24h FROM WB_counselling where ambulances_assigned_24h is not NULL ORDER BY date',
  },
];

export { QUERIES };
