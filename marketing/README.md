# Marketing document repository

Internal working files for Jay Hutch Law. **Nothing in this folder is published.**
It is excluded from the deploy by `.cfignore` and is not referenced by any page.

## Layout

| Folder | Contents |
|---|---|
| `brand/` | Logo files, colour and type specification, usage rules |
| `brand/source/` | Editable originals (PSD, AI, full-resolution photography) |
| `copy/` | Approved text — the single source of truth for the site and ads |
| `ads/` | **Social media ads — creative files, copy, and tagged links.** See `ads/README.md` |
| `campaigns/` | Keyword lists, budget and performance notes |
| `email/` | Clio Grow nurture sequences and intake templates |
| `assets/` | Finished collateral: PDFs, one-pagers, social graphics |

## Why `copy/` matters

Practice-area text currently lives in three places that drift apart: the website,
Google Ads, and whatever gets typed into an intake email. `copy/` is the version
everything else is copied *from*. When the firm's description of a practice area
changes, it changes here first.

## Review status

Legal marketing copy carries professional-responsibility obligations. Every file
should carry a status line at the top:

    Status: DRAFT — not for publication
    Status: APPROVED — reviewed by J. Hutchins, YYYY-MM-DD

Anything marked DRAFT must not go on the site or into an ad.

## Ads

`ads/` holds the actual ad files. Two commands run it:

```bash
python3 tools/ads.py new meta dui-atlanta v1 --page /practice-areas/dui-defense/
python3 tools/ads.py check
```

`new` scaffolds the folder with a correctly tagged destination URL. `check`
audits everything — oversized images, video committed to git, missing UTM tags,
ads marked live without approval, and utm_source values that are not wired into
Clio Grow. It exits non-zero on problems, so it can go in a pre-commit hook.

## Naming

`YYYY-MM-DD-short-description.ext` for dated material (campaigns, reports).
Plain kebab-case for living documents (`practice-areas.md`, `firm-boilerplate.md`).
