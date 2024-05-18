import logging
import re
from pathlib import Path

import click
import nltk
import pandas as pd
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from .cli import cli

nltk.download("averaged_perceptron_tagger")
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("omw-1.4")
nltk.download("stopwords")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


stop_words = set(stopwords.words("english"))
slash_pattern = re.compile(r"\b\w+\'\w+\b")
az_pattern = re.compile(r"[^a-zA-Z]")


def text_preprocessing(text):
    """preprocessing function

    Args:
        text (str): an input str

    Returns:
        a cleared input str
    """
    text = slash_pattern.sub("", text)
    text = az_pattern.sub(" ", text)
    tokens = nltk.word_tokenize(text)
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

    return " ".join(filtered_tokens)


def get_wordnet_pos(tag):
    """getting wordnet postag

    Args:
        tag:

    Returns:
        return wordnet postag
    """
    if tag.startswith("J"):
        return "a"  # Adjective
    elif tag.startswith("V"):
        return "v"  # Verb
    elif tag.startswith("N"):
        return "n"  # Noun
    elif tag.startswith("R"):
        return "r"
    else:
        return "n"


def lemmatize_text_with_pos(text):
    """function lemmatize an input str

    Args:
        text : _input str

    Returns:
        lemmatized text
    """
    lemmatizer = WordNetLemmatizer()
    text = text.lower()
    tokens = word_tokenize(text)
    pos_tags = pos_tag(tokens)
    lemmatized_tokens = [
        lemmatizer.lemmatize(token, get_wordnet_pos(tag)) for token, tag in pos_tags
    ]
    return " ".join(lemmatized_tokens)


def dataframe_preprocessing(data: pd.DataFrame) -> pd.DataFrame:
    """a function return preprocessed df

    Args:
        data (pd.DataFrame): input dataframe

    Returns:
        pd.DataFrame: preprocessed dataframe
    """
    logger.info("Starting DataFrame preprocessing")

    # Apply text preprocessing and lemmatization
    data["text"] = data["text"].apply(text_preprocessing).apply(lemmatize_text_with_pos)

    logger.info("DataFrame preprocessing completed")

    return data


@cli.command()
@click.argument("input_frame_path", type=Path)
@click.argument("output_frame_path", type=Path)
def cli_preprocessing(input_frame_path: Path, output_frame_path: Path):
    """Run data preparing

    Args:
        input_frame_path (Path): in dataset file path
        output_frame_path (Path): out dataset file path
    """
    data = pd.read_csv(input_frame_path, index_col="Unnamed: 0")
    processed_data = dataframe_preprocessing(data)
    processed_data.to_csv(output_frame_path)
    logger.info(f"processed dataframe save into: {output_frame_path}")
