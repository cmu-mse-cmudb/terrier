#!/usr/bin/python3
import os
import sys
import subprocess
import json
import traceback
import shutil
from util.constants import ErrorCode
from util.constants import LOG
from util.common import run_command
from util.test_server import TestServer
from xml.etree import ElementTree
from oltpbench import constants


class TestOLTPBench(TestServer):
    """ Class to run OLTP Bench tests """
    def __init__(self, args):
        TestServer.__init__(self, args)

    def run_pre_suite(self):
        self.install_oltp()

    def install_oltp(self):
        self.clean_oltp()
        self.download_oltp()
        self.build_oltp()

    def clean_oltp(self):
        rc, stdout, stderr = run_command(constants.OLTPBENCH_GIT_CLEAN_COMMAND,
                                         "Error: unable to clean OLTP repo")
        if rc != ErrorCode.SUCCESS:
            LOG.error(stderr)
            sys.exit(rc)

    def download_oltp(self):
        # rc, stdout, stderr = run_command(
        #     constants.OLTPBENCH_GIT_COMMAND,
        #     "Error: unable to git clone OLTP source code")
        # run_command(constants.OLTPBENCH_GIT_CHECKOUT)
        # if rc != ErrorCode.SUCCESS:
        #     LOG.error(stderr)
        #     sys.exit(rc)

        # clone the repo
        rc, stdout, stderr = run_command(
            constants.OLTPBENCH_GIT_COMMAND,
            error_msg="Error: unable to git clone OLTP source code")
        if rc != ErrorCode.SUCCESS:
            LOG.error(stderr)
            sys.exit(rc)

        # checkout the branch
        rc, stdout, stderr = run_command(
            constants.OLTPBENCH_GIT_CHECKOUT,
            cwd=constants.OLTPBENCH_GIT_LOCAL_PATH)
        if rc != ErrorCode.SUCCESS:
            LOG.error(stderr)
            sys.exit(rc)

    def build_oltp(self):
        for command in constants.OLTPBENCH_MVN_COMMANDS:
            rc, stdout, stderr = run_command(
                command, cwd=constants.OLTPBENCH_GIT_LOCAL_PATH)
            if rc != ErrorCode.SUCCESS:
                LOG.error(stderr)
                sys.exit(rc)
