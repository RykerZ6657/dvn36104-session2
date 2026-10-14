# DVN36104 Session 2 — three Streamlit apps


Python 3.12 or newer. Install `pip install -r requirements.txt`.


| Part | Main file | What it demonstrates |
|---|---|---|
| C | `uber_pickups.py` | Cached tutorial data, hourly histogram, checkbox, slider and map |
| D | `star_app.py` | Course starter adapted with metallicity, pair-instability and linked HR diagram |
| E | `streamlit_app.py` | Entry point and pages directory with plotting, mapping and dataframe demos |


Run each with `streamlit run <main file>`. Deploy the three entrypoints as
separate public apps through Streamlit Community Cloud. Install dependencies
from the root requirements file. No credentials are needed by the applications.


Official tutorials:
https://docs.streamlit.io/get-started/tutorials/create-an-app
https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app


Star starter/model source:
https://dvn36104.github.io/session2/star_app.py
https://dvn36104.github.io/session2/part-d.html


Public tutorial data:
https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz
https://streamlit-demo-data.s3-us-west-2.amazonaws.com/agri.csv.gz
https://github.com/streamlit/example-data/tree/master/hello/v1


The bundled Uber CSV is the first 10,000 real records, not a representative
sample of all trips. Live download is streamed and cached; a clearly labelled
copy supports temporary source failures. For offline verification set
`TUTORIAL_SAMPLE_MODE=1`. Maps still need internet for base-map tiles.


The stellar model is a teaching approximation. Its portrait is illustrative;
mass, age and metallicity are not a complete physical stellar-evolution model.
The course's main-sequence scalings are not observational mass estimates for
giants or remnants. Solar-metallicity boundaries and low-metallicity
pair-instability outcomes are implemented explicitly.

