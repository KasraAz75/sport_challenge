import yaml
import argparse
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset

def read_params(config_path):
    """
    read parameters from the params.yaml file
    input: params.yaml location
    output: parameters as dictionary
    """
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def model_monitoring(config_path):
    config = read_params(config_path)
    processed_data_path = config["processed_data_config"]["processed_data_csv"]
    target = config["processed_data_config"]["target"]
    monitor_dashboard_path = config["model_monitor"]["monitor_dashboard_html"]
    monitor_target = config["model_monitor"]["target_col_name"]

    dataset = pd.read_csv(processed_data_path)
    ref = dataset.sample(n=100, replace=False)
    cur = dataset.sample(n=100, replace=False)

    ref = ref.rename(columns ={target:monitor_target}, inplace = False)
    cur = cur.rename(columns ={target:monitor_target}, inplace = False)
    
    report = Report(metrics=[DataDriftPreset(), TargetDriftPreset(),])
    report.run(reference_data=ref, current_data=cur)
    report.save_html(monitor_dashboard_path)

if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    model_monitoring(config_path=parsed_args.config)