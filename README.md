## Introduction

This repository contains the code and configurations for tuning, training and evaluating a binary classification model using scikit-learn's Random Forest Classifier. The model includes functionality for hyperparameter tuning using scikit-optimize. This project is designed to be modular, easy to understand, and easy to use.

Unit tests are included for all the functions in the code.
Integration tests are included for the overall training and prediction workflows.
Performance test is included for the training and prediction workflows.

This repository is part of a tutorial series on Ready Tensor, a web platform for AI developers and users.

## Repository Contents

```bash
binary_class_project/
├── examples/
│   ├── titanic_schema.json
│   ├── titanic_train.csv
│   └── titanic_test.csv
├── inputs/
│   ├── data/
│   │   ├── testing/
│   │   └── training/
│   └── schema/
├── model/
│   └── artifacts/
├── outputs/
│   ├── errors/
│   ├── hpt_outputs/
│   └── predictions/
├── src/
│   ├── config/
│   │   ├── default_hyperparameters.json
│   │   ├── hpt.json
│   │   ├── model_config.json
│   │   ├── paths.py
│   │   └── preprocessing.json
│   ├── data_models/
│   ├── hyperparameter_tuning/
│   │   ├── __init__.json
│   │   └── tuner.py
│   ├── prediction/
│   │   ├── __init__.json
│   │   └── predictor_model.py
│   ├── preprocessing/
│   │   ├── custom_transformers.py
│   │   ├── pipeline.py
│   │   ├── preprocess.py
│   │   └── target_encoder.py
│   ├── schema/
│   │   └── data_schema.py
│   ├── xai/
│   ├── predict.py
│   ├── train.py
│   └── utils.py
├── tests/
│   ├── integration_tests/
│   ├── performance_tests/
│   └── unit_tests/
│       ├── <mirrors /src structure>
│       └── ...
├── tmp/
├── .gitignore
├── LICENSE
├── pytest.ini
├── README.md
├── requirements.txt
└── requirements-test.txt
```

- **`/examples`**: This directory contains example files for the titanic dataset. Three files are included: `titanic_schema.json`, `titanic_train.csv` and `titanic_test.csv`. You can place these files in the `inputs/schema`, `inputs/data/training` and `inputs/data/testing` folders, respectively.
- **`/inputs`**: This directory contains all the input files for your project, including the data and schema files. The data is further divided into testing and training subsets.
- **`/model/artifacts`**: This directory is used to store the model artifacts, such as trained models and their parameters.
- **`/outputs`**: The outputs directory contains sub-directories for error logs, and hyperparameter tuning outputs, and prediction results. Note that model artifacts should not be saved in this directory. Instead, they should be saved in the `/model/artifacts` directory.
- **`/src`**: This directory holds the source code for the project. It is further divided into various subdirectories such as `config` for configuration files, `data_models` for data models for input validation, `hyperparameter_tuning` for hyperparameter-tuning (HPT) related files, `prediction` for prediction model scripts, `preprocessing` for data preprocessing scripts, `schema` for schema scripts, and `xai` for explainable AI scripts.
  - The config file called `hpt.json` in the path `src/config/` is used to specify the tuning specifications for each of the hyperparameters. These specifications are used by the tuner to determine the search space for each hyperparameter.
  - The configuration file called `default_hyperparameters.json` in the path `src/config/` is used to specify the default hyperparameters for the model. These hyperparameters are used when the model is trained without hyperparameter tuning. The default hyperparameters are also used as the starting point for the hyperparameter tuning process.
  - The script called `tuner.py` under `src/hyperparameter_tuning` is used to implement the scikit-optimize tuner.
- **`/tests`**: This directory contains all the tests for the project. It contains sub-directories for specific types of tests such as unit tests, integration tests, and performance tests. For unit tests, the directory structure mirrors the `/src` directory structure.
- **`/tmp`**: This directory is used for storing temporary files which are not necessary to commit to the repository.
- **`.gitignore`**: This file specifies the files and folders that should be ignored by Git.
- **`LICENSE`**: This file contains the license for the project.
- **`README.md`**: This file contains the documentation for the project, explaining how to set it up and use it.
- **`requirements.txt`**: This file lists the dependencies for the project, making it easier to install all necessary packages.

## Usage

- Create your virtual environment and install dependencies listed in `requirements.txt`.
- Move the three example files (`titanic_schema.json`, `titanic_train.csv` and `titanic_test.csv`) into the `inputs/schema`, `inputs/data/training` and `inputs/data/testing` folders, respectively.
- Run the `src/train.py` script to train the model, with `--tune` or `-t` flag for hyperparameter tuning. If the flag is not provided, the model will be trained with default hyperparameters. This will save the model artifacts, including the preprocessing pipeline and label encoder, in the path `./model/artifacts/`. When tuning is requested, the hyperparameter tuning results will be saved in a file called `hpt_results.csv` in the path `./outputs/hpt_outputs/`. The best hyperparameters are used in the trained model.
- Run the script `src/predict.py` to run test predictions using the trained model. This script will load the artifacts and create and save the predictions in a file called `predictions.csv` in the path `./outputs/predictions/`.

## Requirements

Dependencies are listed in the file `requirements.txt`. These packages can be installed by running the following command:

```python
pip install -r requirements.txt
```

For testing, dependencies are listed in the file `requirements-test.txt`. You can install these packages by running the following command:

```python
pip install -r requirements-test.txt
```
