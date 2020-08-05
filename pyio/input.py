# Copyright (c) 2020 Stig Rune Sellevag
#
# This file is distributed under the MIT License. See the accompanying file
# LICENSE.txt or http://www.opensource.org/licenses/mit-license.php for terms
# and conditions.

""" Module providing methods for input of variables."""

import re
import pyio.io_utils as io_utils


class Input:
    """
    Class for easy input of parameters from file objects.

    Attributes:
        __data: dictionary for storage of parameters
    """
    def __init__(self, **kwargs):
        self.__data = {}

        for key in iter(kwargs):
            self.__data[key] = kwargs.get(key)

    def get(self, key=None):
        """Get input parameters."""
        if key:
            return self.__data[key]
        else:
            return self.__data

    def load(self, fname, label=None):
        """Load input parameters from file object."""
        finp = utils.openfile(fname, "r")
        pos = finp.tell()

        found = True
        if label:
            found, pos = io_utils.find_label(finp, label)

        if found:
            finp.seek(pos)
            pkey = r"(\s+)?set (\w+)? =(\s+)?(.*)?"
            pend = r"(\s+)?}"
            while True:
                line = finp.readline()
                if not line:
                    break
                match_key = re.search(pkey, line)
                match_end = re.search(pend, line)
                if match_key:
                    key = match_key.group(2)
                    ans = self._load_helper(finp, key, match_key)
                    if ans:
                        self.__data[key] = ans
                if match_end:
                    break
        return self.__data

    def _load_helper(self, fname, key, match):
        """Helper function for loading parameters."""
        finp = io_utils.openfile(fname, "r")
        pval = r"(\w+)?"
        pstr = r"(.*)?"
        pint = r"([-+]?\d+)?"
        pfloat = r"([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)?"
        ans = None
        if key in self.__data:
            dtype = type(self.__data[key])
            if dtype is str:
                pval = pstr
                mval = re.search(pval, match.group(4))
                if mval:
                    ans = str(mval.group(0))
                    pos = ans.find("#")  # ignore comments
                    if pos > 0:
                        ans = ans[:pos].strip()
            elif dtype is int:
                pval = pint
                mval = re.search(pval, match.group(4))
                if mval:
                    ans = int(mval.group(0))
            elif dtype is float:
                pval = pfloat
                mval = re.search(pval, match.group(4))
                if mval:
                    ans = float(mval.group(0))
            elif dtype is list:
                if len(self.__data[key]) > 0:
                    dtype = type(self.__data[key][0])
                    ans = io_utils.read_vector(finp, dtype=dtype)
                else:
                    ans = io_utils.read_vector(finp, dtype=None)
        return ans
