import requests

from util.constants import LOG

class Jenkins:
    def __init__(self,url):
        self.base_url = url

    def get_artifacts(self, project, branch=None, min_build=0, status_filter=None):
        artifacts = []
        job = self.get_job_data(project, branch)
        build_numbers = get_build_numbers_from_job(job, min_build, status_filter)
        for build_num in build_numbers:
            try:
                build = self.get_build_data(project, branch, build_num)
                artifact_paths = get_artifact_paths_from_build(build)
                for artifact_path in artifact_paths:
                    try:
                        artifacts.append(self.get_artifact_data(project, branch, build_num, artifact_path))
                    except:
                        pass
            except:
                pass
        return artifacts


    def get_job_data(self, project, branch):
        job_url = "{BASE_URL}/{JOB_PATH}/api/json".format(
            BASE_URL=self.base_url, JOB_PATH=create_job_path(project,branch))
        try:
            LOG.debug("Retrieving list of Jenkins builds from {URL}".format(URL=job_url))
            response = requests.get(job_url)
            response.raise_for_status()
            return response.json()
        except Exception as err:
            LOG.error("Unexpected error when retrieving list of Jenkins builds")
            LOG.error(err)
            raise

    def get_build_data(self, project, branch, build_number=1):
        build_url = "{BASE_URL}/{JOB_PATH}/{BUILD_NUM}/api/json".format(
            BASE_URL=self.base_url, JOB_PATH=create_job_path(project,branch), BUILD_NUM=build_number)
        try:
            LOG.debug("Retrieving Jenkins JSON build data from {URL}".format(URL=build_url))
            response = requests.get(build_url)
            response.raise_for_status()
            return response.json()
        except Exception as err:
            LOG.error("Unexpected error when retrieving Jenkins build data")
            LOG.error(err)
            raise

    def get_artifact_data(self, project, branch, build_number, artifact_path):
        artifact_url = "{BASE_URL}/{JOB_PATH}/{BUILD_NUM}/artifact/{ARTIFACT}".format(BASE_URL=self.base_url,
            JOB_PATH=create_job_path(project,branch), BUILD_NUM=build_number, ARTIFACT=artifact_path)
        try:
            LOG.debug("Retrieving JSON artifact data from {URL}".format(URL=artifact_url))
            response = requests.get(artifact_url)
            response.raise_for_status()
            return response.json()
        except Exception as err:
            LOG.error("Unexpected error when retrieving Jenkins artifact")
            LOG.error(err)
            raise       

def create_job_path(project, branch):
    job_path = "job/{PROJ}".format(PROJ=project)
    if branch: job_path = "{PROJ_PATH}/job/{BRANCH}".format(PROJ_PATH=job_path, BRANCH=branch)
    return job_path

def get_build_numbers_from_job(job_dict, min_build=0, status_filter=None):
    build_numbers = []
    for build in job_dict.get('builds'):
        if build.get('number') >= min_build and (build.get('result') == status_filter if status_filter else True):
            build_numbers.append(build.get('number'))
    return build_numbers

def get_artifact_paths_from_build(build_dict):
    artifact_paths = []
    for artifact in build_dict.get('artifacts'):

        if artifact.get('relativePath').endswith('_benchmark.json'):
            artifact_paths.append(artifact.get('relativePath'))
    return artifact_paths

