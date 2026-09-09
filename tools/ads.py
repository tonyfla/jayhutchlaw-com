#!/usr/bin/env python3
"""Manage the social media ad library in marketing/ads/.

    python3 tools/ads.py new meta dui-atlanta v1 [--page /practice-areas/dui-defense/]
    python3 tools/ads.py check

`new`   scaffolds the ad folder, writes ad.md with a correctly tagged
        destination URL, and adds a row to REGISTRY.md.
`check` audits the library: oversized images, committed video, missing or
        malformed UTM tags, and utm_source values that are not wired into
        MARKETING_SOURCE_IDS in functions/api/lead.js.
"""
import argparse
import datetime
import os
import re
import shutil
import sys
from urllib.parse import urlencode

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADS = os.path.join(ROOT, "marketing", "ads")
REGISTRY = os.path.join(ADS, "REGISTRY.md")
SITE = "https://www.jayhutchlaw.com"

PLATFORMS = ["meta", "google", "linkedin", "other"]

# Platform folder -> the utm_source value that platform's ads should carry.
UTM_SOURCE = {
    "meta": "facebook",
    "google": "google",
    "linkedin": "linkedin",
    "other": "referral",
}

MAX_IMAGE_MB = 2
MAX_ANY_MB = 10
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".avi", ".webm", ".mkv"}


def mb(path):
    return os.path.getsize(path) / (1024 * 1024)


def tagged_url(page, source, campaign, variant, medium="cpc"):
    params = urlencode({
        "utm_source": source,
        "utm_medium": medium,
        "utm_campaign": campaign,
        "utm_content": variant,
    })
    return f"{SITE}{page}?{params}"


def cmd_new(args):
    if args.platform not in PLATFORMS:
        sys.exit(f"Unknown platform '{args.platform}'. Use one of: {', '.join(PLATFORMS)}")

    slug = re.sub(r"[^a-z0-9-]", "-", args.campaign.lower()).strip("-")
    variant = re.sub(r"[^a-z0-9]", "", args.variant.lower())
    date = args.date or datetime.date.today().isoformat()
    name = f"{date}-{slug}-{variant}"
    dest = os.path.join(ADS, args.platform, name)

    if os.path.exists(dest):
        sys.exit(f"Already exists: {os.path.relpath(dest, ROOT)}")

    shutil.copytree(os.path.join(ADS, "_template"), dest)
    os.makedirs(os.path.join(dest, "creative"), exist_ok=True)
    gitkeep = os.path.join(dest, "creative", ".gitkeep")
    if not os.listdir(os.path.join(dest, "creative")):
        open(gitkeep, "w").close()

    source = UTM_SOURCE[args.platform]
    url = tagged_url(args.page, source, slug, variant)

    md = os.path.join(dest, "ad.md")
    body = open(md, encoding="utf-8").read()
    body = body.replace("# [Ad name]", f"# {slug.replace('-', ' ').title()} — {variant}")
    body = body.replace("| **Platform** | meta / google / linkedin / other |",
                        f"| **Platform** | {args.platform} |")
    body = body.replace("| **Campaign** | practice area + geography, e.g. `dui-atlanta` |",
                        f"| **Campaign** | `{slug}` |")
    body = body.replace("| **Variant** | `v1` |", f"| **Variant** | `{variant}` |")
    body = re.sub(r"```\nhttps://www\.jayhutchlaw\.com[^\n]*\n```",
                  f"```\n{url}\n```", body, count=1)
    open(md, "w", encoding="utf-8").write(body)

    row = (f"| {date} | {args.platform} | `{slug}` | `{variant}` | draft "
           f"| [{name}]({args.platform}/{name}/) |\n")
    with open(REGISTRY, "a", encoding="utf-8") as fh:
        fh.write(row)

    rel = os.path.relpath(dest, ROOT)
    print(f"Created {rel}")
    print(f"  Destination: {url}")
    print(f"  Next: add creative to {rel}/creative/, then fill in the copy in ad.md")


def cmd_check(args):
    problems = []
    notes = []

    wired = set()
    lead_js = os.path.join(ROOT, "functions", "api", "lead.js")
    if os.path.exists(lead_js):
        block = re.search(r"MARKETING_SOURCE_IDS = \{(.*?)\};", open(lead_js, encoding="utf-8").read(), re.S)
        if block:
            wired = set(re.findall(r"^\s*(\w+):\s*\d+", block.group(1), re.M))

    ad_files = []
    for platform in PLATFORMS + ["archive"]:
        base = os.path.join(ADS, platform)
        if not os.path.isdir(base):
            continue
        for entry in sorted(os.listdir(base)):
            folder = os.path.join(base, entry)
            if not os.path.isdir(folder) or entry.startswith("_"):
                continue
            ad_files.append((platform, entry, folder))

    for platform, entry, folder in ad_files:
        rel = os.path.relpath(folder, ROOT)
        md = os.path.join(folder, "ad.md")

        if not os.path.exists(md):
            problems.append(f"{rel}: no ad.md")
            continue

        text = open(md, encoding="utf-8").read()

        urls = re.findall(r"https://www\.jayhutchlaw\.com\S*", text)
        tagged = [u for u in urls if "utm_source=" in u]
        if not tagged:
            problems.append(f"{rel}: destination URL has no UTM tags — leads from this ad will be untraceable")
        else:
            for u in tagged:
                for key in ("utm_medium", "utm_campaign", "utm_content"):
                    if key not in u:
                        problems.append(f"{rel}: destination URL missing {key}")
                src = re.search(r"utm_source=([\w.-]+)", u)
                if src and wired and src.group(1) not in wired:
                    notes.append(f"{rel}: utm_source '{src.group(1)}' is not in MARKETING_SOURCE_IDS "
                                 f"(lead is still created, but arrives untagged in Clio Grow)")

        if re.search(r"^\|\s*\*\*Status\*\*\s*\|\s*live\s*\|", text, re.M | re.I):
            if re.search(r"^\|\s*\*\*Approved\*\*\s*\|\s*not yet", text, re.M | re.I):
                problems.append(f"{rel}: marked live but not approved")

        creative = os.path.join(folder, "creative")
        files = []
        if os.path.isdir(creative):
            files = [f for f in os.listdir(creative) if not f.startswith(".")]
        if not files and platform != "archive":
            notes.append(f"{rel}: no creative files yet")

        for f in files:
            path = os.path.join(creative, f)
            ext = os.path.splitext(f)[1].lower()
            size = mb(path)
            if ext in VIDEO_EXT:
                problems.append(f"{rel}/creative/{f}: video committed to git ({size:.1f} MB) — "
                                f"move it to R2 or a shared drive and link it in ad.md")
            elif ext in IMAGE_EXT and size > MAX_IMAGE_MB:
                problems.append(f"{rel}/creative/{f}: {size:.1f} MB exceeds the {MAX_IMAGE_MB} MB image limit — re-export it")
            elif size > MAX_ANY_MB:
                problems.append(f"{rel}/creative/{f}: {size:.1f} MB is too large to commit")

    # An empty table means every ad's source is unmapped, which is worth saying
    # once rather than silently passing.
    if ad_files and not wired:
        notes.append("MARKETING_SOURCE_IDS in functions/api/lead.js is empty — every lead "
                     "will arrive in Clio Grow without a marketing source. Fill it in from "
                     "GET /grow/sources once the Clio account exists.")

    print(f"Checked {len(ad_files)} ad{'s' if len(ad_files) != 1 else ''}.\n")
    if problems:
        print("Problems:")
        for p in problems:
            print(f"  ✗ {p}")
        print()
    if notes:
        print("Notes:")
        for n in notes:
            print(f"  · {n}")
        print()
    if not problems and not notes:
        print("Nothing to report.")
    return 1 if problems else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    new = sub.add_parser("new", help="scaffold a new ad")
    new.add_argument("platform", help=f"one of: {', '.join(PLATFORMS)}")
    new.add_argument("campaign", help="campaign slug, e.g. dui-atlanta")
    new.add_argument("variant", nargs="?", default="v1", help="variant, default v1")
    new.add_argument("--page", default="/", help="landing path, e.g. /practice-areas/dui-defense/")
    new.add_argument("--date", help="override the date (YYYY-MM-DD)")
    new.set_defaults(func=cmd_new)

    check = sub.add_parser("check", help="audit the ad library")
    check.set_defaults(func=cmd_check)

    args = parser.parse_args()
    sys.exit(args.func(args) or 0)


if __name__ == "__main__":
    main()
