import yaml
import argparse
import pandas as pd
from sklearn.impute import KNNImputer
from load_data import read_params

def feature_extractor(df, model_features):
    """Extract model features"""
    return df[model_features]

def percentile_cutoffs(df, target, percentile_feature):
    """
    It calculates the 0.01 quantile of the 'handle' column for each unique 'time_slot and drop them
    """
    # Calculate the 0.01 quantile for each time_slot
    df_percentile_cutoffs = df[[target, percentile_feature]].groupby(by=percentile_feature).quantile(0.1).reset_index()
    df_merged = df.merge(df_percentile_cutoffs, on=percentile_feature)
    df_processed = df_merged[df_merged[f'{target}_x'] > df_merged[f'{target}_y']].drop(columns=['handle_y'])
    df_processed = df_processed.rename(columns={f'{target}_x':target})
    df_processed = df_processed.reset_index(drop=True)

    return df_processed

def imputer(df, imputer_rows):
    """
    Impute missing values using KNN Imputer 
    """
    imputer = KNNImputer(n_neighbors=5)
    df[imputer_rows] = imputer.fit_transform(df[imputer_rows])

    return df

def one_hot_encoding(df, cat_features):
    """
    apply one hot encoding to columns with categorical values
    input: raw dataframe and columns
    output: processed raw dataframe 
    """
    return pd.get_dummies(df, columns=cat_features, dtype=int)

def apply_preprocessing(config_path):
    """apply preprocessing to dataframe"""
    config = read_params(config_path)
    interim_data_path = config["feature_engineering_config"]["interim_data_csv"]
    processed_data_csv = config["processed_data_config"]["processed_data_csv"]

    model_features = config["processed_data_config"]["model_features"]
    target = config["processed_data_config"]["target"] 
    percentile_feature = config["processed_data_config"]["percentile_feature"]
    imputer_rows = config["processed_data_config"]["imputer_rows"]
    cat_features = config["processed_data_config"]["cat_features"]
    
    interim_data_path = pd.read_csv(interim_data_path)
    model_features = feature_extractor(interim_data_path, model_features)
    percentile_cutoffs_df = percentile_cutoffs(model_features, target, percentile_feature)
    imputer_df = imputer(percentile_cutoffs_df, imputer_rows)
    one_hot_encoding_df = one_hot_encoding(imputer_df, cat_features)

    one_hot_encoding_df.to_csv(processed_data_csv, index=False)    


if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    apply_preprocessing(config_path=parsed_args.config)
