import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))


import pandas as pd
from bikeshare_model.processing.features import WeekdayImputer, WeathersitImputer, Mapper, OutlierHandler, WeekdayOneHotEncoder
from bikeshare_model.config.core import config

# test the WeekdayImputer with sample_input_data
def test_weekday_imputer(sample_input_data):
    
    # Create a WeekdayImputer instance
    imputer = WeekdayImputer(variables=[config.model_config_.weekday_var, config.model_config_.dteday_var])

    # convert 'dteday' column to Datetime datatype
    sample_input_data[0]['dteday'] = pd.to_datetime(sample_input_data[0]['dteday'], format='%Y-%m-%d')

    # Fit the imputer on the sample data
    imputer.fit(sample_input_data[0])
    # Transform the sample data
    transformed_data = imputer.transform(sample_input_data[0])
    # Check that the transformed data has no missing values in the weekday column
    assert transformed_data['weekday'].isnull().sum() == 0

# test the WeathersitImputer with sample_input_data
def test_weathersit_imputer(sample_input_data):
    # Create a WeathersitImputer instance
    imputer = WeathersitImputer(variables=[config.model_config_.weathersit_var])
    # Fit the imputer on the sample data
    imputer.fit(sample_input_data[0])
    # Transform the sample data
    transformed_data = imputer.transform(sample_input_data[0])
    # Check that the transformed data has no missing values in the weathersit column
    assert transformed_data['weathersit'].isnull().sum() == 0

