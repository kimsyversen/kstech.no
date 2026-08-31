# Kstech: app portfolio

The public `kstech.no` site is a GitHub Pages portfolio. Each app is maintained
and published separately on Cloudflare Pages, and the portfolio links directly
to those eight app sites.

```
/                       Landing page
/support/               One support page for every app
/404.html               Not-found page
/robots.txt             Crawler rules for kstech.no
/sitemap.xml            Sitemap for the kstech.no pages
/pacingguard/           Legacy local fallback page, not linked from the portfolio
/respirix/              Legacy local fallback page, not linked from the portfolio
/lull/                  Legacy local fallback page, incomplete on purpose
/spacesift/             Legacy local fallback page, not linked from the portfolio
/promptuary/             Legacy local fallback page, not linked from the portfolio
/<app>/assets/          That app's icon
/assets/app.css         The stylesheet every app page and /support/ share
/assets/fonts.css       Self-hosted @font-face rules
/assets/fonts/          woff2 files, latin + latin-ext
/assets/squircle.svg    Superellipse mask used for every icon tile
/assets/og/             Social cards, one per app plus the site card
/scripts/gen-assets.py  Rebuilds the OG cards and the favicon
/scripts/migrate.sh     Old porting helper, read the warning in §1 before running
/redirects/bulk-redirects.csv   Cloudflare Bulk Redirects import for the old domains
```

The site is deployable as-is. The landing page owns the portfolio identity and
central support page; clicking an app opens that app's own Pages site. The local
app folders are retained as a non-destructive fallback and are not part of the
main navigation.

## 1. One portfolio, separate app sites

The main portfolio is intentionally thin: it owns Kstech's identity, short app
summaries, the central support page and links to the separate app sites. Adding
an app means adding one row to `index.html`, one entry to `/support/`, and one
direct Pages URL.

The legacy local app pages are still written against one shared stylesheet,
`assets/app.css`. They are useful as a fallback or source for shared assets, but
they are no longer the public destinations from the portfolio.

**Warning about `scripts/migrate.sh`.** It was built for the old consolidated-site
plan and overwrites `<app>/index.html` with an app's old markup. Do not run it
against the local fallback pages unless you intentionally want to replace them.

Copy in the local fallback pages was taken from each app's own site, so it is the
wording you already wrote. Nothing about a feature was invented here.

## 2. Placeholder inventory (replace before go-live)

| Where | Placeholder | Replace with |
|---|---|---|
| every page's og:image and og:url, robots.txt, sitemap.xml, redirects CSV | `kstech.no` | already set for the live domain |
| index.html and support/ | `kstechnodev@gmail.com` | current support address |
| index.html and support/ | eight direct Pages URLs | keep these URLs aligned with the live Pages projects |
| Lull's accent | `#C8925B` on `lull/index.html` and row 3 of index.html | the real one. Every other accent is the app's own dark-mode `--accent`, read from its live stylesheet |
| Lull | no App Store link | the live Lull site's badge points to placeholder ID `id000000000`. Set the real ID on the Lull page and in index.html |
| Lull | tile shows the `L` monogram | add `lull/assets/app-icon.png`. The other four icons came from App Store artwork on 2026-07-25 |
| every page | name `Kstech` | change if you brand differently |

After changing an icon, an accent or a card line, rerun the asset build:

```
python3 scripts/gen-assets.py
```

It rewrites `assets/og/*.png` and the favicon set from the app icons and the
accents. It needs Google Chrome and nothing else.

## 3. Go-live runbook (order matters)

1. **Keep the current DNS.** This setup leaves `kstech.no` serving the existing
   GitHub Pages site. The app destinations remain their own `pages.dev` hosts,
   so no DNS change is needed to publish the portfolio links. Do not replace
   existing Azure, n8n, email or other records just for this update.
2. **Update the existing GitHub Pages site** from this folder and keep the
   `CNAME` file set to `kstech.no`.
3. **Check the eight app destinations** in `index.html` and `/support/` after
   publishing. Each link should open the corresponding app's Pages project;
   each app site should own its detailed marketing, support and privacy pages.
4. **Email.** The portfolio uses `kstechnodev@gmail.com` for support.
5. **App Store Connect**, per app: use that app's direct `pages.dev` URL as the
   marketing URL, `https://kstech.no/support/` as the central support URL, and
   the app site's own privacy URL where required.
6. **Old-domain redirects.** The CSV in `redirects/bulk-redirects.csv` now
   sends the four migrated domains directly to their matching Pages sites.
   Import it as a Cloudflare Bulk Redirect List and enable the corresponding
   rule only for domains that are active zones in your Cloudflare account.
   Test a normal URL and a deep link for each domain after enabling it.
7. **Keep old domains live for 6–12 months** with redirects where possible,
   then let them lapse when traffic has moved.

## 4. What was verified vs. not

- Updated 2026-08-31: the landing page and support page contain the eight direct
  Pages URLs supplied for SpaceSift, Respirix, Promptuary, Rouse, Lull, SkyHop,
  Pacing Guard and Attune.
- The local app folders and their assets were left unchanged as a fallback.
- The sitemap lists only pages hosted on `kstech.no`; app `pages.dev` URLs are
  linked from the site but are not added to the kstech.no sitemap.
- The legacy redirect CSV now targets the corresponding direct Pages sites.
- Verified 2026-08-31: all eight supplied Pages URLs returned HTTP 200.
- Landing page repositioned 2026-07-25 at your request. The hero is now the name
  plus one line about the work. The "independent Apple app studio" label is gone,
  since Kstech will cover more than Apple apps, and so are the site-wide
  "no ads / no tracking / no accounts / no subscriptions" ledger and the
  "buy once, own forever" promise. Each app row still states its own terms,
  which stay factual per app.
- Historical rebuild on 2026-07-25. What changed and where it came from:
  - **Accents.** Each app's live stylesheet declares its own dark-mode `--accent`.
    Those are now used verbatim: Pacing Guard `#4D94E8`, Respirix `#3B82F6`,
    SpaceSift `#D89878`, Promptuary `#A78BFA`. Only Lull's is still a guess.
  - **App page copy** was taken from each app's own live site, including Pacing
    Guard's Workwell Foundation note, which is reproduced word for word.
  - **Icons** came from App Store artwork at 256px, four of the original five.
  - **Fonts** are self-hosted from Google Fonts, latin and latin-ext, all three
    under the SIL Open Font License. Nothing is fetched from a third party at
    runtime any more. They are unsubsetted; `pyftsubset` would cut them a lot if
    you ever install fonttools.
  - **OG cards and favicon** are generated by `scripts/gen-assets.py`.
  - **Squircle tiles.** `assets/squircle.svg` is a real superellipse
    (`|x|^5 + |y|^5 = 1`), which is the curve Apple icons are drawn to, rather
    than a rounded rectangle.
  - **Ambient tint.** The wash behind the landing page takes the accent of the
    row under the pointer, via `:has()`, no JavaScript. Adding an app means
    adding one line to that list in index.html.
  - **View transitions.** Chrome and Safari morph the icon from the shelf into
    the app page header. Other browsers navigate normally.
  - **Entrance animations** use `backwards` fill with the hidden state inside the
    keyframe, so content that never animates is still visible.
- Verified historically against the original app sites: copy and taglines used
  in the local fallback pages, App Store links and IDs, theme colors, Lull's
  placeholder store ID, and the cross-app support emails.
- Verified against Cloudflare docs: the bulk-redirects CSV format (no header
  row; source,target,status,preserve_query,include_subdomains,subpath_matching,
  preserve_path_suffix).
- migrate.sh was smoke-tested against a synthetic site covering canonicals,
  OG tags, root-relative paths, www variants and protocol-relative URLs.
- Checked 2026-07-25: `lull.app` is a parked domain that bounces visitors to a
  registrar lander, so it is not yours. Its row remains absent from
  `redirects/bulk-redirects.csv`; the supplied `lull-website.pages.dev` URL is
  now the portfolio destination.
- Checked in a browser on 2026-07-25: every route and asset returns 200 from a
  local server, the ambient tint recolors to the hovered app's accent, and the
  pages render at desktop and mobile widths. The view transition itself was not
  watched frame by frame [unverified: open two pages in Chrome and click through].
- Not verified here: live DNS responses for `kstech.no`, GitHub Pages deployment
  state, App Store Connect field validation, or whether pacingguard.app and
  promptuaryapp.com are Cloudflare zones.

## 5. Optional cleanup

The local app folders can be removed later once you are certain no one relies on
their old `kstech.no/<app>/` URLs. Keeping them for now is safer and does not
change where the portfolio sends visitors.
