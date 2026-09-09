#!/usr/bin/env python3
"""Build a UTM-tagged link for an ad.

    python3 tools/adlink.py <campaign> <landing-path> [options]

    python3 tools/adlink.py personal-injury /resources/after-a-car-accident-in-georgia/
    python3 tools/adlink.py dui-atlanta /practice-areas/dui-defense/ --source instagram --variant v2

Options: --source (default facebook) --medium (default cpc) --variant (default v1)

Why bother: an ad pointing at an untagged URL produces leads you cannot trace
back to it, and that cannot be reconstructed afterwards. The tags are read by
the site on landing, kept for the session, and written into the Clio Grow lead.
"""
import argparse
import os
import sys
from urllib.parse import urlencode

SITE = "https://www.jayhutchlaw.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("campaign", help="campaign name, e.g. dui-atlanta")
parser.add_argument("path", help="landing path, e.g. /practice-areas/dui-defense/")
parser.add_argument("--source", default="facebook", help="utm_source (default: facebook)")
parser.add_argument("--medium", default="cpc", help="utm_medium (default: cpc)")
parser.add_argument("--variant", default="v1", help="utm_content (default: v1)")
args = parser.parse_args()

path = "/" + args.path.strip("/") + "/" if args.path.strip("/") else "/"

# Catch a mistyped landing path here rather than after the money is spent.
local = os.path.join(ROOT, path.strip("/"))
if path != "/" and not (os.path.exists(local) or os.path.exists(os.path.join(local, "index.html"))):
    print(f"warning: {path} does not exist in this repo — check the path", file=sys.stderr)

print(SITE + path + "?" + urlencode({
    "utm_source": args.source,
    "utm_medium": args.medium,
    "utm_campaign": args.campaign,
    "utm_content": args.variant,
}))
