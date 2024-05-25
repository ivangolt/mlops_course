# ClearML report 

This task locate in branch [clearML](https://gitlab.com/ivan_golt/mlops_course/-/tree/clear_ml?ref_type=heads)

In this task, the clearML functionality was used to track experiments in ml.

A comparative machine learning task was performed to classify reviews from the toxic comments dataset (classification task).

## Preparing the environment

for poetry: `poetry add clearml`
for mamba: `mamba create -y -n clearml python=3.10.14 numpy pandas polars clearml scikit-learn matplotlib pytorch transformers hydra-core omegaconf ipykernel jupyter`

## Deployment clearML

1) using docker-compose: use [docker-compose.yaml](clear_ml_infrastucture/docker-compose.yaml) and run docker-compose up -d

then add credential in clearML server cope credentials and after in local machine start:
`clearml-init` 
and then add credentials to clearml.conf
[!](docs/clearml_artifacts/clearml init.png)

2) using saas: use for this credentials from clerml from web and update or add new credentials in clearml.conf

## Tracking experiments

1) To start working with ClearML initiate a new session:

```task = Task.init(project_name=projec_name, 
    task_name=TASK_NAME, 
    output_uri=True)
```
This code create project and task in clearML server.

if you want to create new task use new task name.


2) Uploading the dataset to the ClearML cloud with parameters that will then be used in notebooks:

clearml-data create --project "project_name" --name "dataset_name"
clearml-data add --files datad/train.csv
clearml-data close

3) Download from cloud 

```# initialize ClearML tracking
task = Task.init(project_name=cfg.project.name, task_name=TASK_NAME, output_uri=True)

# initialize local version of dataset

dataset = Dataset.get(
    dataset_project=cfg.dataset.project, dataset_name=cfg.dataset.name
).get_local_copy()

task.set_progress(0)
```
4) uploading artifacts

```# fixing artifacts
task.upload_artifact(name="TfidfVectorizer", artifact_object=pickle.dumps(tfidf_vectorizer))

task.upload_artifact(
    name="train_features",
    artifact_object=(train_features, train["toxic"].to_numpy()),
)

task.upload_artifact(
    name="test_features",
    artifact_object=(test_features, test["toxic"].to_numpy()),
)
```
[!](docs/clearml_artifacts/artifacts.png)

5) logging metrics 

```# Fix progress in CLearML
task.set_progress(95)

# Fix parameters of model
logger = task.get_logger()

logger.report_single_value("Accuracy", report.pop("accuracy"))

for class_name, metrics in report.items():
    for metric, value in metrics.items():
        logger.report_single_value(f"{class_name}_{metric}", value)
```
[!](docs/clearml_artifacts/metrics.png)

Also you can upload plots, for example confusion_matrix

[!](docs/clearml_artifacts/plots.png)

6) After all code runs you need to stop task

`task.close()`

## Compare two experiments

In this task was compare two variants of embeddings 1)tf-idf, 2)BERT, and then fitting on them model of Logistic Regression.

TF-IDf embeddings was fitted on local machine, and BERT model was fitted in Google Colab using ClearML Agent.

In clearML server we have 2 completed runs with artifacts, metrics and plots.
[!](docs/clearml_artifacts/completed work.png)

Also we can compare logged metrics:
[!](docs/clearml_artifacts/metrics.png)

and plots:
[!](docs/clearml_artifacts/plots.png)