from flask import Flask, request
from catboost_model.execute import load_model,model_predict
model = load_model()

app = Flask(__name__)

@app.post("/api/predict")
def hello_world():
    return model_predict(request.get_json())

if __name__ == '__main__':
    app.run(debug=True)