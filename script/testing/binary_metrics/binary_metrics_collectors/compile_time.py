import os
import time
import subprocess

from binary_metrics.base_binary_metrics_collector import BaseBinaryMetricsCollector
from util.constants import DIR_REPO, LOG


class CompileTimeCollector(BaseBinaryMetricsCollector):
    def __init__(self, isDebug):
        super().__init__(isDebug)
        cmake_cmd = 'cmake -DCMAKE_BUILD_TYPE=Release -DTERRIER_USE_ASAN=OFF -DTERRIER_USE_JEMALLOC=ON -DTERRIER_BUILD_TESTS=OFF ..'
        make_cmd = 'make -j4 terrier'

        self._compile_commands = [cmake_cmd, make_cmd]

    def run_collector(self):
        start_time = time.perf_counter()
        try:
            for cmd in self._compile_commands:
                subprocess.run(cmd, cwd=self.build_path, shell=True, check=True, capture_output=(not self.isDebug))
        except subprocess.CalledProcessError as err:
            LOG.debug(err.stdout)
            LOG.error(err.stderr)
            return err.returncode

        end_time = time.perf_counter()
        self.metrics['compile_time_sec'] = end_time - start_time
        return 0
