import joblib
import pandas as pd
from hydra import compose, initialize
from hydra.utils import instantiate
from omegaconf import DictConfig
from sklearn.model_selection import train_test_split


def compose_config(overrides: list[str] | None = None) -> DictConfig:
    """get a config for overriding params

    Args:
        overrides (list[str] | None, optional): params with override values

    Returns:
        DictConfig: config
    """

    with initialize(config_path="../../config"):
        hydra_config = compose(config_name="config", overrides=overrides)
    return hydra_config


def train_and_save_model(df, output_file, model_type="GBT", scale_type=None):
    """_summary_

    Args:
        df (_type_): _description_
        output_file (_type_): _description_
        model_type (str, optional): _description_. Defaults to "GBT".
        scale_type (_type_, optional): _description_. Defaults to None.

    Raises:
        ValueError: _description_
    """
    X = df.drop(columns=["Survived"])
    y = df["Survived"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    if model_type == "GBT" or model_type == "RNDF":
        cfg = compose_config(overrides=[f"model='{model_type}'"])
        model = instantiate(cfg["model"])

    else:
        raise ValueError("Invalid model type provided")

    model.fit(X_train, y_train)
    joblib.dump(model, output_file)


df_transform_robust = pd.read_csv(snakemake.input[0])

train_and_save_model(
    df_transform_robust, snakemake.output[0], model_type="GBT", scale_type="robust"
)

train_and_save_model(
    df_transform_robust,
    snakemake.output[1],
    model_type="RNDF",
    scale_type="robust",
)

df_transform_standard = pd.read_csv(snakemake.input[1])
train_and_save_model(
    df_transform_standard,
    snakemake.output[2],
    model_type="GBT",
    scale_type="standard",
)
train_and_save_model(
    df_transform_standard,
    snakemake.output[3],
    model_type="RNDF",
    scale_type="standard",
)
