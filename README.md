# ics-calendar-stats
A script to parse ics calendar export and tell you where your time goes.

## How to run?
1. Install Python 3 and virtualenv
2. Clone the repository:
    ```
    git clone https://github.com/ostap-korkuna/ics-calendar-stats.git
    ```
3. Create and activate virtualenv: 
    ```
    cd ics-calendar-stats 
    python3 -m venv venv
    source source venv/bin/activate
    ```
4. Install requirements:
    ```
    pip3 install -r requirements.txt
    ```
5. Export the ics file from google calendar:
https://support.google.com/calendar/answer/37111?hl=en

6. Update configuration file config_example.json to your liking (can do this later) 

7. Run the script, e.g.:
    ```
    python3 ics-calendar-stats/ics-calendar-stats.py -f my_calendar.ics -c config_example.json --date-range "2021-01-01" "2021-01-23"
    ```

Find more useful command line arguments in the next section.

# CLI Arguments

```bash
(venv) ics-calendar-stats $ python3 ics-calendar-stats/ics-calendar-stats.py -h
usage: ics-calendar-stats.py [-h] -f FILE [-c CONFIG] [--date-range DATE_RANGE [DATE_RANGE ...]] [-v] [--csv] [--weekly] [--hours]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Input ics file
  -c CONFIG, --config CONFIG
                        Config for stats tracking
  --date-range DATE_RANGE [DATE_RANGE ...]
                        Date range to filter
  -v, --verbose         Verbose logging
  --csv                 Export summary in csv
  --weekly              In CSV export weekly statistics instead of daily
  --hours               In CSV export data in hours instead of minutes
```

# Config

There's a config file (`example_config.json` included in the repo).
Currently it stores:

#### mailbox
The mailbox you exported ics file from. This is used to filter out events that you did not attend. 

#### category_keywords

List of keywords (substrings) to search in the event title to detect event's category. The first match wins.

# Examples

Get a quick report of activity in a given period (use this also to list activities and see if they are correctly categorized):
```bash
python3 ics-calendar-stats/ics-calendar-stats.py -f my_calendar.ics -c config_example.json --date-range "2021-01-01" "2021-01-23"
```

Export daily stats to CSV:
```bash
python3 ics-calendar-stats/ics-calendar-stats.py -f my_calendar.ics -c config_example.json --date-range "2021-01-01" "2021-01-23" --csv > daily_stats.csv
```

Export weekly stats in hours to CSV:
```bash
python3 ics-calendar-stats/ics-calendar-stats.py -f my_calendar.ics -c config_example.json --date-range "2021-01-01" "2021-01-23" --csv --weekly --hours > weekly_stats.csv
```
