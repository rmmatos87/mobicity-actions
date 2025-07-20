import os
import sys
import json
from datetime import datetime, timedelta
from mobicity import Mobicity

# Parse command-line arguments
argv = {x[0].replace("--", ""): x[1] for x in [i.split("=") for i in sys.argv[1:] if "=" in i]}

# Required arguments
required_args = ["shift", "start_day", "pwd"]
missing_args = [arg for arg in required_args if arg not in argv]
if missing_args:
    raise ValueError(f"Missing required arguments: {', '.join(missing_args)}")

# Load JSON configuration
with open(argv["json_usr"], encoding="utf-8") as f:
    user_config = json.load(f)

with open(argv["json_sitemap"], encoding="utf-8") as f:
    sitemap = json.load(f)

shift = argv['shift']
days = 3
if shift != '3D+3N':
    days = int(shift[0])
    shift = 'day' if shift[-1].lower() == 'd' else None
    shift = 'night' if shift[-1].lower() == 'n' else None
start_day = argv['start_day']
pwd = argv['pwd']

ano = datetime.today().year
start_day = start_day if len(start_day.split('/')) == 3 else start_day + '/' + str(ano)
middle_day = (datetime.fromisoformat("-".join(start_day.split(r"/")[::-1])) + timedelta(days=3)).strftime(r"%d/%m/%Y")
time_to_work_d = user_config["time"]["time_to_work"]['day']
time_to_home_d = user_config["time"]["time_to_home"]['day']
time_to_work_n = user_config["time"]["time_to_work"]['night']
time_to_home_n = user_config["time"]["time_to_home"]['night']
addresses = user_config['addresses']
schedule_d = user_config['week_schedule']['day']
schedule_n = user_config['week_schedule']['night']

# Create Mobicity instance and configure
m_d = Mobicity(
    shift='day',
    time_to_work=time_to_work_d,
    time_to_home=time_to_home_d,
    start_day=start_day,
    days=days,
    sitemap=sitemap,
    **addresses
)
m_n = Mobicity(
    shift='night',
    time_to_work=time_to_work_n,
    time_to_home=time_to_home_n,
    start_day=start_day,
    days=days,
    sitemap=sitemap,
    **addresses
)

if shift == '3D+3N':
    m_n.start_day = middle_day
if 'd' in shift:
    for schedule in schedule_d:
        m_d.setup_schedule_weekdays(**schedule)
    m_d.setup_rides(user_config['username'] + "@petrobras.com.br", pwd)
if 'n' in shift:
    for schedule in schedule_n:
        m_n.setup_schedule_weekdays(**schedule)
    m_n.setup_rides(user_config['username'] + "@petrobras.com.br", pwd)
