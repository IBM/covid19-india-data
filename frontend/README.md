# Landing Page

[![Website](https://img.shields.io/badge/design-carbon-blue)](https://www.carbondesignsystem.com/)

This is the source code for the [landing page](https://ibm.biz/covid-data-india) of the COVID-19 India Data project.
The goal of the landing page is to make the data quickly accessible, in its most basic form, for researchers to explore.
Findings from the data will also be added to the landing page over time.

## Setting up locally

```bash
frontend:~$ yarn
frontend:~$ yarn start
```

### Configuration

1. The default sampling rate at which to display the graphs on the landing page: this setting will ensure that
   graphs show data every `sampling_rate` days. This setting is in place to save downloading large amoutns of data
   for the viewer as well as to speed up the plotting on the browser.

```json
sampling_rate: 10
```

2. List of states to display:

Each state in the configuration is key-ed by its `short_name` which is the same as that used by the state 
in its entry in the database (and is used for all calls to fetch data from it).
The full name is used for display purposes only.
The `short_name` is also visible in the [table schemas](https://github.com/IBM/covid19-india-data/wiki/States), 
the raw link to this image from the [wiki](https://github.com/IBM/covid19-india-data/wiki)
is also provided in the config.

```json
"states": {
  "DL": {
    "name" : "Delhi",
    "short_name" : "DL",
    "link_to_db_schema" : "https://raw.githubusercontent.com/IBM/covid19-india-data/main/docs/images/DL_tables.png"
  },
  "WB": {
    "name" : "West Bengal",
    "short_name" : "WB",
    "link_to_db_schema" : "https://raw.githubusercontent.com/IBM/covid19-india-data/main/docs/images/WB_tables.png"
  }
}
```

### Using the DB locally

If you are running the DB locally for testing:

1. Bring up the DB server [here](../serve_db).
2. Add link to the local server in the [configuration file](./src/config.json).

```json
data_server: "http://localhost:3456"
```

## Adding a new page

1. Make a copy of the [NewStatePage](./src/content/NewStatePage) template inside the `content` directory.
2. Replace "NewStatePage" with the name of your state. See [Delhi](./src/content/Delhi) or [West Bengal](./src/content/WestBengal) for examples.
3. Add your state to the static nav Header
   - Import your page in [App.js](./src/App.js#L14): `import NewStatePage from './content/NewStatePage';`
   - Add a new route in [App.js](./src/App.js#L38): `<Route exact path="/NewStatePage" component={NewStatePage} />`
4. Add custom styles for your page in [app.scss](https://github.com/IBM/covid19-india-data/blob/main/frontend/src/app.scss#L14):
   `@import './content/WestBengal/new-state.scss';`
5. Add your entry in the list of states to display in [config.json](./src/config.json) as seen above. Note that the short_name corresponds to
   the entry of the state in the DB. See [here](../docs/images/DL_tables.png) for an example: "DL" for Delhi.
