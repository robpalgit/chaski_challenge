from flask import Flask, json
from flask import render_template
from flask import request
from flask import jsonify
import os
import utils

#service_url = {'SERVICE_URL': os.environ['SERVICE_URL']}
service_url = {'SERVICE_URL': "http://127.0.0.1:5000"}

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def dash():
    if request.method == "POST":
        file = request.files["csvfile"]
        if not os.path.isdir("static"):
            os.mkdir("static")
        filepath = os.path.join("static", file.filename)
        file.save(filepath)

        df = utils.create_dataframe(filepath)
        metrics = utils.calculate_metrics(df)
        resampled_df = utils.generate_resampled_data(df)

        lineplot_path = utils.generate_lineplot(resampled_df)
        histogram_path = utils.generate_histogram(resampled_df)
        piechart_path = utils.generate_piechart(resampled_df)

        return render_template(
            "dash.html", 
            lineplot=lineplot_path,
            histogram=histogram_path,
            piechart=piechart_path,
            start_datetime=metrics["start_datetime"],
            duration=metrics["duration"],
            min_bpm=metrics["min_bpm"],
            max_bpm=metrics["max_bpm"],
            avg_bpm=metrics["avg_bpm"],
            **service_url
            )

    return render_template(
        "home.html", 
        **service_url
        )


if __name__ == "__main__":
    app.run(debug=True)
