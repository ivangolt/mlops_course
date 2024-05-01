import os
configfile: "workflows/config.yaml"

SCALERS = ['robust', 'standart']
MODELS = ['gbt', 'rndf']

rule all:
    input: ("workflows/models/{model}_models_{scaler}.pkl", model=MODELS, scaler=SCALERS)

rule train_model:
    input: 
        expand("data/prepared_data/titanic_prepared_{scaler}.csv", scaler=SCALERS)
    output: 
        expand("workflows/models/{model}_models_{scaler}.pkl", model=MODELS, scaler=SCALERS)
    threads: config["n_threads"]
    script: "workflows/scripts/train_model.py"


rule prepare_data:
    input: "data/titanic_data/titanic.csv"
    output: 
        expand("data/prepared_data/titanic_prepared_{scaler}.csv", scaler=SCALERS)
    threads: config["n_threads"]
    script: "workflows/scripts/prepare_data.py"


rule load_data:
    input: "data/kaggle_data/train.csv"
    output: "data/titanic_data/titanic.csv"
    threads: config["n_threads"]
    script: "workflows/scripts/load_data.py"

