'''
Talk to Concourse via the REST API.
See https://github.com/concourse/concourse/blob/master/atc/routes.go for all possible routes
'''

from datetime import datetime
from pprint import pprint
import json
import requests


class API:
    '''
    Talk to Concourse via the REST API
    Regular output of the methods is in JSON (dict) format
    '''

    def __init__(self, url, username, password, team_name='main'):
        ''' Initialise variables and authenticate at Concourse '''
        self._username = username
        self._password = password
        self._headers = {}
        self._token = ''
        self._team_name = team_name
        self._url = url
        self._expires = 0
        self._authenticate()

    def get_info(self):
        ''' Get Concourse version information '''
        path = '/api/v1/info'
        return self._get(path)

    # ### Builds ####
    def list_builds(self):
        ''' List all builds '''
        path = '/api/v1/builds'
        return self._get(path)

    def get_build(self, build_id):
        ''' Get specific build '''
        path = '/api/v1/builds/{!s}'.format(build_id)
        return self._get(path)

    def get_build_plan(self, build_id):
        ''' Get specific build plan '''
        path = '/api/v1/builds/{!s}/plan'.format(build_id)
        return self._get(path)

    def build_events(self, build_id):
        ''' Get build events '''
        path = '/api/v1/builds/{!s}/events'.format(build_id)
        return self._get(path)

    def build_resources(self, build_id):
        ''' Get build resources '''
        path = '/api/v1/builds/{!s}/resources'.format(build_id)
        return self._get(path)

    def abort_build(self, build_id):
        ''' Abort a build '''
        path = '/api/v1/builds/{!s}/abort'.format(build_id)
        return self._put(path)

    def get_build_preparation(self, build_id):
        ''' Get build preparation '''
        path = '/api/v1/builds/{!s}/preparation'.format(build_id)
        return self._get(path)

    def get_build_artifacts(self, build_id):
        ''' Get build artifacts '''
        path = '/api/v1/builds/{!s}/artifacts'.format(build_id)
        return self._get(path)

    # ### Jobs ####
    def list_all_jobs(self):
        ''' List all jobs '''
        path = '/api/v1/jobs'
        return self._get(path)

    def list_jobs(self, pipeline_name, team_name=''):
        ''' List jobs of a specific pipeline '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/pipelines/{!s}/jobs'.format(team_name, pipeline_name)
        return self._get(path)

    def get_job(self, pipeline_name, job_name, team_name=''):
        ''' Get a job from a pipeline '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/pipelines/{!s}/jobs/{!s}'.format(team_name, pipeline_name, job_name)
        return self._get(path)

    def list_job_builds(self, pipeline_name, job_name, team_name=''):
        ''' List job builds '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/pipelines/{!s}/jobs/{!s}/builds'.format(team_name, pipeline_name, job_name)
        return self._get(path)

    def create_job_build(self, pipeline_name, job_name, team_name=''):
        ''' Start a job build '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/pipelines/{!s}/jobs/{!s}/builds'.format(team_name, pipeline_name, job_name)
        return self._post(path)

    def list_job_inputs(self, pipeline_name, job_name, team_name=''):
        ''' List inputs of a job '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/pipelines/{!s}/jobs/{!s}/inputs'.format(team_name, pipeline_name, job_name)
        return self._get(path)

    def get_job_build(self, pipeline_name, job_name, build_name, team_name=''):
        ''' Get all builds of a job '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/pipelines/{!s}/jobs/{!s}/builds/{!s}'.format(
            team_name, pipeline_name, job_name, build_name)
        return self._get(path)

    def pause_job(self, pipeline_name, job_name, team_name=''):
        ''' Pause a job '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/pipelines/{!s}/jobs/{!s}/pause'.format(team_name, pipeline_name, job_name)
        return self._put(path)

    def unpause_job(self, pipeline_name, job_name, team_name=''):
        ''' Un-pause a job '''
        path = '/api/v1/teams/{!s}/pipelines/{!s}/jobs/{!s}/unpause'.format(team_name, pipeline_name, job_name)
        if not team_name:
            team_name = self._team_name
        return self._put(path)

    def job_badge(self, pipeline_name, job_name, team_name=''):
        ''' Get job badge '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/pipelines/{!s}/jobs/{!s}/badge'.format(team_name, pipeline_name, job_name)
        return self._get(path)

    def main_job_badge(self, pipeline_name, job_name):
        ''' Get main job badge '''
        path = '/api/v1/pipelines/{!s}/jobs/{!s}/badge'.format(pipeline_name, job_name)
        return self._get(path)

    # ### Pipelines ####
    def get_config(self, pipeline_name, team_name=''):
        ''' Get pipeline configuration '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/pipelines/{!s}/config'.format(team_name, pipeline_name)
        return self._get(path)

    def list_pipelines(self):
        ''' List all pipelines '''
        path = '/api/v1/pipelines'
        return self._get(path)

    def get_pipeline(self, pipeline_name, team_name=''):
        ''' Get a pipeline '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/pipelines/{!s}'.format(team_name, pipeline_name)
        return self._get(path)

    def pause_pipeline(self, pipeline_name, team_name=''):
        ''' Pause a pipeline '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/pipelines/{!s}/pause'.format(team_name, pipeline_name)
        return self._put(path)

    def unpause_pipeline(self, pipeline_name, team_name=''):
        ''' Un-pause a pipeline '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/pipelines/{!s}/unpause'.format(team_name, pipeline_name)
        return self._put(path)

    def list_pipeline_builds(self, pipeline_name, team_name=''):
        ''' List all build of a pipeline '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/pipelines/{!s}/builds'.format(team_name, pipeline_name)
        return self._get(path)

    def create_pipeline_build(self, pipeline_name, team_name=''):
        ''' Start pipeline build '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/pipelines/{!s}/builds'.format(team_name, pipeline_name)
        return self._post(path)

    def pipeline_badge(self, pipeline_name, team_name=''):
        ''' Get pipeline badge '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/pipelines/{!s}/badge'.format(team_name, pipeline_name)
        return self._get(path)

    # ### Resources ####
    def list_all_resources(self):
        ''' List all resources '''
        path = '/api/v1/resources'
        return self._get(path)

    def list_resources(self, pipeline_name, team_name=''):
        ''' List resources of a pipeline '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/pipelines/{!s}/resources'.format(team_name, pipeline_name)
        return self._get(path)

    def list_resource_types(self, pipeline_name, team_name=''):
        ''' List resources types of a pipeline '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/pipelines/{!s}/resource-types'.format(team_name, pipeline_name)
        return self._get(path)

    def get_resource(self, pipeline_name, resource_name, team_name=''):
        ''' Get a resource '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/pipelines/{!s}/resources/{!s}'.format(team_name, pipeline_name, resource_name)
        return self._get(path)

    def list_resource_versions(self, pipeline_name, resource_name, limit=100, team_name=''):
        ''' List resource versions '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/pipelines/{!s}/resources/{!s}/versions?limit={!s}'.format(
            team_name, pipeline_name, resource_name, limit)
        return self._get(path)

    def get_resource_version(self, pipeline_name, resource_name, resource_version_id, team_name=''):
        ''' Get the version of a resource '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/pipelines/{!s}/resources/{!s}/versions/{!s}'.format(
            team_name, pipeline_name, resource_name, resource_version_id)
        return self._get(path)

    def enable_resource_version(self, pipeline_name, resource_name, resource_version_id, team_name=''):
        ''' Enable a resource '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/pipelines/{!s}/resources/{!s}/versions/{!s}/enable'.format(
            team_name, pipeline_name, resource_name, resource_version_id)
        return self._put(path)

    def disable_resource_version(self, pipeline_name, resource_name, resource_version_id, team_name=''):
        ''' Disable a resource version '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/pipelines/{!s}/resources/{!s}/versions/{!s}/disable'.format(
            team_name, pipeline_name, resource_name, resource_version_id)
        return self._put(path)

    def pin_resource_version(self, pipeline_name, resource_name, resource_config_version_id, team_name=''):
        ''' Pin a resource version '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/pipelines/{!s}/resources/{!s}/versions/{!s}/pin'.format(
            team_name, pipeline_name, resource_name, resource_config_version_id)
        return self._put(path)

    def unpin_resource_version(self, pipeline_name, resource_name, resource_config_version_id, team_name=''):
        ''' Un-pin a resource version '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/pipelines/{!s}/resources/{!s}/versions/{!s}/unpin'.format(
            team_name, pipeline_name, resource_name, resource_config_version_id)
        return self._put(path)

    def list_builds_with_version_as_input(self, pipeline_name, resource_name, resource_id, team_name=''):
        ''' List builds with versions as input '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/pipelines/{!s}/resources/{!s}/versions/{!s}/input_to'.format(
            team_name, pipeline_name, resource_name, resource_id)
        return self._get(path)

    def list_builds_with_version_as_output(self, pipeline_name, resource_name, resource_id, team_name=''):
        ''' List builds with versions as output '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/pipelines/{!s}/resources/{!s}/versions/{!s}/output_to'.format(
            team_name, pipeline_name, resource_name, resource_id)
        return self._get(path)

    def get_resource_causality(self, pipeline_name, resource_name, resource_version_id, team_name=''):
        ''' Get resource casuality '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/pipelines/{!s}/resources/{!s}/versions/{!s}/causality'.format(
            team_name, pipeline_name, resource_name, resource_version_id)
        return self._get(path)

    def pause_resource(self, pipeline_name, resource_name, team_name=''):
        ''' Pause a resource '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/pipelines/{!s}/resources/{!s}/pause'.format(team_name, pipeline_name, resource_name)
        return self._put(path)

    def unpause_resource(self, pipeline_name, resource_name, team_name=''):
        ''' Un-pause a resource '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/pipelines/{!s}/resources/{!s}/unpause'.format(
            team_name, pipeline_name, resource_name)
        return self._put(path)

    # ### Teams ####
    def list_teams(self):
        ''' List teams '''
        path = '/api/v1/teams'
        return self._get(path)

    def list_team_builds(self, team_name=''):
        ''' List team builds '''
        if not team_name:
            team_name = self._team_name
        path = '/api/v1/teams/{!s}/builds'.format(team_name)
        return self._get(path)

    # ### Common ####
    def _authenticate(self):
        ''' Authenticate with Concourse, keep the authentication cookie '''
        self._token = None
        session = requests.Session()
        response = session.get(self._url + '/sky/login')
        if requests.codes.ok:
            post_url = list(
                filter(
                    lambda x: '/sky/issuer/auth/local' in x,
                    response.text.split('\n')))[0].strip().split('"')[1]
            response = session.post(self._url + post_url, {'login': self._username, 'password': self._password})
            if 'invalid username and password' in response.text:
                raise Exception('Authentication failure')
            if response.status_code == requests.codes.ok:
                # Find the right cookie and its expiration date
                for cookie in session.cookies:
                    if cookie.name == 'skymarshal_auth':
                        # Raise execption if we have no cookie content
                        if len(cookie.value.split()) == 0:
                            self._http_errorhandling(response, 'retrieving cookie (unexpected cookie value)')
                        self._token = cookie.value.split()[-1].replace('"', '')
                        self._expires = cookie.expires

        if self._token and len(self._token) >= 900:
            self._headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self._token}
            return
        self._http_errorhandling(response, 'retrieving cookie')

    def _check_expiry(self):
        ''' Check expiry date of auth cookie and re-auth if neccessary '''
        self._authenticate() if datetime.timestamp(datetime.now()) + 300 >= self._expires else None

    def _get(self, path):
        ''' HTTP get method '''
        self._check_expiry()
        response = requests.get(self._url + path, headers=self._headers)
        if response.status_code == requests.codes.ok:
            return json.loads(response.text)
        self._http_errorhandling(response, 'sending get request')

    def _post(self, path, post_data=''):
        ''' HTTP post method '''
        self._check_expiry()
        response = requests.post(self._url + path, headers=self._headers, data=post_data)
        if response.status_code == requests.codes.ok:
            return json.loads(response.text)
        self._http_errorhandling(response, 'sending post request')

    def _put(self, path):
        ''' HTTP put method '''
        self._check_expiry()
        response = requests.put(self._url + path, headers=self._headers)
        if response.status_code == requests.codes.ok:
            return
        self._http_errorhandling(response, 'sending put request')

    def _http_errorhandling(self, http_response, action=''):
        ''' Dump the HTTP response object on error '''
        response_dump = str(pprint(http_response.__dict__, indent=2))
        raise Exception('HTTP error ' + str(http_response.status_code) + ' while ' + action + '\n' + response_dump)
