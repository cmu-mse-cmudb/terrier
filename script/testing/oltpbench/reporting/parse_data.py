#!/usr/bin/python3

import os
from oltpbench.reporting.parsers.config_parser import parse_config_file
from oltpbench.reporting.parsers.summary_parser import parse_summary_file

def parse_data(results_dir):
    env_metadata = parse_jenkins_env_vars()
    files_metadata, timestamp, type, parameters, metrics = parse_files(results_dir)
    metadata = {**env_metadata, **files_metadata}
    return metadata, timestamp, type, parameters, metrics


def parse_jenkins_env_vars():
    build_id = os.environ['BUILD_ID']
    git_branch = os.environ['GIT_BRANCH']
    commit_id = os.environ['GIT_COMMIT']
    metadata = {
        'jenkins': {
            'build_id': build_id
        },
        'github': {
            'branch': git_branch,
            'commit_id': commit_id
        }
    }
    return metadata

def parse_files(results_dir):
    """
    Parse information from the config and summary files

    Args:
        results_dir (str): The location of directory where the oltpbench results are stored.
        
    Returns:
        metadata (dict): An object containing metadata information.
        timestamp (int): The timestamp when the benchmark was created in milliseconds.
        type (str): The type of OLTPBench test it was (tatp, noop, etc.)
        parameters (dict): Information about the parameters with which the test was run.
        metrics (dict): The summary measurements that were gathered from the test.
    """
    config_parameters = parse_config_file(results_dir+'/oltpbench.expconfig')
    metadata, timestamp, type, summary_parameters, metrics  = parse_summary_file(results_dir+'/oltpbench.summary')
    parameters = {**summary_parameters,**config_parameters}
    return metadata, timestamp, type, parameters, metrics
