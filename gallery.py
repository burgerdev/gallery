#!/usr/bin/env python3

import os
import glob

_listing_template = """
<html>
<head><title>{site} - {dir}</title></head>
<body>
<h1>{dir}</h1>
{back}
<p>
<table>
<tr><th scope="col">Size</th><th scope="col">Content</th></tr>
{items}
</table>
</p>
</body>
</html>
"""

_link_template = """<tr><td>{prefix}</td><td><a href="{target}">{name}</td></tr>"""

_index = "index.html"

def itemize(f):
    base = os.path.basename(f)
    if os.path.isdir(f):
        prefix = "Dir"
        target = os.path.join(base, "index.html")
    else:
        size = os.path.getsize(f)
        prefix = "{}B".format(size, base)
        target = base
    return _link_template.format(target=target, name=base, prefix=prefix)

def listing(d, site="Gallery", back=True):
    assert(os.path.isdir(d))
    if back:
        back = """<p><a href="../index.html">Back</a></p>"""
    else:
        back = ""
    items = (itemize(f) for f in glob.glob(os.path.join(d, "*")))
    return _listing_template.format(
        site=site, dir=os.path.basename(d), items="\n".join(items), back=back)

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("dir", type=str, default=".", nargs="?")

    args = parser.parse_args()


    for d in glob.glob("./**/", recursive=True):
        print(d)
        with open(os.path.join(d, "index.html"), "w") as f:
            f.write(listing(d, back= d != "./"))
