from flask import Flask
from flask import render_template
from flask import request
import os
import utils

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
        resampled_df = utils.generate_resampled_data(df)

        lineplot_path = utils.generate_lineplot(resampled_df)
        histogram_path = utils.generate_histogram(resampled_df)
        piechart_path = utils.generate_piechart(resampled_df)

        return render_template(
            "dash.html", 
            lineplot=lineplot_path,
            histogram=histogram_path,
            piechart=piechart_path,
             **{'SERVICE_URL': os.environ['SERVICE_URL']}
             )

    return render_template(
        "home.html", 
        **{'SERVICE_URL': os.environ['SERVICE_URL']}
        )


if __name__ == "__main__":
    app.run(debug=True)
