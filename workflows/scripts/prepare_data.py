import pandas as pd
from hydra import compose, initialize
from sklearn.compose import ColumnTransformer
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, RobustScaler, StandardScaler


def return_config(config_path: str, config: str):
    with initialize(config_path=config_path):
        config = compose(config)
    return config


def preprocess_data(df: pd.DataFrame, scaler_type: str) -> pd.DataFrame:
    """
    Args:
        df (pd.DataFrame): _description_
        scaler_type (str): _description_
    Raises:
        ValueError: _description_
    Returns:
        pd.Dataframe: _description_
    """
    simple_imputer_config = return_config(
        "../../config/preprocessing", config="simpleimputer.yaml"
    )
    knn_imputer_config = return_config(
        "../../config/preprocessing", config="knnimputer.yaml"
    )

    df = df.drop(columns=["Name", "Ticket", "Cabin"])
    cat_cols = ["Embarked", "Pclass"]
    cat_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(**simple_imputer_config)),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )
    num_cols = ["Age", "Fare"]
    if scaler_type == "robust":
        scaler = RobustScaler()
    elif scaler_type == "standard":
        scaler = StandardScaler()
    else:
        raise ValueError("Invalid scaler_type. Choose 'robust' or 'standard'.")
    num_transformer = Pipeline(
        steps=[("imputer", KNNImputer(**knn_imputer_config)), ("scaler", scaler)]
    )
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_transformer, num_cols),
            ("cat", cat_transformer, cat_cols),
        ],
        remainder="passthrough",
    )
    df["Sex"] = df["Sex"].map({"male": 1, "female": 0})
    df_transformed = preprocessor.fit_transform(df)
    feature_names = preprocessor.get_feature_names_out()
    feature_names = [
        name.split("__")[1] if "__" in name else name for name in feature_names
    ]
    df_transformed = pd.DataFrame(df_transformed, columns=feature_names)
    return df_transformed


df = pd.read_csv(snakemake.input[0])
df_robust = preprocess_data(df, "robust")
df_standard = preprocess_data(df, "standard")
df_robust.to_csv(snakemake.output[0])
df_standard.to_csv(snakemake.output[1])
