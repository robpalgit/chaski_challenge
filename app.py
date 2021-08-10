from flask import Flask
from flask import render_template
from flask import request
import os
import utils
import tempfile

service_url = {'SERVICE_URL': os.environ['SERVICE_URL']}
#service_url = {'SERVICE_URL': "http://127.0.0.1:5000"}

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def dash():
    if request.method == "POST":
        file = request.files["csvfile"]

        temp_folder = tempfile.TemporaryDirectory()
        temp_folder_path = temp_folder.name

        filepath = os.path.join(temp_folder_path, file.filename)
        file.save(filepath)

        df = utils.create_dataframe(filepath)
        metrics = utils.calculate_metrics(df)
        resampled_df = utils.generate_resampled_data(df)

        lineplot_data = utils.generate_lineplot(resampled_df)
        histogram_data = utils.generate_histogram(resampled_df)
        piechart_data = utils.generate_piechart(resampled_df)
        
        return render_template(
            "dash.html", 
            lineplot=lineplot_data,
            histogram=histogram_data,
            piechart=piechart_data,
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
