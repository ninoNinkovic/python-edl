# -*- coding: utf-8 -*-

import unittest
from itertools import izip_longest
from edl import Parser


class EDLTestCase(unittest.TestCase):
    """tests the edl.edl.List class
    """

    def testing_to_edl_method_will_output_the_standard_edl_case1(self):
        """testing if to_string will output the EDL as string
        """
        p = Parser('24')
        with open('../tests/test_data/test_24.edl') as f:
            expected_edl = [line.rstrip('\n') for line in f.readlines()]
            # Reset to beginning of file and read into new EDL
            f.seek(0)
            actual_edl = p.parse(f).to_string().split('\n')

        # Remove blank lines, since they don't affect data content
        expected_edl = [line for line in expected_edl if line]
        actual_edl = [line for line in actual_edl if line]

        self.maxDiff = None

        self.assertEqual(len(expected_edl), len(actual_edl),
                         "Generated EDL has the same number of data lines as "
                         "original EDL.")

        for expected, actual in izip_longest(expected_edl, actual_edl):
            # Remove extraneous whitespace to prevent false negatives
            expected = " ".join(expected.split())
            actual = " ".join(actual.split())

            self.assertEqual(expected, actual, "Generated EDL line is the same"
                                               "as original EDL line.")


    def testing_to_edl_method_will_output_the_standard_edl_case2(self):
        """testing if to_string will output the EDL as string
        """
        p = Parser('24')
        with open('../tests/test_data/test.edl') as f:
            s = p.parse(f)

        with open('../tests/test_data/test.edl') as f:
            expected_edl = f.readlines()

        print s.to_string()

        self.assertEqual(
            ''.join(expected_edl),
            s.to_string()
        )

    def testing_to_edl_method_will_output_the_standard_edl_case3(self):
        """testing if to_string will output the EDL as string
        """
        p = Parser('24')
        with open('../tests/test_data/test_50.edl') as f:
            s = p.parse(f)

        with open('../tests/test_data/test_50.edl') as f:
            expected_edl = f.readlines()

        print s.to_string()

        self.assertEqual(
            ''.join(expected_edl),
            s.to_string()
        )
