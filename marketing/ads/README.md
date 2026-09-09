# Social media ad library

Every paid ad the firm runs, with its creative files, its copy, and the tagged
link it points at. Not deployed — `.cfignore` keeps `marketing/` out of the
Cloudflare build, so nothing here is published.

## Layout

```
ads/
  REGISTRY.md      one line per ad — the index. Scan this first.
  _template/       copy this folder to start a new ad
  meta/            Facebook and Instagram (one Meta ads account)
  google/          Google Ads image and video assets
  linkedin/        LinkedIn (estate planning, business audiences)
  other/           anything else — TikTok, Nextdoor, local sponsorships
  archive/         retired ads. Move, do not delete.
  brand-kit/       logo files, colour swatches, fonts for building creative
```

One folder per ad, named `YYYY-MM-DD-campaign-variant`:

```
meta/2026-09-14-dui-atlanta-v1/
  ad.md                     copy, targeting, dates, the tagged link
  creative/
    feed-1080x1080.jpg
    story-1080x1920.jpg
```

Variants of the same ad (`-v1`, `-v2`) get their own folders, because they need
their own `utm_content` value to be measurable separately.

## File rules

**Images: commit them.** Keep each under **2 MB**. Export JPG for photography,
PNG only when you need transparency. A 1080×1080 feed image should be
200–500 KB; if yours is 4 MB it was exported wrong.

**Video: do not commit it.** Git stores every version of every file forever, and
it cannot compress video. A handful of 30 MB clips will make this repository
slow to clone permanently, and you cannot cleanly remove them later.

Put video masters in the Cloudflare R2 bucket or a shared drive, and record the
link in `ad.md` under **Creative**. If video becomes routine, set up Git LFS
(`git lfs install && git lfs track "*.mp4"`) before committing the first one —
not after.

`python3 tools/ads.py check` enforces both rules.

## Adding an ad

```bash
python3 tools/ads.py new meta dui-atlanta v1
```

That creates the folder, writes `ad.md`, generates the correctly tagged
destination URL, and adds the ad to `REGISTRY.md`. Drop the creative files into
`creative/` and fill in the copy.

## Why the tagged link matters

The site captures UTM parameters on landing, holds them for the session, and
writes them into the Clio Grow lead. **An ad pointing at a bare URL produces a
lead you cannot trace back to it.** There is no way to recover that afterwards.

So every ad link must carry its tags, and `utm_content` must match the variant —
that is what tells you which creative actually produced clients rather than
which one produced clicks.

`utm_source` values also map to Clio Grow marketing sources in
`functions/api/lead.js` (`MARKETING_SOURCE_IDS`). A source that is not in that
table still creates the lead, but arrives untagged in the CRM. Keep the two in
step: `python3 tools/ads.py check` reports any mismatch.

## Status values

Use one of: `draft`, `in review`, `live`, `paused`, `archived`.

Ads run under the firm's name and carry professional-responsibility
obligations. Nothing moves to `live` without J. Hutchins approving the copy —
record the date on the `Approved` line in `ad.md`.
