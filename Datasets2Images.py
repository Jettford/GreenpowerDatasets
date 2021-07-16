import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import requests
import json

Datapoints = ["Input throttle (%)", "Amps (A)", "Temp2 (C)"]

if not os.path.exists("output"):
    os.mkdir("output")

apiReturn = requests.get("https://api.github.com/repos/jettford/GreenpowerDatasets/contents/").text

apiJSON = json.loads(apiReturn)

for file in apiJSON:
    if not file["name"].split(".")[1] == "csv": continue
    if os.path.exists("output/" + (file["name"].split(".")[0])): os.rmdir("output/" + (file["name"].split(".")[0]))
    os.mkdir("output/" + (file["name"].split(".")[0]))
    df = pd.read_csv(file["download_url"])
    df['time'] = [datetime.fromtimestamp(x / 1000).strftime('%H:%M:%S') for x in df['timestamp']]

    for datapoint in Datapoints:
        fig = px.line(df, x = 'time', y = datapoint, title='Pugh Practice 2 Telemetry data')
        fig.write_image("output/" + (file["name"].split(".")[0]) + "/" + datapoint + ".png")
