import os
import cipush.ci

class Ci(cipush.ci.BaseCi):

    def get_project_name(self):
        return os.environ['CIRCLE_PROJECT_REPONAME']

    def get_branch_name(self):
        return os.environ['CIRCLE_BRANCH']

    def get_user_name(self):
        return os.environ['CIRCLE_USERNAME']

    def get_build_link(self):
        return 'https://circleci.com/gh/{0}/{1}/{2}'.format(
            os.environ.get('CIRCLE_PROJECT_USERNAME'),
            os.environ.get('CIRCLE_PROJECT_REPONAME'),
            os.environ.get('CIRCLE_BUILD_NUM'),
        )