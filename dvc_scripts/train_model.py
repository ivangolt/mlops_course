import logging
import pickle
from pathlib import Path

import click
import dvc.api
import joblib
import pandas as pd
from catboost import CatBoostClassifier

from .cli import cli

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def train_model(data: pd.DataFrame, vectorizer) -> CatBoostClassifier:
    params = dvc.api.params_show()
    data = data.dropna()
    features = data["text"]
    target = data["toxic"]

    features = vectorizer.transform(data["text"])

    # model_lr = LogisticRegression(**params["logistic_regression"]).fit(features, target)
    # return model_lr

    model_catboost = CatBoostClassifier(**params["catboost"]).fit(features, target)
    return model_catboost


@cli.command()
@click.argument("input_train_csv_path", type=Path)
@click.argument("input_vectorizer_path", type=Path)
@click.argument("output_model_path", type=Path)
def cli_train(
    input_train_csv_path: Path,
    input_vectorizer_path: Path,
    output_model_path: Path,
):
    data = pd.read_csv(input_train_csv_path)
    tf_idf_vectorizer = joblib.load(input_vectorizer_path)

    logger.info("features and target are download")

    model = train_model(data=data, vectorizer=tf_idf_vectorizer)
    logger.info("model trained")
    pickle.dump(model, output_model_path.open("wb"))
