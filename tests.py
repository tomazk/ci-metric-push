import unittest
from xml.etree import ElementTree as et

from mock import patch

import cipush
import cipush.parser
import cipush.push
import cipush.backend
import cipush.ci



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

    def test_get_ci(self):
        instance = cipush.push.get_ci('default')
        self.assertTrue(isinstance(instance, cipush.ci.BaseCi))

    def test_capture_metric_coverage(self):
        backend_instance = cipush.push.get_backend('json')
        self.assertEqual(len(backend_instance._queue), 0)

        cipush.push.capture_metric('coverage', 'frontend', 'json', 'default', 'examples/cobertura-karma.xml')
        
        self.assertEqual(len(backend_instance._queue), 1)
        metric = backend_instance._queue.pop()
        self.assertTrue('coverage.default_project.frontend.default_branch.coverage' in metric)
        self.assertAlmostEqual(metric['coverage.default_project.frontend.default_branch.coverage'], 0.1485)
    
    def test_capture_metric_coverage_fail(self):
        try:
            cipush.push.capture_metric('coverage', 'frontend', 'json', 'default', 'examples/cobertura-*.xml')
            self.fail()
        except cipush.CiPushException:
            pass

    #def test_capture_metric_junit(self):









if __name__ == '__main__':
    unittest.main()