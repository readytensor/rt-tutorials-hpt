from typing import List, Union, Any
import joblib
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class CustomTargetEncoder(BaseEstimator, TransformerMixin):
    """ Binarizes the target variable to 0/1 values."""
    def __init__(self, target_field:str, allowed_values: List[str]) -> None:
        """
        Initializes a new instance of the `CustomTargetEncoder` class.

        Order of the classes in allowed_values matter.
        allowed_values[0] is encoded as 0, and
        allowed_values[1] is encoded as 1 (i.e. treated as positive class)

        Args:
            target_field: str
                Name of the target field.
            allowed_values: List[str]
                Class labels in a list.
        """
        self.target_field = target_field
        self.classes_ = [str(c) for c in allowed_values]
        self.class_encoding = {self.classes_[0]:0, self.classes_[1]:1}

    def fit(self, data):
        """
        No-op.

        Returns:
            self
        """
        return self

    def transform(self, data):
        """
        Transform the data.

        Args:
            data: pandas DataFrame - data to transform
        Returns:
            transformed data as a pandas Series if target is present in data, else None
        """
        if self.target_field in data.columns:
            targets = data[self.target_field].astype(str)
            observed_classes = set(targets)
            if len(observed_classes) != 2:
                raise ValueError(f"Expected two classes {self.classes_}. Found {len(observed_classes)} class in given target classes: {list(observed_classes)}")
            if len(observed_classes.intersection(self.classes_)) != 2:
                raise ValueError(f"Observed classes in target {list(observed_classes)} do not match given allowed values for target: {self.classes_}")
            transformed_targets = targets.apply(str).map(self.class_encoding)
        else:
            transformed_targets = None
        return transformed_targets


def get_target_encoder(
        data_schema: Any) -> 'CustomTargetEncoder':
    """Create a TargetEncoder using the data_schema.

    Args:
        data_schema (Any): An instance of the BinaryClassificationSchema.

    Returns:
        A TargetEncoder instance.
    """
    # Create a target encoder instance
    encoder = CustomTargetEncoder(
        target_field=data_schema.target,
        allowed_values=data_schema.allowed_target_values)
    return encoder



def train_target_encoder(
        target_encoder: CustomTargetEncoder,
        train_data: pd.DataFrame) -> CustomTargetEncoder:
    """Train the target encoder using the given training data.

    Args:
        target_encoder (CustomTargetEncoder): A target encoder instance.
        train_data (pd.DataFrame): The training data as a pandas DataFrame.

    Returns:
        A fitted target encoder instance.
    """
    # Fit the target encoder on the training data
    target_encoder.fit(train_data)
    return target_encoder


def transform_targets(target_encoder: CustomTargetEncoder, 
                      data: Union[pd.DataFrame, np.ndarray]) -> pd.Series:
    """Transform the target values using the fitted target encoder.

    Args:
        target_encoder (CustomTargetEncoder): A fitted target encoder instance.
        data (pd.DataFrame): The data as a pandas DataFrame.

    Returns:
        The transformed target values as a pandas Series.
    """
    # Transform the target values
    transformed_targets = target_encoder.transform(data)
    return transformed_targets


def save_target_encoder(target_encoder: CustomTargetEncoder, file_path_and_name: str) -> None:
    """Save a fitted label encoder to a file using joblib.

    Args:
        target_encoder (CustomTargetEncoder): A fitted target encoder instance.
        file_path_and_name (str): The filepath to save the LabelEncoder to.
    """
    joblib.dump(target_encoder, file_path_and_name)

def load_target_encoder(file_path_and_name: str) -> CustomTargetEncoder:
    """Load the fitted target encoder from the given path.

    Args:
        file_path_and_name: Path to the saved target encoder.

    Returns:
        Fitted target encoder.
    """
    return joblib.load(file_path_and_name)


if __name__ == "__main__":
    df = pd.DataFrame()
    target_encoder = CustomTargetEncoder(
        target_field="target", allowed_values=["A", "B"])
    result = target_encoder.fit_transform(df)
    print(result)
    print(type(result))

    # expected = pd.Series({"target": [1, 0, 1, 0]})
    # print(type(expected), "expected")
    # print(expected)