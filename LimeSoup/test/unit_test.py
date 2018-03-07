#!/usr/bin/env python

"""
unit_test script is a script to test the parser_paper class.
Future to be implementated, this is file is from an old
implementation for a different problem.

Use:
    python 



"""

__author__ = "Tiago Botari"
__copyright__ = ""
__version__ = "1.0"
__maintainer__ = "Tiago Botari"
__email__ = "tiagobotari@gmail.com"
__date__ = "May 20 2017"

import unittest
import argparse

from LimeSoup.ECSSoup import ECSSoup
import json


class TestKnownValuesOffline(unittest.TestCase):
    # Test a list of html files from paper of different publishers, future...
    # Create a instance with a emulated method to create a test set offline
    from LimeSoup.ECSSoup import ECSSoup

    # This a test for known values, other tests can be included.
    def test_ECSSoup_parser(self):
        """parser should give known result with known input"""
        for k in range(1, 2):
            know_value = json.load(open('ecs_papers/paper{:}.json'.format(k)))
            with open('ecs_papers/paper{:}.html'.format(k), 'r') as fd:
                html_str = fd.read()
            result = ECSSoup.parse(html_str)
            self.assertEqual(know_value, result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""unit_test is a script that test the ParserPaper class""",
        epilog="""Author: {}
            Version: {}
            Last updated: {}""".format(__author__, __version__, __date__))
    parser.add_argument(
        "-ARG1",
        help="""descriptions of ARG1 .""")
    args = parser.parse_args()
    if args.ARG1 is None:
        ARG1 = args.ARG1
    if ARG1 is not None:
        print("Performing online test!")
    else:
        print("Performing just offline test!")
    print("\nPerforming offline test!")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestKnownValuesOffline)
    unittest.TextTestRunner().run(suite)