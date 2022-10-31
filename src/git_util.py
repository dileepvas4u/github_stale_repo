import requests
import logging
import json
import sys
import os

class GitAPI:
    
    def __init__(self, user_name: str, repo_name: str) -> None:
        self.__version__ = 0.1
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"logging level set as: {self.logger.level}")

        self.user_name = user_name
        self.repo_name = repo_name
        self.set_base()
    
    def set_base(self):
        if 'GIT_ACCESS_TOKEN' not in os.environ:
            self.logger.error('Please add access token into environment variable GIT_ACCESS_TOKEN')
            self.logger.info("os.environ['GIT_ACCESS_TOKEN'] = '***********'")
            self.logger.info('MORE INFO -- https://docs.github.com/en/enterprise-server@3.4/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token')
            raise EnvironmentError("Failed because GIT_ACCESS_TOKEN is not set.")

        self.base_url = f"https://api.github.com/repos/{self.user_name}/{self.repo_name}"
        self.headers = {
            'Content-type': 'application/json', 
            'Accept': 'application/vnd.github+json',
            'Authorization': f"Bearer {os.environ['GIT_ACCESS_TOKEN']}"
        }
    
    def list_branches(self) -> dict:
        try:
            response = requests.get(f'{self.base_url}/branches', headers=self.headers)
            response_json = response.json()
            self.logger.info(f'Response -- {response}')
            self.logger.info(f'Found total {len(response_json)} branches.')
        except Exception as e:
            self.logger.error('Failed calling branches API \n', e)
        else:
            return response_json
    
    def get_branch_info(self, branch: dict) -> dict:
        try:
            branch_info_ = requests.get(branch['commit']['url'])
            branch_info = branch_info_.json()
        except Exception as e:
            self.logger.error('Failed fetching branch info \n', e)
        else:
            return {
                'branch_name': branch['name'],
                'committer_name': branch_info['commit']['committer']['name'],
                'committer_email': branch_info['commit']['committer']['email'],
                'author_name': branch_info['commit']['author']['name'],
                'author_email': branch_info['commit']['author']['email'],
                'date': branch_info['commit']['committer']['date'],
                'commit_message': branch_info['commit']['message'],
            }
