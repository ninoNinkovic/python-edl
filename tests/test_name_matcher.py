# -*- coding: utf-8 -*-

import unittest
import re
from edl import EDL
from edl.matchers import TitleMatcher


class NameMatcherTestCase(unittest.TestCase):
    """tests the edl.edl.TitleMatcher class
    """

    def runTest(self):
        self.test_TitleMatcher_regex_is_working_properly()
        self.test_TitleMatcher_apply_is_working_properly()

    def test_TitleMatcher_regex_is_working_properly(self):
        """testing if the TitleMatcher.regex is working properly
        """
        test_line = 'TITLE: Sequence 01'
        e = TitleMatcher()

        m = re.search(e.regex, test_line)

        self.assertIsNotNone(m)

        self.assertEqual(
            'Sequence 01',
            m.group(1).strip()
        )

    def test_TitleMatcher_apply_is_working_properly(self):
        """testing if the TitleMatcher.apply() is working properly
        """
        ed_list = EDL('24')

        e = TitleMatcher()

        test_line = 'TITLE: Sequence 01'
        e.apply(ed_list, test_line)

        self.assertEqual(
            'Sequence 01',
            ed_list.title
        )

        test_line = 'TITLE: Test EDL 24'
        e.apply(ed_list, test_line)

        self.assertEqual(
            'Test EDL 24',
            ed_list.title
        )
