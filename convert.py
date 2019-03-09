#!/usr/bin/env python3
import re
import os

from collections import defaultdict

# example format: 20170913_174448.jpg

_filename_re = re.compile(r"([0-9]{4})([0-9]{2}).*")
_conversion = "vips resize '{src}' '{dst}' {scale:.03f}"
_copy = "{cp} '{src}' '{dst}'"


def name_to_dict(name):
    m = _filename_re.match(name)
    if m is None:
        return None
    g = m.groups()
    return dict(year=g[0], month=g[1], name=m.string)


def dict_to_out(base, ext, d):
    return os.path.join(base, d["year"], d["month"], d["name"] + ext)


def convert(src, dst, scale):
    cmd = _conversion.format(src=src, dst=dst, scale=scale)
    os.system(cmd)


def copy(cp, src, dst):
    os.system(_copy.format(cp=cp, src=src, dst=dst))


def mkdir(target):
    os.system("mkdir -p '{}'".format(target))


if __name__ == "__main__":
    from argparse import ArgumentParser
    from glob import glob
    parser = ArgumentParser()

    parser.add_argument("input_dir")
    parser.add_argument("output_dir")
    parser.add_argument("--copy", action="store_true", default=False, help="create copies instead of hard links (default: false)")

    args = parser.parse_args()
    cp = "cp" if args.copy else "ln"

    files = list(glob(os.path.join(args.input_dir, "*.jpg")))
    num_items = len(files)
    i = 0

    for f in files:
        print("processing {}/{}".format(i, num_items))
        i += 1
        d = name_to_dict(os.path.basename(f))
        if d is None:
            raise ValueError("unexpected file name {}".format(f))
        mkdir(os.path.dirname(dict_to_out(args.output_dir, "", d)))
        copy(cp, f, dict_to_out(args.output_dir, "", d))
        convert(f, dict_to_out(args.output_dir, ".small.jpg", d), 0.01)
        convert(f, dict_to_out(args.output_dir, ".medium.jpg", d), 0.05)
