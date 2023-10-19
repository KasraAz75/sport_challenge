import yaml
import argparse
import pandas as pd

def read_params(config_path):
    """
    read parameters from the params.yaml file
    input: params.yaml location
    output: parameters as dictionary
    """
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def team_popularity_calculator(raw_data_path, df_popularity_score):
    """Adds popularity score to the raw data frame"""
    updated_df_raw = pd.merge(raw_data_path, df_popularity_score, left_on='home_team', right_on='team', how='left')
    updated_df_raw.rename(columns={'popularity_score': 'home_team_popularity'}, inplace=True)

    updated_df_raw = pd.merge(updated_df_raw, df_popularity_score, left_on='away_team', right_on='team', how='left')
    updated_df_raw.rename(columns={'popularity_score': 'away_team_popularity'}, inplace=True)

    updated_df_raw.drop(['home_team', 'away_team', 'team_x', 'team_y'], axis=1, inplace=True)
    return updated_df_raw

def feature_eng(config_path):
    """
    apply feature engineering and selection, then create the pipeline for data injestion
    """
    config = read_params(config_path)
    raw_data_path = config["raw_data_config"]["raw_data_csv"]
    df_popularity_score_path = config["feature_engineering_config"]["team_popularity_df_path"]
    interim_data_csv = config["feature_engineering_config"]["interim_data_csv"]

    raw_df = pd.read_csv(raw_data_path)
    df_popularity_score = pd.read_csv(df_popularity_score_path)
    updated_raw_df = team_popularity_calculator(raw_df, df_popularity_score)
    updated_raw_df.to_csv(interim_data_csv, index=False)  

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    feature_eng(config_path=parsed_args.config)