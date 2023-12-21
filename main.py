from flask import Flask, render_template
import pandas as pd


app = Flask(__name__)

stations = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = stations[['STAID', 'STANAME                                 ']]

@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    # Load dataframe
    filename = f"data_small/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze()/10
    return {"station": station,
            "date": date,
            "temperature": temperature
            }


@app.route("/api/v1/<station>")
def station_data(station):
    # Load dataframe
    filename = f"data_small/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    df["TG"] = df['   TG']/10
    station_all = df[['STAID', '    DATE', 'TG']]
    station_all = station_all.to_html()
    return station_all


@app.route("/api/v1/yearly/<station>/<year>")
def station_year(station, year):
    filename = f"data_small/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(filename, skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df["    DATE"].str.startswith(str(year))].to_html()
    return result


if __name__ == "__main__":
    app.run(debug=True, port=5001)

