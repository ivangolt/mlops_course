import json
import logging
import os
import pickle
from pathlib import Path

import click
import joblib
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    classification_report,
)

from .cli import cli

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def conf_matrix(y_true: np.ndarray, pred: np.ndarray) -> Figure:
    """Plot output confusion patrix to png

    Args:
        y_true (np.ndarray): true label
        pred (np.ndarray): predict label

    Returns:
        Figure: out figure
    """
    plt.ioff()
    fig, ax = plt.subplots(figsize=(5, 5))
    ConfusionMatrixDisplay.from_predictions(y_true, pred, ax=ax, colorbar=False)
    ax.xaxis.set_tick_params(rotation=90)
    _ = ax.set_title("Confusion Matrix")
    plt.tight_layout()
    return fig


# Round all float values in the dictionary recursively to the specified precision
def round_floats_in_dict(data: dict, precision: int = 5) -> dict:
    """Round all float values in the dictionary recursively to the specified precision

    Args:
        data (dict): input data
        precision (int, optional): _description_. Defaults to 5.

    Returns:
        dict: dict of rounded data
    """
    if isinstance(data, dict):
        rounded_dict = {}
        for key, value in data.items():
            rounded_dict[key] = round_floats_in_dict(value, precision)
        return rounded_dict
    elif isinstance(data, list):
        return [round_floats_in_dict(item, precision) for item in data]
    elif isinstance(data, float):
        return round(data, precision)
    else:
        return data


def test_model(data: pd.DataFrame, model: LogisticRegression, vectorizer) -> tuple[dict, Figure]:
    """test model

    Args:
        data (pd.DataFrame): in testing data
        model (LogisticRegression): model for predictions
        vectorizer (_type_): vectorizer for vectorize data

    Returns:
        tuple[dict, Figure]: dict of metrics and figure of conf matrix
    """
    data = data.dropna()
    test_features = data["text"]
    test_target = data["toxic"]

    test_features = vectorizer.transform(data["text"])
    predicts = model.predict(test_features)
    fig = conf_matrix(test_target, predicts)
    report = classification_report(test_target, predicts, output_dict=True)
    return (round_floats_in_dict(report), fig)
    # fig = conf_matrix(test_target, predicts)
    # return classification_report(test_target, predicts, output_dict=True), fig


@cli.command()
@click.argument("test_csv_path", type=Path)
@click.argument("ml_model_path", type=Path)
@click.argument("vectorizer_model_path", type=Path)
@click.argument("metric_path", type=Path)
@click.argument("figure_path", type=Path)
def cli_testing(
    test_csv_path: Path,
    ml_model_path: Path,
    vectorizer_model_path: Path,
    metric_path: Path,
    figure_path: Path,
):
    """running testing model

    Args:
        test_csv_path (Path): in test data path
        ml_model_path (Path): in ml_model path
        vectorizer_model_path (Path): in vectorizer path
        metric_path (Path): out json file for metric
        figure_path (Path): out figure path
    """
    data = pd.read_csv(test_csv_path)
    logger.info("features and target are download")
    ml_model = joblib.load(ml_model_path)
    logger.info("model is downloaded")
    tf_idf_vectorizer = pickle.load(vectorizer_model_path.open("rb"))
    logger.info("Vectorizer is downloaded")

    result, fig = test_model(data=data, model=ml_model, vectorizer=tf_idf_vectorizer)

    os.makedirs(os.path.split(metric_path)[0], exist_ok=True)
    os.makedirs(os.path.split(figure_path)[0], exist_ok=True)

    json.dump(result, metric_path.open("w"))
    plt.savefig(figure_path)
