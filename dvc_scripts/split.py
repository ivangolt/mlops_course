import logging
from pathlib import Path

import click
import dvc.api
import pandas as pd
from sklearn.model_selection import train_test_split

from .cli import cli

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def split_data(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    params = dvc.api.params_show()
    logger.info("Splitting data into train and validation sets...")
    train, test = train_test_split(
        data,
        test_size=params["test_train_split"],
        shuffle=True,
        random_state=params["random_state"],
    )
    logger.info("Data split completed.")
    return train, test


@cli.command()
@click.argument("input_frame_path", type=Path)
@click.argument("train_features_path", type=Path)
@click.argument("val_features_path", type=Path)
def cli_split(
    input_frame_path: Path,
    train_features_path: Path,
    val_features_path: Path,
):
    logger.info("Reading input data from: %s", input_frame_path)
    data = pd.read_csv(input_frame_path)

    train, val = split_data(data)

    logger.info("Writing train features to: %s", train_features_path)
    train.to_csv(train_features_path)

    logger.info("Writing validation features to: %s", val_features_path)
    val.to_csv(val_features_path)

    logger.info("Splitting process completed.")
