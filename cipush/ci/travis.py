import os
import cipush.ci

class Ci(cipush.ci.BaseCi):

    def get_project_name(self):
        travis_repo_slug = os.environ['TRAVIS_REPO_SLUG']
        _, project_name = travis_repo_slug.split()

        return project_name

    def get_branch_name(self):
        return os.environ['TRAVIS_BRANCH']

    def get_user_name(self):
        return 'default'

    def get_build_link(self):
        return 'https://travis-ci.org/{0}/builds/{1}'.format(
            os.environ.get('TRAVIS_REPO_SLUG'),
            os.environ.get('TRAVIS_BUILD_ID'),
        )