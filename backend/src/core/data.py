from typing import Any, Tuple, Dict, List
import pandas as pd
import numpy as np

from sklearn.pipeline import Pipeline


def preprocess(data: Any)-> str:
    return str(data)

def predict(data: str, model: Pipeline) -> np.ndarray:

    prediction = model.predict(pd.DataFrame(columns = ["text"], data = [data]))

    return np.array(prediction)

def explain_prediction(mapping: Dict[str, List[str]], prediction: np.ndarray)-> List[List[str]]:
    result = []
    indices = np.where(prediction == 1)
    for idx in indices[1].tolist():
        result.append(mapping[str(idx)])
    return result