import yaml
import argparse
import pandas as pd
from load_data import read_params
from sklearn.model_selection import train_test_split

def split_data(df,train_data_path,test_data_path,split_ratio, random_state):
    train, test = train_test_split(df, test_size=split_ratio, shuffle=True, random_state=random_state)
    train.to_csv(train_data_path, index=False)
    test.to_csv(test_data_path,  index=False)    

def split_and_saved_data(config_path):
    """
    split the train dataset(data/raw) and save it in the data/processed folder
    input: config path 
    output: save splitted files in output folder
    """
    config = read_params(config_path)
    processed_data_csv = config["processed_data_config"]["processed_data_csv"]
    test_data_path = config["split_data_config"]["test_data_csv"] 
    train_data_path = config["split_data_config"]["train_data_csv"]
    split_ratio = config["split_data_config"]["train_test_split_ratio"]
    random_state = config["split_data_config"]["random_state"]
    
    raw_df=pd.read_csv(processed_data_csv)
    split_data(raw_df,train_data_path,test_data_path,split_ratio, random_state)
    
if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    split_and_saved_data(config_path=parsed_args.config)