#!/usr/bin/env python3
import re
import os

from collections import defaultdict

# example format: 20170913_174448.jpg

_filename_re = re.compile(r"([0-9]{4})([0-9]{2}).*")
_conversion = "vips resize '{src}' '{dst}' 0.01"
_copy = "cp '{src}' '{dst}'"


def name_to_dict(name):
    m = _filename_re.match(name)
    if m is None:
        return None
    return dict(year=m.groups[0], month=m.groups[1], name=m.string)


def dict_to_out(base, ext, d):
    return os.path.join(base, d["year"], d["month"], d["name"] + ext)


def convert(src, dst):
    os.system(_conversion(src=src, dst=dst))


def copy(src, dst):
    os.system(_copy(src=src, dst=dst))


if __name__ == "__main__":
    from argparse import ArgumentParser
    from glob import glob
    parser = ArgumentParser()

    parser.add_argument("input_dir")
    parser.add_argument("output_dir")

    args = parser.parse_args()

    files = list(glob(os.path.join(args.input_dir, "*.jpg")))
    num_items = len(l)
    i = 0

    for f in files:
        print("processing {}/{}".format(i, num_items))
        i += 1
        if i > 3:
            break
        d = name_to_dict(os.path.basename(f))
        if d is None:
            raise ValueError("unexpected file name {}".format(f))
        copy(f, dict_to_out(args.input_dir, "", f))
        convert(f, dict_to_out(args.input_dir, ".small.jpg", f))
