# Personal Injury Quest — v1

| | |
|---|---|
| **Platform** | meta |
| **Placement** | story / reel (9:16 vertical) |
| **Campaign** | `personal-injury-quest` |
| **Variant** | `v1` |
| **Status** | draft |
| **Approved** | not yet — needs J. Hutchins |
| **Live dates** | — |
| **Budget** | — |

## Destination

```
https://www.jayhutchlaw.com/resources/after-a-car-accident-in-georgia/?utm_source=facebook&utm_medium=cpc&utm_campaign=personal-injury-quest&utm_content=v1
```

Landing on the guide rather than the homepage is deliberate: the four levels in
this ad are the same four beats as that guide (get care, document, do not post
or sign, deadlines). Message match lowers bounce.

If the goal is form-fills rather than calls, switch the destination to
`/practice-areas/personal-injury/` — that page carries its own consultation
form tagged `practice_personal_injury`, so leads arrive in Clio Grow already
categorised. Change `utm_content` to `v1-pp` if you run both so they stay
separately measurable.

**Story and reel placements put the link in the sticker, not the caption.** The
tagged URL above must go in the link sticker. The `jayhutchlaw.com` printed on
the creative is branding — it is not clickable and carries no attribution.

## Copy

**On-creative text** (part of the image, not editable at run time)

> PERSONAL INJURY QUEST — LEVEL UP YOUR CLAIM!
>
> **Level 1: Get Care** — Seek medical attention. Follow your treatment plan.
> **Level 2: Collect Proof** — Take photos. Save records. Get witness contacts.
> **Level 3: Avoid Traps** — Don't post the accident or sign papers you don't understand.
> **Final Level: Act Fast** — Deadlines may apply. Call Attorney Jay.
>
> IF AN ACCIDENT KNOCKS YOU OFF YOUR WAY — LEVEL UP YOUR CLAIM WITH ATTORNEY JAY!
>
> JAY HUTCH LAW · 855-HUTCHLAW · JAYHUTCHLAW.COM
> Attorney advertising. General information only.

**Primary text** (caption — draft, needs approval)

> Hurt in an accident in Georgia? The first few days decide what's possible
> later. Four steps, no jargon. Free consultation — 855-488-2452.

**Headline**

> After an accident: the first four moves

**Call to action button**

> Learn More

## Creative

| File | Size | Notes |
|---|---|---|
| `creative/story-1080x1920.png` | — | **not yet added — see below** |

Retro pixel-art game styling. Dark navy and gold, consistent with the site
palette. Four level panels plus a closing banner and the firm's contact bar.

**Export at 1080×1920.** The version supplied is smaller than that; Meta will
upscale it, and pixel art degrades badly when resampled. Re-export at exactly
1080×1920 with nearest-neighbour scaling to keep the pixel edges crisp.

## Alt text

Required on Meta, and this ad is entirely text-in-image — without alt text none
of it reaches anyone using a screen reader.

> Retro video-game styled poster titled "Personal Injury Quest: Level Up Your
> Claim." Four levels: get medical care, collect proof, avoid traps such as
> posting about the accident or signing papers you don't understand, and act
> fast because deadlines may apply. Jay Hutch Law, 855-HUTCHLAW,
> jayhutchlaw.com. Attorney advertising, general information only.

## Targeting

- Location: Atlanta metro, Georgia
- Age: 21+
- Audience:

## Notes

**Legibility.** The level descriptions are small relative to a phone-sized story
frame. The headline and the closing banner will read fine; the body lines may
not. Worth testing on an actual handset before spending on it — and consider a
variant that carries one level per frame in a carousel.

**Compliance — for J. Hutchins.** The creative already carries "Attorney
advertising. General information only," which is the right instinct. Two things
to confirm before this runs:

- Whether "Level Up Your Claim" reads as implying an improved outcome under
  Georgia Rule 7.1. A game framing is not inherently misleading, but the phrase
  is doing outcome-adjacent work and it is worth a deliberate decision rather
  than an accidental one.
- Whether the gamified treatment of an injury claim sits comfortably with the
  firm's positioning. This is a judgement call, not a rule — flagging it so it
  is made on purpose.

**Attribution.** `utm_source=facebook` is not yet present in
`MARKETING_SOURCE_IDS` in `functions/api/lead.js`. Leads will still be created,
but will arrive in Clio Grow untagged until that table is filled in from
`GET /grow/sources`.
