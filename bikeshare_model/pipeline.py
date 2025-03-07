import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

from bikeshare_model.config.core import config
from bikeshare_model.processing.features import WeekdayImputer
from bikeshare_model.processing.features import WeathersitImputer
from bikeshare_model.processing.features import Mapper
from bikeshare_model.processing.features import OutlierHandler
from bikeshare_model.processing.features import WeekdayOneHotEncoder
from bikeshare_model.processing.features import ColumnDropper



bikeshare_pipe=Pipeline([

    #variables = ['weekday','dteday']
    ('weekday_imputation', WeekdayImputer(variables = [config.model_config_.weekday_var, config.model_config_.dteday_var])),
    ('Weathersit_imputation', WeathersitImputer(variables = [config.model_config_.weathersit_var])),
    
    #('map_yr',Mapper('yr',{2011: 0, 2012: 1})),
    ('map_yr',Mapper(config.model_config_.yr_var,config.model_config_.yr_mappings)),
    #map_mnth
    ('map_mnth',Mapper(config.model_config_.mnth_var,config.model_config_.mnth_mappings)),
    #map_season
    ('map_season',Mapper(config.model_config_.season_var,config.model_config_.season_mappings)),
    #map_weathersit
    ('map_weathersit',Mapper(config.model_config_.weathersit_var,config.model_config_.weathersit_mappings)),
    #map_holiday
    ('map_holiday',Mapper(config.model_config_.holiday_var,config.model_config_.holiday_mappings)),
    #map_workingday
    ('map_workingday',Mapper(config.model_config_.workingday_var,config.model_config_.workingday_mappings)),
    #map_hr
    ('map_hr',Mapper(config.model_config_.hr_var,config.model_config_.hr_mappings)),

    #handle outliers
    ('hum_outlier_handler', OutlierHandler(config.model_config_.hum_var)),
    ('windspeed_outlier_handler', OutlierHandler(config.model_config_.windspeed_var)),

    #weekday encoder
    ('weekday_encoder', WeekdayOneHotEncoder(config.model_config_.weekday_var)),    
    
    #drop columns
    ('drop_dteday', ColumnDropper(columns=[config.model_config_.dteday_var, config.model_config_.weekday_var])),

    # scale
     ("scaler", StandardScaler()),
     ('model_rf', RandomForestRegressor(n_estimators=config.model_config_.n_estimators, 
                                         max_depth=config.model_config_.max_depth,
                                         random_state=config.model_config_.random_state))
          
     ])
