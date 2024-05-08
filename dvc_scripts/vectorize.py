import logging
import pickle
from collections import OrderedDict
from pathlib import Path

import cli
import click
import dvc.api
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from .cli import cli  # noqa: F811

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def train_tf_df_vectorize(data: pd.DataFrame) -> TfidfVectorizer:
    params = dvc.api.params_show()

    tfidf_vectorizer = TfidfVectorizer(**params["vectorizer_tfidf"])
    logger.info("Starting fitting vectorizer...")
    data = data.dropna()
    tfidf_vectorizer.fit(data["text"])

    # Dictionary ordering in TF/IDF vectoriser to improve reproducibility
    tfidf_vectorizer.vocabulary_ = OrderedDict(
        sorted(tfidf_vectorizer.vocabulary_.items(), key=lambda kv: kv[1])
    )
    tfidf_vectorizer._stop_words_id = 0

    logger.info("vectorizer is fitted")

    return tfidf_vectorizer


@cli.command()
@click.argument("input_frame_path", type=Path)
@click.argument("vectorizer_path", type=Path)
def cli_tfidf(input_frame_path: Path, vectorizer_path: Path):
    data = pd.read_csv(input_frame_path)
    vectorizer = train_tf_df_vectorize(data)
    pickle.dump(vectorizer, vectorizer_path.open("wb"))
    logger.info(f"tf_idf save to: {vectorizer_path}")
