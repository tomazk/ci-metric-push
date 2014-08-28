import unittest
from xml.etree import ElementTree as et

import cipush.parser



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



if __name__ == '__main__':
    unittest.main()