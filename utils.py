import pandas as pd
import numpy as np
#import os
import base64
from io import BytesIO

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
plt.style.use("bmh")
#plt.rcParams['figure.dpi'] = 72 #by default
import seaborn as sb


zone_limits = [18, 28, 40]

def determine_zone(bpm):
    if (bpm > 0) & (bpm <= zone_limits[0]):
        return "Zone 1 (Low)"
    elif (bpm > zone_limits[0]) & (bpm <= zone_limits[1]):
        return "Zone 2 (Medium)"
    elif (bpm > zone_limits[1]) & (bpm <= zone_limits[2]):
        return "Zone 3 (High)"
    elif (bpm > zone_limits[2]):
        return "Zone 4 (Extreme)"
    

def create_dataframe(filepath):
    df = pd.read_csv(filepath, skiprows=1, header=1)
    
    # Convert dateTime
    df["dateTime"] = pd.to_datetime(df["dateTime"], unit="ms")

    # Convert timeSeconds to time
    df["time"] = pd.to_datetime(df["timeSeconds"], unit="s")

    return df


def calculate_metrics(df):
    metrics = {
        'start_datetime': df["dateTime"].dt.strftime("%Y-%m-%d %H:%M:%S")[0],
        'duration': df["time"].dt.strftime("%H:%M:%S").max(),
        'min_bpm': str(round(df["signalFrequencyBpm"].min(), 2)),
        'max_bpm': str(round(df["signalFrequencyBpm"].max(), 2)),
        'avg_bpm': str(round(df["signalFrequencyBpm"].mean(), 2))
        }
    return metrics


def generate_resampled_data(df, resample_num=10):
    # Drop unnecessary columns
    df.drop(["timeSeconds", "tempOral", "tempNasal", "signalPeriodSec", "dateTime"], axis=1, inplace=True)

    # Set time as index
    df.set_index("time", inplace=True)

    resample_bin = '{}S'.format(resample_num)
    resampled_df = df["signalFrequencyBpm"].resample(resample_bin).mean().reset_index()
    resampled_df["time"] = resampled_df["time"].dt.time
    resampled_df.set_index("time", inplace=True)

    # Add new categorical variable 
    resampled_df["bpmZone"] = resampled_df["signalFrequencyBpm"].apply(lambda x: determine_zone(x))

    return resampled_df


def generate_lineplot(resampled_df):
    fig = Figure(figsize=(15,3))
    ax = fig.subplots()
    # Line plot
#    plt.figure(figsize=(15,3))
    resampled_df["signalFrequencyBpm"].plot(color="tab:cyan", ax=ax)
    # Horizontal lines
    if resampled_df["signalFrequencyBpm"].max() > zone_limits[0]:
        ax.axhline(y=zone_limits[0], color="lime", linestyle="--")
    if resampled_df["signalFrequencyBpm"].max() > zone_limits[1]:
        ax.axhline(y=zone_limits[1], color="tab:orange", linestyle="--")
    if resampled_df["signalFrequencyBpm"].max() > zone_limits[2]:
        ax.axhline(y=zone_limits[2], color="red", linestyle="--")
    ax.set_title("Respiration Rate [BPM] vs. Time [hh:mm:ss]")
    ax.set_xlabel("")
    ax.legend(["Respiration Rate [BPM]"], loc="best")
#    # Save plot
#    lineplot_path = os.path.join(dir_path, "lineplot" + ".png")
#    plt.savefig(lineplot_path)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    data = f"data:image/png;base64,{data}"
    return data


def generate_histogram(resampled_df):
    fig = Figure(figsize=(4,3))
    ax = fig.subplots()
    # Histogram
#    plt.figure(figsize=(4,3))
    sb.histplot(
        x="signalFrequencyBpm", 
        data=resampled_df, 
        color="tab:cyan",
        bins=np.arange(12,34,1),
        ax=ax
        )
    # Vertical lines
    if resampled_df["signalFrequencyBpm"].max() > zone_limits[0]:
        ax.axvline(x=zone_limits[0], color="lime", linestyle="--")
    if resampled_df["signalFrequencyBpm"].max() > zone_limits[1]:
        ax.axvline(x=zone_limits[1], color="tab:orange", linestyle="--")
    if resampled_df["signalFrequencyBpm"].max() > zone_limits[2]:
        ax.axvline(x=zone_limits[2], color="red", linestyle="--")
    ax.set_title("Respiration Rate [BPM]")
    ax.set_xlabel("")
    ax.set_xticks(np.arange(12,34,2))
    ax.set_ylabel("")
    ax.set_yticks([])
#    # Save plot
#    histogram_path = os.path.join(dir_path, "histogram" + ".png")
#    plt.savefig(histogram_path)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    data = f"data:image/png;base64,{data}"
    return data


def generate_piechart(resampled_df):
    data = np.unique(resampled_df["bpmZone"], return_counts=True)
    labels = data[0]
    n_cats = len(labels)
    colors = ["blue", "lime", "tab:orange", "red"]

    fig = Figure(figsize=(4,3))
    ax = fig.subplots()
#    plt.figure(figsize=(4,3))
    ax.pie(
        x=data[1],
#         labels=labels,
        radius=0.9,
        colors=colors[:n_cats],
        startangle=90,
#         explode=(0,0,0,0.2,0,0,0.1),
        autopct='%1.1f%%',
        labeldistance=1.2,
        textprops={"size": 10}
    )
    #plt.title("Zones", size=14)
    ax.legend(loc='best', labels=labels, fontsize=8)
#    # Save plot
#    piechart_path = os.path.join(dir_path, "piechart" + ".png")
#    plt.savefig(piechart_path)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    data = f"data:image/png;base64,{data}"
    return data
