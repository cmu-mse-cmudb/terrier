#!/usr/bin/python3

import requests
from oltpbench.reporting.parse_data import parse_data
from oltpbench.constants import PERFORMANCE_STORAGE_SERVICE_API

def report(results_dir, query_mode='simple'):
    metadata, timestamp, type, parameters, metrics = parse_data(results_dir)
    parameters['query_mode'] = query_mode

    results = {
        'metadata': metadata,
        'timestamp': timestamp,
        'type': type,
        'parameters': parameters,
        'metrics': metrics
    }
    
    send_results(results)


def send_results(results):
    result = requests.post(PERFORMANCE_STORAGE_SERVICE_API + '/oltpbench/', json=results)
    result.raise_for_status()
