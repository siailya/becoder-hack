import json

import pandas as pd
from flask import Flask, request, jsonify, Response, send_from_directory
from flask_cors import CORS

from analyse.main import get_most_edit_person_for_file
from catboost_model.execute import load_model, model_predict

model = load_model(
    model_path='catboost_model/bccommit'
)

with open("analyse/analyse_data_angular.json", 'r') as read_file:
    main_data = json.load(read_file)

# create app and set static files folder and index.html
app = Flask(__name__,
            static_folder="static",
            static_url_path="/")
CORS(app)


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.post("/api/predict")
def hello_world():
    df = pd.DataFrame.from_dict(request.get_json())

    df["date"] = df['date'].astype(str)
    res = model_predict(df)
    try:
        return jsonify({"result": res[0][0], "person": get_most_edit_person_for_file(main_data, df["file"][0])})
    except ValueError:
        return Response('Не найден файл', status=502, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
