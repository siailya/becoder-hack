import pandas as pd
from flask import Flask, request, jsonify

from catboost_model.execute import load_model, model_predict

model = load_model(
    model_path='../catboost_model/bccommit'
)

app = Flask(__name__)


@app.post("/api/predict")
def hello_world():
    df = pd.DataFrame.from_dict(request.get_json())

    df["date"] = df['date'].astype(str)
    res = model_predict(df)

    return jsonify({"result": res[0][0]})


if __name__ == '__main__':
    app.run(debug=True)
