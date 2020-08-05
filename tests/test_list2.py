# Copyright (c) 2020 Stig Rune Sellevag
#
# This file is distributed under the MIT License. See the accompanying file
# LICENSE.txt or http://www.opensource.org/licenses/mit-license.php for terms
# and conditions.

import os
import unittest
from pyio.io_utils import read_list2


class TestList2(unittest.TestCase):
    def test_list2(self):
        lst_orig = \
            [[1.0],
             [123231.0, 2345.0, 888754.0],
             [223467.0, 85645.0]]

        lst = read_list2(os.path.join("tests", "list2.inp"), dtype=float)
        self.assertTrue(lst == lst_orig)
