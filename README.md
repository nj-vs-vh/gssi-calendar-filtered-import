- follow [this](https://developers.google.com/calendar/api/quickstart/python) quickstart guide up
  until "Install the Google client library" step
- setup environment for this script with
  `python3.10 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
- in `import_gssi_lectures.py`, edit `MY_SHORT_COURSES` variable to include your courses
- create empty google calendar and copy it's ID (Settings and sharing -> Calendar ID), export it as
  environment variable (`export TARGET_CALENDAR_ID="<my calendar id>"`)
- run the script with `python import_gssi_lectures`
