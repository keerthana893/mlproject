'''
MAIN PURPOSE:
To do feature engg,data cleaning,changing categorical features into numerical features.
'''
import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer # to create pipeline(ohe,standard scaling)
from sklearn.impute import SimpleImputer   # for missing values


from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
import os
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifact',"preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self):
        '''this function is responsible for data transformation'''
        try:
            numerical_columns=["writing_score","reading_score"]
            categorical_columns=[
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course"
            ]

            num_pipeline = Pipeline(   # creating pipeline
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),  # imputer is for handling missing values inside pipeline
                    ("scalar",StandardScaler())
                ])
             
            cat_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder(handle_unknown="ignore")),
                    ("scalar",StandardScaler(with_mean=False))
                ]
            )

            logging.info("Numerical column :{numerical_columns}")
            logging.info("Categorical column:{categorical_columns} ")
        
        # combining numerical pipeline with categorical pipeline--using column transformer

            preprocessor=ColumnTransformer([
            ("num_pipeline",num_pipeline,numerical_columns),
            ("cat_pipeline",cat_pipeline,categorical_columns)
            ])


            return preprocessor


        except Exception as e:
            raise CustomException (e,sys)



    # starting data transformation technique.
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("read train and test data completely")
            logging.info("obtaining preprocessing object")
            preprocessing_obj=self.get_data_transformer_object()
            target_column_name="math_score"
            numerical_columns=["writing_score","reading_score"]
            categorical_columns=[
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course"]

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)  
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)  
            target_feature_test_df=test_df[target_column_name]  

            logging.info(f'Applying preprocessor  object on training dataframe and tesing dataframe')

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr=np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr=np.c_[input_feature_test_arr,np.array(target_feature_test_df)]
            logging.info(f'Saved preprocessing object.')

            save_object(file_path=self.data_transformation_config.preprocessor_obj_file_path,
                        obj=preprocessing_obj)
            
            
            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
        
        except Exception as e:
            raise CustomException(e,sys)

            





































