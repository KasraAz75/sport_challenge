import yaml
import argparse
import pandas as pd
from sqlalchemy import create_engine

def read_params(config_path):
    """
    read parameters from the params.yaml file
    input: params.yaml location
    output: parameters as dictionary
    """
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def read_query(quer_path):
    with open(quer_path, "r") as file:
        sql_query = file.read()
    return sql_query

def query_db(config_path):

    config=read_params(config_path)
    db_uri = config["raw_data_config"]["db_uri"]
    query = read_query(config["raw_data_config"]["data_model"])
    raw_data = config["raw_data_config"]["raw_data_csv"]

    conn = create_engine(db_uri)
    df = pd.read_sql(
        query,
        con=conn
    )
    df.to_csv(raw_data, index=False)

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    query_db(config_path=parsed_args.config)