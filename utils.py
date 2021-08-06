import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
plt.style.use("bmh")
#plt.rcParams['figure.dpi'] = 72 #by default
import seaborn as sb

import os


def determine_zone(bpm):
    if (bpm > 0) & (bpm <= 18):
        return "1 (Low)"
    elif (bpm > 18) & (bpm <= 28):
        return "2 (Medium)"
    elif (bpm > 28) & (bpm <= 40):
        return "3 (High)"
    elif (bpm > 40):
        return "4 (Extreme)"
    

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

    resample_qty = 5
    resample_bin = '{}S'.format(resample_qty)

    resampled_df = df["signalFrequencyBpm"].resample(resample_bin).mean().reset_index()
    resampled_df["time"] = resampled_df["time"].dt.time
    resampled_df.set_index("time", inplace=True)

    # Add new categorical variable 
    resampled_df["bpmZone"] = resampled_df["signalFrequencyBpm"].apply(lambda x: determine_zone(x))

    return resampled_df


def generate_lineplot(resampled_df):
    # Line plot
    plt.figure(figsize=(10,2))
    resampled_df["signalFrequencyBpm"].plot(color="blue")
    if resampled_df["signalFrequencyBpm"].max() > 18:
        plt.axhline(y=18, color="lime", linestyle="--")
    if resampled_df["signalFrequencyBpm"].max() > 28:
        plt.axhline(y=28, color="tab:orange", linestyle="--")
    if resampled_df["signalFrequencyBpm"].max() > 40:
        plt.axhline(y=40, color="red", linestyle="--")
    plt.legend(["Respiration Rate [BPM]"])
    #plt.xticks(rotation=45, ha="right")
    # Save plot
    lineplot_path = os.path.join("static", "lineplot" + ".png")
    plt.savefig(lineplot_path)
    return lineplot_path


def generate_histogram(resampled_df):
    # Histogram
    plt.figure(figsize=(4,3))
    sb.histplot(x="signalFrequencyBpm", data=resampled_df, bins=np.arange(12,34,1))
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
        textprops={"size": 14}
    )
    plt.title("Zones", size=16)
    plt.legend(loc='best', labels=labels)

    piechart_path = os.path.join("static", "piechart" + ".png")
    plt.savefig(piechart_path)
    return piechart_path
