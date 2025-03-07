from typing import List
import sys
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import  OneHotEncoder


class WeekdayImputer(BaseEstimator, TransformerMixin):
    """ Impute missing values in 'weekday' column by extracting dayname from 'dteday' column """

    def __init__(self, variables: list):

        if not isinstance(variables, list):
            raise ValueError("variables should be a list")

        self.variables = variables

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        # we need the fit statement to accomodate the sklearn pipeline
        #self.variables[0] = weekday
        
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        #self.variables[1] = dteday
        X = X.copy()
        wkday_null_idx=X[X[self.variables[0]].isnull() == True].index
        X.loc[wkday_null_idx, self.variables[0]] = X.loc[wkday_null_idx, self.variables[1]].dt.day_name().apply(lambda x: x[:3])
        print("Weekday Imputer")
        print(X.weekday.isnull().sum())
        print(X.weekday.value_counts())
        return X


class WeathersitImputer(BaseEstimator, TransformerMixin):
    """ Impute missing values in 'weathersit' column by replacing them with the most frequent category value """

    def __init__(self, variables: list):
        if not isinstance(variables, list):
            raise ValueError("variables should be a list")

        self.variables = variables
        self.fill_val = 'Clear'

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
      #X_train['weathersit'].mode()[0]
      print(self.variables[0])
      self.fill_val = X[self.variables[0]].mode()[0]
      return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        X[self.variables]=X[self.variables].fillna(self.fill_val)       
        return X
    
class Mapper(BaseEstimator, TransformerMixin):
    """
    Ordinal categorical variable mapper:
    Treat column as Ordinal categorical variable, and assign values accordingly
    """

    def __init__(self, variables: str, mappings: dict):

        if not isinstance(variables, str):
            raise ValueError("variables should be a str")

        self.variables = variables
        self.mappings = mappings

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        # we need the fit statement to accomodate the sklearn pipeline        
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        #for feature in self.variables:
        #  print(f"Dtype of {self.variables} is {X[self.variables].dtype}")      
        X[self.variables] = X[self.variables].map(self.mappings).astype(str)
        if self.variables == 'yr': 
            #print the dtype of the yr column
            print(f"Dtype of {self.variables} is {X[self.variables].dtype}")
            #print the value counts of the new features
            print(f"Value counts for {self.variables}")
            print(X[self.variables].value_counts())
        return X
    
class OutlierHandler(BaseEstimator, TransformerMixin):
    """
    Change the outlier values:
        - to upper-bound, if the value is higher than upper-bound, or
        - to lower-bound, if the value is lower than lower-bound respectively.
    """

    def __init__(self, variables: str):

        if not isinstance(variables, str):
            raise ValueError("variables should be a str")

        self.variables = variables

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        q1 = X.describe()[self.variables].loc['25%']
        q3 = X.describe()[self.variables].loc['75%']
        iqr = q3 - q1
        self.lower_bound = q1 - (1.5 * iqr)
        self.upper_bound = q3 + (1.5 * iqr)
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        for i in X.index:
          if X.loc[i,self.variables] > self.upper_bound:
              X.loc[i,self.variables]= self.upper_bound
          if X.loc[i,self.variables] < self.lower_bound:
              X.loc[i,self.variables]= self.lower_bound

        return X

class WeekdayOneHotEncoder(BaseEstimator, TransformerMixin):
    """ One-hot encode weekday column """

    def __init__(self, variables: str):

        if not isinstance(variables, str):
            raise ValueError("variables should be a str")

        self.variables = variables

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        self.encoder = OneHotEncoder(sparse_output=False)
        self.encoder.fit(X[[self.variables]])
        return self

    def transform(self, X: pd.DataFrame):
       X = X.copy()
       encoded_weekday = self.encoder.transform(X[[self.variables]])
       enc_wkday_features = self.encoder.get_feature_names_out([self.variables])
       X[enc_wkday_features] = encoded_weekday
       return X
    
# Define a custom transformer to drop columns
class ColumnDropper(BaseEstimator, TransformerMixin):
    def __init__(self, columns:list):
        if not isinstance(columns, list):
            raise ValueError("variables should be a list")
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # Drop specified columns from the DataFrame
        X = X.drop(columns=self.columns,axis=1)
        print(X.info())
        print(X.head())
        return X