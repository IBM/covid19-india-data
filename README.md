# Covid-19 India Data 🇮🇳

[![License](https://img.shields.io/badge/license-MIT-purple)](https://github.com/IBM/covid19-india-data/blob/main/LICENSE)
[![Website](https://img.shields.io/badge/website-up-deep%20green)](https://ibm.biz/covid-data-india)
[![Database](https://img.shields.io/badge/database-download-blue)](https://www.dropbox.com/s/hbe04q6vtzapdam/covid-india.db?dl=1)
[![Slack](https://img.shields.io/badge/community-slack-red)](https://join.slack.com/t/covid-19-india-data/shared_invite/zt-uej5v98i-mjggggkLMASKFbZRXzq4xw)

Availability of COVID-19 data is crucial for researchers and policy makers to understand the progression of the pandemic and react to it in real time. [Here is recent plea](https://www.sciencemag.org/news/2021/05/there-are-so-many-hurdles-indian-scientists-plead-government-unlock-covid-19-data) from researchers in India for they urgent access to COVID data collected by government agencies. Individual states and cities in India provide detailed information in their daily media bulletins about the current situation of COVID-19 in their respective locations. However, such data (usually in the form of PDF documents) is not readily accessible in structured form.

While there are [fantastic crowd-sourced efforts](https://www.covid19india.org/) underway to curate such data, manual approaches cannot scale to the volume of the data produced over the long term. Unfortunately, although this project originally began anticipating this outcome, this eventuality has [already come to pass](https://blog.covid19india.org/2021/08/07/end/).

**Project Goals** In this project, we use AI-assisted document and image extraction techniques to automate the extraction of such data in structured (SQL) form from the state-level daily health bulletins; and aim to make this data readily (and freely) available for further research and analysis. The target is to automate the data extraction and curation for each Indian state, so that once the extraction process of each state is complete, we can be on "autopilot" for that state, requiring little to none continued manual curation (other than to respond to changes in schema).

## How to Contribute

The following are a few ways to get going. In general, you can pick up any unassigned issue, or issues tagged with `help wanted`, from the [issue board](https://github.com/IBM/covid19-india-data/issues). 

### ✊ Own a State

`priority`

This is the biggest way you can contribute in the beginning stages of the project. 
"Owning a state" involves:

1. Write the data extraction code for the bulletins of the state. 
This repository provides the starting code and helper packages to make this as simple as possible.
See [here](data_extractor) for instructions. 

2. Eventually reacting (or helping others react) to additions or changes in schema for the
bulletins being put out by that state. The schemas have remained quite stable all this while 
but this issue may show up in a few states as the pandemic evolves.

For the project to succeed, this is the **most crucial part**. Once the data extraction 
code for a state is done, the logging of data for that state is automatic and we can 
~~sit back and relax~~ scale up to the rest of the country over time.
We hope we can get to good coverage before support for 
[covid19india.org](https://blog.covid19india.org/2021/08/07/end/)
ends on Oct 31. 🤞

### 😒 Data Cleaning

1. Remove missing data / deal with missing for the plots.
2. Idenitify possible outliers and errors. 

### 🤓 Analysis

Analyze the data for insights, irregularities, etc. You can put up results of your analysis in your papers, blogs, etc. 
(and point to that from our [landing page](https://ibm.biz/covid-data-india)) or directly add it to our landing page as a 
[new page](frontend/README.md#adding-a-new-page).

## Current state roster

| State | Link to Daily Bulletin | Owner (backend) | Owner (frontend) | Status |
|-------|------------------------|-----------------|------------------|--------|
| Delhi (DL) | [Link](http://health.delhigovt.nic.in/wps/wcm/connect/doit_health/Health/Home/Covid19/Bulletin+August+2021) | [Mayank Agarwal](https://github.com/MayankAgarwal) | [Tathagata Chakraborti](https://github.com/TathagataChakraborti) | :white_check_mark: &nbsp; COMPLETE ([Wiki](https://github.com/IBM/covid19-india-data/wiki/States#delhi-dl-database-schema)) |
| West Bengal (WB) | [Link](https://www.wbhealth.gov.in/pages/corona/bulletin) | [Mayank Agarwal](https://github.com/MayankAgarwal) | [Tathagata Chakraborti](https://github.com/TathagataChakraborti) | :white_check_mark: &nbsp; COMPLETE ([Wiki](https://github.com/IBM/covid19-india-data/wiki/States#west-bengal-wb-database-schema)) | 
| Telengana (TG) | [Link](https://covid19.telangana.gov.in/announcements/media-bulletins/) | [Mayank Agarwal](https://github.com/MayankAgarwal) | [Tathagata Chakraborti](https://github.com/TathagataChakraborti) | :construction: &nbsp; IN PROGRESS ([#4](https://github.com/IBM/covid19-india-data/issues/4)) | 
| Karnataka (KA) | [Link](https://covid19.karnataka.gov.in/govt_bulletin/en) | [Own it!](https://github.com/IBM/covid19-india-data/pulls) |  | |  [TBD]() |
| Tamil Nadu (TN) | [Link](https://stopcorona.tn.gov.in/daily-bulletin/) | [Own it!](https://github.com/IBM/covid19-india-data/pulls) |  | |  [TBD]() |
| Kerala (KL) | [Link](https://dhs.kerala.gov.in/%e0%b4%a1%e0%b5%86%e0%b4%af%e0%b4%bf%e0%b4%b2%e0%b4%bf-%e0%b4%ac%e0%b5%81%e0%b4%b3%e0%b5%8d%e0%b4%b3%e0%b4%b1%e0%b5%8d%e0%b4%b1%e0%b4%bf%e0%b4%a8%e0%b5%8d%e2%80%8d/) | [Own it!](https://github.com/IBM/covid19-india-data/pulls) |  | |  [TBD]() |
| Madhya Pradesh (MP) | [Link](http://sarthak.nhmmp.gov.in/covid/health-bulletin/) | [Own it!](https://github.com/IBM/covid19-india-data/pulls) |  | |  [TBD]() |
| Punjab (PB) | [Link](http://pbhealth.gov.in/media-bulletin.htm) | [Own it!](https://github.com/IBM/covid19-india-data/pulls) |  | |  [TBD]() |
| Uttarakhand (UK) | [Link1](https://health.uk.gov.in/pages/view/134-covid19-health-bulletin-for-uttarakhand-page-01), [Link2](https://health.uk.gov.in/pages/view/151-covid19-health-bulletin-for-uttarakhand-page-10)| [Own it!](https://github.com/IBM/covid19-india-data/pulls) |  | |  [TBD]() |
| `Add new state` | |  |  | |  |

As you might have noticed, this is an incomplete list of Indian states. 
Not all states produce this form of data. ☹️
&nbsp; We will continue adding new sources over time.

### Interested? Join the Community 

[`slack`](https://join.slack.com/t/covid-19-india-data/shared_invite/zt-uej5v98i-mjggggkLMASKFbZRXzq4xw)
