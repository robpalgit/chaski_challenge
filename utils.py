import pandas as pd
import numpy as np
import os

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
    

def generate_resampled_data(filepath):
    df = pd.read_csv(filepath, skiprows=1, header=1)

    # Convert dateTime
    df["dateTime"] = pd.to_datetime(df["dateTime"], unit="ms")

    # Convert timeSeconds to time
    df["time"] = pd.to_datetime(df["timeSeconds"], unit="s")

    # Drop unnecessary columns
    df.drop(["timeSeconds", "tempOral", "tempNasal", "signalPeriodSec", "dateTime"], axis=1, inplace=True)

    # Set time as index
    df.set_index("time", inplace=True)

    resample_qty = 10
    resample_bin = '{}S'.format(resample_qty)

    resampled_df = df["signalFrequencyBpm"].resample(resample_bin).mean().reset_index()
    resampled_df["time"] = resampled_df["time"].dt.time
    resampled_df.set_index("time", inplace=True)

    # Add new categorical variable 
    resampled_df["bpmZone"] = resampled_df["signalFrequencyBpm"].apply(lambda x: determine_zone(x))

    return resampled_df


def generate_lineplot(resampled_df):
    # Line plot
    plt.figure(figsize=(15,3))
    resampled_df["signalFrequencyBpm"].plot(color="tab:cyan")
    if resampled_df["signalFrequencyBpm"].max() > zone_limits[0]:
        plt.axhline(y=zone_limits[0], color="lime", linestyle="--")
    if resampled_df["signalFrequencyBpm"].max() > zone_limits[1]:
        plt.axhline(y=zone_limits[1], color="tab:orange", linestyle="--")
    if resampled_df["signalFrequencyBpm"].max() > zone_limits[2]:
        plt.axhline(y=zone_limits[2], color="red", linestyle="--")
    plt.legend(["Respiration Rate [BPM]"], loc="best")
    #plt.xticks(rotation=45, ha="right")
    # Save plot
    lineplot_path = os.path.join("static", "lineplot" + ".png")
    plt.savefig(lineplot_path)
    return lineplot_path


def generate_histogram(resampled_df):
    # Histogram
    plt.figure(figsize=(4,3))
    sb.histplot(
        x="signalFrequencyBpm", 
        data=resampled_df, 
        color="tab:cyan",
        bins=np.arange(12,34,1)
        )
    if resampled_df["signalFrequencyBpm"].max() > zone_limits[0]:
        plt.axvline(x=zone_limits[0], color="lime", linestyle="--")
    if resampled_df["signalFrequencyBpm"].max() > zone_limits[1]:
        plt.axvline(x=zone_limits[1], color="tab:orange", linestyle="--")
    if resampled_df["signalFrequencyBpm"].max() > zone_limits[2]:
        plt.axvline(x=zone_limits[2], color="red", linestyle="--")
    plt.title("Respiration Rate [BPM]")
    plt.xlabel("")
    # Save plot
    histogram_path = os.path.join("static", "histogram" + ".png")
    plt.savefig(histogram_path)
    return histogram_path


def generate_piechart(resampled_df):
    data = np.unique(resampled_df["bpmZone"], return_counts=True)
    labels = data[0]
    n_cats = len(labels)
    colors = ["blue", "lime", "tab:orange", "red"]
    
    plt.figure(figsize=(4,3))
    plt.pie(
        x=data[1],
#         labels=labels,
        radius=0.9,
        colors=colors[:n_cats],
        startangle=90,
#         explode=(0,0,0,0.2,0,0,0.1),
        autopct='%1.1f%%',
        labeldistance=1.2,
        textprops={"size": 12}
    )
    #plt.title("Zones", size=14)
    plt.legend(loc='best', labels=labels)
    # Save plot
    piechart_path = os.path.join("static", "piechart" + ".png")
    plt.savefig(piechart_path)
    return piechart_path
