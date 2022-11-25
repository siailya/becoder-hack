import pandas as pd
from catboost import CatBoostClassifier
import time


model = None


def load_model():
    global model

    print("Loading model...")
    time_start = time.time()
    model = CatBoostClassifier()
    model.load_model("bccommit")

    print("Model loaded in", time.time() - time_start, "seconds")

    return model


def model_predict(data):
    global model

    return model.predict_proba(data)


if __name__ == '__main__':
    load_model()

    test = {
        "file": ["abc.js"],
        "author": ["Ilya"],
        "msg": ["Test commit"],
        "date": [1669308352]
    }

    test_df = pd.DataFrame.from_dict(test)

    test_df["date"] = test_df['date'].astype(str)

    res = model.predict_proba(test_df)

    print(res)
