# Copyright (c) 2020 Stig Rune Sellevag
#
# This file is distributed under the MIT License. See the accompanying file
# LICENSE.txt or http://www.opensource.org/licenses/mit-license.php for terms
# and conditions.

"""Module providing I/O utilities."""

import sys
import re


def openfile(fname, mode="r"):
    """Helper function to open a file or filename for I/O."""
    if not fname:
        return
    elif isinstance(fname, str):
        return open(fname, mode)  # got filename
    else:  # got file
        return fname


def find_label(fname, label):
    """
    Function for finding label in file object.

    Args:
        fname: filename or input file object
        label: label to be found

    Return:
        found: True if label is found; False otherwise
        pos:   file position for where label is found
    """
    finp = openfile(fname, mode="r")
    pos = finp.tell()
    plabel = r"(\s+)?set " + label + " = {"
    found = False
    while True:
        if found:
            break
        line = finp.readline()
        if not line:
            break
        if line.startswith("#"):
            continue
        mlabel = re.search(plabel, line)
        if mlabel:
            found = True
            pos = finp.tell()
            break
    return found, pos


def read_vector_prm(fname, key="vector", dtype=float):
    """
    Return 1D array parameter from input file object as list.

    Note:
        The formatting of the array must be on the form
        set key =
        [value1 value2 value3 # this is a comment
        value4 value5 value6]
    """
    finp = openfile(fname, mode="r")
    vector = []
    pattern = r"set " + key + " ="
    found = False
    while not found:
        line = finp.readline()
        if not line:
            raise IOError("bad formatting of " + key)
        elif line.startswith("#"):
            continue
        match = re.search(pattern, line)
        if match:
            vector = read_vector(finp, dtype)
            break
    return vector


def read_vector(fname, dtype=None):
    """
    Return 1D array from an input file object as list.

    Note:
        The function reads values until ']' is encountered.
    """
    finp = openfile(fname, mode="r")
    vector = []
    found = False
    while not found:
        line = finp.readline()
        if not line:
            raise IOError("no data found")
        elif line.startswith("[]"):
            found = True
            break
        elif line.startswith("#"):
            continue
        tmp = line.split()
        for value in tmp:
            if value.startswith("["):
                if value[1:]:
                    if value.endswith(","):
                        vector.append(value[1:-1])
                    elif value.endswith("]"):
                        found = True
                        vector.append(value[1:-1])
                        break
                    else:
                        vector.append(value[1:])
                else:
                    continue
            elif value.startswith("]"):
                found = True
                break
            elif value.endswith("]"):
                found = True
                vector.append(value[:-1])
                break
            elif value.startswith("#"):
                break  # ignore rest of data in tmp
            else:
                if value.endswith(","):
                    vector.append(value[:-1])
                else:
                    vector.append(value)
    if dtype:
        vector = [dtype(v) for v in vector]
    return vector


def read_list2(fname, dtype=None):
    """
    Return list of lists from an input file object.

    Note:
        The list must be formatted as '[ [1, 2, 3], [4, 5, 6] ]'.
    """
    finp = openfile(fname, mode="r")
    lst = []
    ltmp = []
    found = False
    while not found:
        line = finp.readline()
        if not line:
            raise IOError("no data found")
        elif line.startswith("[[]]"):
            found = True
            break
        elif line.startswith("[]"):
            found = True
            break
        elif line.startswith("#"):
            continue
        tmp = line.split()
        for value in tmp:
            if value[:] == "]":
                found = True
                break
            if value[:] == "[":
                continue
            if value.startswith("["):
                ltmp = []
                if value.endswith("],"):
                    ltmp.append(value[1:-2])
                    lst.append(ltmp)
                    ltmp = []
                elif value.endswith("]"):
                    ltmp.append(value[1:-1])
                    lst.append(ltmp)
                    ltmp = []
                elif value.endswith(","):
                    ltmp.append(value[1:-1])
            else:
                if value.endswith("],"):
                    ltmp.append(value[:-2])
                    lst.append(ltmp)
                    ltmp = []
                elif value.endswith("]"):
                    ltmp.append(value[:-1])
                    lst.append(ltmp)
                    ltmp = []
                elif value.endswith(","):
                    ltmp.append(value[:-1])
    if dtype:
        for i in range(len(lst)):
            for j in range(len(lst[i])):
                lst[i][j] = dtype(lst[i][j])
    return lst


def print_vector(vector, fname=sys.stdout, fmt="%.6e"):
    """Print vector to output file object."""
    fout = openfile(fname, mode="w")
    if len(vector) == 1:
        buf = "[" + fmt + "]\n"
        fout.write(buf % vector[0])
    else:
        it = 0
        buf = "[" + fmt + ", "
        fout.write(buf % vector[0])
        buf = fmt + ", "
        for i in range(1, len(vector)-1):
            fout.write(buf % vector[i])
            if it == 5:
                fout.write("\n")
                it = 0
            it += 1
        buf = fmt + "]\n"
        fout.write(buf % vector[-1])


def print_list2(lst, fname=sys.stdout):
    """Print list of lists to output file object."""
    fout = openfile(fname, mode="w")
    if len(lst) == 1:
        fout.write("[ %s ]\n" % lst[0])
    else:
        fout.write("[ %s,\n" % lst[0])
        for i in range(1, len(lst)-1):
            fout.write("  %s,\n" % lst[i])
        fout.write("  %s ]\n" % lst[-1])


def print_heading(heading, fname=sys.stdout):
    """Print heading."""
    n = len(heading)
    fout = openfile(fname, mode="w")
    fout.write("\n")
    fout.write("%s" % "=" * n)
    fout.write("\n%s\n" % heading)
    fout.write("%s" % "=" * n)
    fout.write("\n")


def atof_list(buf):
    """Convert a list in string format to float."""
    vec = []
    for v in buf:
        for ch in ["[", "]", "'", ","]:
            if ch in v:
                v = v.replace(ch, "")
        vec.append(float(v))
    return vec


def atoi_list(buf):
    """Convert a list in string format to integers."""
    vec = []
    for v in buf:
        for ch in ["[", "]", "'", ","]:
            if ch in v:
                v = v.replace(ch, "")
        vec.append(int(v))
    return vec


def atoa_list(buf):
    """Convert a list in string format to a proper list of strings."""
    vec = []
    for v in buf:
        for ch in ["[", "]", "'"]:
            if ch in v:
                v = v.replace(ch, "")
        vec.append(v)
    return vec
