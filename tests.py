import os
import unittest
import shutil
from xml.etree import ElementTree as et

from mock import patch

import cipush
import cipush.parser
import cipush.push
import cipush.backend
import cipush.ci
import cipush.conf



class ParserTests(unittest.TestCase):

    def test_coverage_karma(self):
        tree = et.parse('examples/cobertura-karma.xml')
        self.assertAlmostEqual(
                cipush.parser.get_coverage_from_cobertura_xml(tree),
                0.1485
            )

    def test_coverage_python(self):
        tree = et.parse('examples/cobertura-python.xml')
        self.assertAlmostEqual(
                cipush.parser.get_coverage_from_cobertura_xml(tree),
                0.6152
            )

    def test_num_tests_python(self):
        tree = et.parse('examples/junit-python.xml')
        self.assertEqual(
                cipush.parser.get_num_tests_from_junit_xml(tree),
                11
            )

    def test_num_tests_karma(self):
        tree = et.parse('examples/junit-karma.xml')
        self.assertEqual(
                cipush.parser.get_num_tests_from_junit_xml(tree),
                10
            )
             
    def test_duration_karma(self):
        tree = et.parse('examples/junit-karma.xml')
        self.assertAlmostEqual(
                cipush.parser.get_duration_from_junit_xml(tree),
                0.159
            )   

    def test_duration_python(self):
        tree = et.parse('examples/junit-python.xml')
        self.assertAlmostEqual(
                cipush.parser.get_duration_from_junit_xml(tree),
                0.121
            )   


class PushTests(unittest.TestCase):

    def tearDown(self):
        backend_instance = cipush.push.get_backend('json')
        del backend_instance._queue[:]

    def test_get_backend(self):
        instance = cipush.push.get_backend('json')
        self.assertTrue(isinstance(instance, cipush.backend.BaseBackend))


    def test_get_backend_fail(self):
        try:
            cipush.push.get_backend('does-not-exist')
            self.fail()
        except cipush.CiPushException:
            pass

    def test_get_ci(self):
        instance = cipush.push.get_ci('default')
        self.assertTrue(isinstance(instance, cipush.ci.BaseCi))


    def test_get_ci_fail(self):
        try:
            cipush.push.get_ci('does-not-exist')
            self.fail()
        except cipush.CiPushException:
            pass

    def test_capture_metric_coverage(self):
        backend_instance = cipush.push.get_backend('json')
        self.assertEqual(len(backend_instance._queue), 0)

        cipush.push.capture_metric('coverage', 'frontend', 'json', 'default', 'examples/cobertura-karma.xml')
        
        self.assertEqual(len(backend_instance._queue), 1)
        metric_name, metric_value = backend_instance._queue.pop()
        self.assertEqual(metric_name, 'coverage.default_project.frontend.default_branch.coverage')
        self.assertAlmostEqual(metric_value, 0.1485)
    
    def test_capture_metric_coverage_fail_more_then_one_matching_file(self):
        try:
            cipush.push.capture_metric('coverage', 'frontend', 'json', 'default', 'examples/cobertura-*.xml')
            self.fail()
        except cipush.CiPushException:
            pass

    def test_capture_metric_coverage_fail_no_matches(self):
        try:
            cipush.push.capture_metric('coverage', 'frontend', 'json', 'default', 'does-not-exist')
            self.fail()
        except cipush.CiPushException:
            pass

    def test_capture_metric_junit(self):
        backend_instance = cipush.push.get_backend('json')
        self.assertEqual(len(backend_instance._queue), 0)

        cipush.push.capture_metric('junit', 'backend', 'json', 'default', 'examples/junit-*.xml')
        
        self.assertEqual(len(backend_instance._queue), 2)
        metric_name, metric_value = backend_instance._queue.pop()
        self.assertEqual(metric_name, 'junit.default_project.backend.default_branch.num_tests')
        self.assertEqual(metric_value, 21)
    
        metric_name, metric_value = backend_instance._queue.pop()
        self.assertEqual(metric_name, 'junit.default_project.backend.default_branch.duration')
        self.assertAlmostEqual(metric_value, 0.159 + 0.121)


    def test_capture_metric_junit_fail_no_matches(self):
        try:
            cipush.push.capture_metric('junit', 'backend', 'json', 'default', 'does-not-exist')
            self.fail()
        except cipush.CiPushException:
            pass


class ConfTests(unittest.TestCase):

    conf_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'examples/.pushci.yml.example')

    def test_default_config_file_path(self):
        self.assertEqual(
                cipush.conf.default_config_file_path(),
                os.path.join(os.path.dirname(os.path.realpath(__file__)), '.pushci.yml')
            )

    def test_parse_config_file(self):
        conf_list = cipush.conf.parse_config_file(self.conf_file_path)
        self.assertEqual(conf_list, [
                {'junit': {'backend': 'json',
                    'ci': 'default',
                    'pwd': 'examples/junit-*',
                    'suite': 'frontend'}},
                {'coverage': {'backend': 'json',
                       'ci': 'default',
                       'pwd': 'examples/cobertura-karma.xml',
                       'suite': 'backend'}}
            ])
        cipush.conf.validate_config(conf_list)
            
    def test_parse_config_file_fail(self):
        shutil.move('.pushci.yml', '.pushci.yml.backup')
        self.assertFalse(os.path.exists(cipush.conf.default_config_file_path()))
        try:
            cipush.conf.parse_config_file()
            self.fail()
        except cipush.CiPushException:
            pass
        shutil.move('.pushci.yml.backup', '.pushci.yml')
    
    def test_parse_config_file_fail_unvalid_yaml(self):
        readme_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'README.md')
        self.assertTrue(os.path.exists(readme_path))
        try:
            cipush.conf.parse_config_file(readme_path)
            self.fail()
        except cipush.CiPushException:
            pass

    def test_validate_config_fail(self):
        conf_list = \
            [{'junit': {'backend': 'json',
                'ci': 'default',
                'suite': 'frontend'}}]
        try:
            cipush.conf.validate_config(conf_list)
            self.fail()
        except AssertionError:
            pass
        
    def test_validate_config_fail_2(self):
        conf_list = \
            [{'does-not-exist': {'backend': 'json',
                'ci': 'default',
                'suite': 'frontend'}}]
        try:
            cipush.conf.validate_config(conf_list)
            self.fail()
        except AssertionError:
            pass

if __name__ == '__main__':
    unittest.main()