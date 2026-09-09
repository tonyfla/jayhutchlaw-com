Status: DRAFT

# Campaigns

One file per campaign, named `YYYY-MM-DD-platform-topic.md`.

## UTM convention

All inbound paid and referral links must be tagged. The site captures these on
landing, holds them for the session, and writes them into the Clio Grow lead —
so an untagged link produces a lead with no attribution.

    ?utm_source=google&utm_medium=cpc&utm_campaign=dui-atlanta&utm_term=dui+lawyer+atlanta

| Parameter | Use |
|---|---|
| `utm_source` | `google`, `bing`, `facebook`, `instagram`, `referral` |
| `utm_medium` | `cpc`, `organic-social`, `email`, `referral` |
| `utm_campaign` | practice area + geography, e.g. `dui-atlanta` |
| `utm_term` | the keyword, for search campaigns |
| `utm_content` | the ad variant, for A/B tests |

`utm_source` values must match the keys in `MARKETING_SOURCE_IDS` in
`functions/api/lead.js` for the lead to be tagged with a Clio Grow source.
