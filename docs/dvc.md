# Report of DVC task
This task comleted in branch [dvc](https://gitlab.com/ivan_golt/mlops_course/-/tree/dvc)

In this task fitting model for predict label ("toxic": 1, "non_toxic": 0) of comments in "Datashop" site.
For fitting have been choosen two 1) Logistic Regression, 2) Catboost

## Pipeline
Pipeline consist the next stages:
1) data_preprocessing
2) splitting_data
3) tf_idf fitting
4) training ml model
5) testing model

All stages desribe in [dvc.yaml](https://gitlab.com/ivan_golt/mlops_course/-/blob/dvc/dvc.yaml)

Also using initializing parameters of models with dvc.api [params.yaml](https://gitlab.com/ivan_golt/mlops_course/-/blob/dvc/params.yaml)

## DVC Storage Preparation

dvc init:
`dvc init`\
`dvc remote add -d --project gdrive gdrive://<URL>`

dvc remote sending:

`dvc add data\dvc_data\raw_data\data.csv`\
`dvc push`

running dvc stage:

`dvc repro` 
`dvc repro <STAGE_NAME>`

## metrics and predicts 

[!](../dvc_artifacts/conflusion_matrix.png)

{"0": {"precision": 0.95857, "recall": 0.99492, "f1-score": 0.97641, "support": 42909.0}, 
"1": {"precision": 0.93249, "recall": 0.62006, "f1-score": 0.74484, "support": 4856.0}, 
"accuracy": 0.95681, "macro avg": {"precision": 0.94553, "recall": 0.80749, "f1-score": 0.86062, "support": 47765.0},
 "weighted avg": {"precision": 0.95592, "recall": 0.95681, "f1-score": 0.95287, "support": 47765.0}}
