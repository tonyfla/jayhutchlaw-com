# Ads

One folder per ad. Put the files in it, write a few lines in `ad.md`. That's it.

```
ads/
  personal-injury-quest/
    ad.md
    story.png
```

Nothing here is published — `.cfignore` keeps `marketing/` out of the deploy.

## The link

This is the only part worth being careful about. An ad pointing at a bare
`jayhutchlaw.com` produces leads you cannot trace back to it, and there is no
way to reconstruct that later.

```bash
python3 tools/adlink.py personal-injury /resources/after-a-car-accident-in-georgia/
```

That prints the tagged URL. Paste it into the ad — for stories and reels that
means the **link sticker**, not the caption. A URL printed on the image itself
is branding; it isn't clickable and carries no tracking.

The pattern, if you'd rather just type it:

```
?utm_source=facebook&utm_medium=cpc&utm_campaign=NAME&utm_content=v1
```

Use `--source instagram` (or `google`, `linkedin`) and `--variant v2` for a
second version of the same ad, so you can tell which creative actually worked.

## Files

Keep images under about 2 MB. Meta re-compresses everything on upload, so a
huge source file buys nothing.

**Don't commit video.** Git keeps every version of every file forever and can't
compress video — a few clips will make this repo permanently slow to clone.
Put video in the Cloudflare R2 bucket or a shared drive and link it in `ad.md`.

## Colours, for building creative

| Use | Hex |
|---|---|
| Navy | `#0e2947` |
| Deep navy | `#061a30` |
| Gold — decorative only | `#b38a4d` |
| Gold — text and buttons | `#8c6626` |
| Ivory | `#faf8f3` |

`#b38a4d` is too light to read against white — use `#8c6626` for any wording,
including the call to action. Headings are Libre Baskerville, body is DM Sans;
the exact font files are in `assets/fonts/`.

Georgia advertising rules apply to social ads, not just the website. Confirm
with J. Hutchins what each ad needs, and don't state or imply a guaranteed result.
