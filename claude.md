# AMC Healthcare Website — Claude Code Handoff

## Session Goals

Approximate clone of https://amchealthcareinc.com/about-us/, simple enough to host on Netlify. Scoped to a 7-page shell (Home, About Us, Process, Press, Contact Us, Leadership, Partners) in a prior Cowork session, then dropped into this repo (`wardrush/amcwebsite`, already `git init`'d with `origin` pointed at GitHub — see Repo State below) to continue in Claude Code.

Status: pages built, link-checked, and two rounds of contrast fixes applied (see Key Decisions). Not yet visually diffed against the live site — that's the top item in Next Steps.

## Repo State (as of this handoff)

- `origin` → `https://github.com/wardrush/amcwebsite.git`, branch `master`, tracking `origin/master`.
- One prior commit ("first commit") containing only `README.md`.
- Everything below is **untracked** — nothing from this session has been committed or pushed. That's intentional: committing/pushing wasn't done here so the first real commit is a deliberate one made in Claude Code, not an automated drop.
- `README.md` predates this session and has an odd encoding (looks like it was saved as UTF-16 via GitHub's web UI) — worth re-saving as plain UTF-8 at some point, low priority.
- **`.git/index.lock` exists and couldn't be removed from this session** (`Operation not permitted` — likely ProtonDrive sync holding a lock on the file). This will block git commands with `fatal: Unable to create '.git/index.lock': File exists.` until it's cleared. Delete it by hand (File Explorer, or `del .git\index.lock` from a regular terminal on the actual machine, not through sync) before running any git commands in Claude Code.

## Key Decisions

**Full shell over single page.** About Us links to Leadership and Partners in its dropdown, and the header nav includes Process/Press/Contact Us. Building all seven pages avoids five dead links off a single-page clone.

**Images hotlinked, not downloaded.** Every `<img>` src points at the live `amchealthcareinc.com/wp-content/uploads/...` URL. Two things forced this in the Cowork sandbox: outbound `curl`/`wget` to the domain was blocked by network rules, and the fetch tool available there only returns text (no binary/image support). **This constraint doesn't apply in Claude Code** — downloading the images locally and repointing `<img>` src values is a reasonable cleanup task now that a normal dev environment is available. URLs are all listed in `build.py`.

**Styling is a best-effort approximation, not a computed-CSS match.** No browser inspection tool was available in the Cowork session (Chrome extension stayed disconnected all session), so the live page's actual CSS — exact colors, font stack, spacing — was never inspected. Current palette: navy `#0b2545`, teal accent `#1c7c9c`, `--text-light: #4b5563`. This is a guess informed by the "dark" footer-logo variant name and general genre convention, **not** verified against the source. **This is still the biggest gap versus the real page** — first thing to fix once a real browser is available (see Next Steps).

**Contrast pass (round 2, this session).** User flagged that text was reading too close in color to background elements in two places:
1. *Footer* — `--text-light` was `#6b7280` against the footer's `#f5f6f8` background, ~2.9:1 contrast (fails WCAG AA). Darkened to `#4b5563` (~6.3:1), which also improved every other place `--text-light` is used (press dates, form notes, stat-strip captions).
2. *About Us hero banner* — the H1 "About Us" was rendering directly below the banner image with only ~40px of padding, and the image came before the title in DOM order (opposite of the live site, which shows the title first). Restructured `about_body` in `build.py` so the title sits in its own full-width white block *above* the banner image, matching the live site's actual DOM order and guaranteeing navy-on-white contrast regardless of what colors are in the banner photo itself. Also bumped `.hero` bottom margin to 32px for clearer separation.

If contrast still looks off anywhere after these changes, the likely next culprit is the `--accent` teal (`#1c7c9c`) used for the "eyebrow" label text on the Contact page — it's borderline (~5:1 on white, technically passes AA but is the next weakest ratio in the stylesheet).

**Contact form is non-functional by design.** Static HTML form, JS `alert()` on submit, no backend. Netlify Forms is the lowest-effort fix (add `data-netlify="true"` and a hidden `form-name` input to the `<form>` tag in `build.py`'s `contact_body`); otherwise wire it to Formspree or similar.

**Homepage is a lightweight placeholder,** not a clone of the real (video-heavy) homepage — the actual ask was About Us, so `index.html` is a simplified hero + stat strip.

**A file-sync gremlin, for the record:** mid-session, edits made through the file-editing tool weren't immediately visible to the shell environment used to run `build.py` — the shell saw a truncated version of `build.py` twice, causing `SyntaxError`s that had nothing to do with the actual edits. Fixed by writing the file directly from the shell instead of through the editor. Not expected to recur in Claude Code (single environment, no editor/shell split), but if a Python script mysteriously has a `SyntaxError` pointing at content that looks fine when read normally, checking for truncation (`wc -l`, tail the file) is the fast diagnostic.

## Useful Files Directory

```
amcwebsite/  (repo root — this is the Netlify publish directory)
├── claude.md          # this file
├── README.md          # pre-existing, from repo init — odd encoding, low-priority fix
├── build.py            # Python generator — edit page content/nav here, then `python3 build.py`
├── index.html           # homepage placeholder
├── about-us.html        # the original target page — closest to a full clone
├── process.html
├── press.html
├── contact-us.html      # static form, not wired to a backend
├── leadership.html      # 8 team member cards, hotlinked headshots
├── partners.html        # 8 partner links (text tiles, not the partners' actual logos — see Known Gaps)
└── css/style.css        # single shared stylesheet
```

Regenerate all pages after editing `build.py`: `python3 build.py` (writes directly into the repo root).

## Next Steps

1. **Visual QA against the live site.** With a real browser available in Claude Code, open `about-us.html` locally and the live page side by side, and adjust the CSS custom properties in `css/style.css` (`--navy`, `--accent`, `--text-light`, font stack) to match. This is the fastest way to close the single biggest known gap.
2. **Decide on image hosting.** Hotlinking works today but creates a silent dependency on AMC's own media library. Download the URLs listed in `build.py` into an `assets/` folder and repoint the `<img>` tags if that dependency is unwanted.
3. **Wire up the contact form** if it needs to actually receive submissions (Netlify Forms is the low-effort option since this is already headed for Netlify).
4. **First commit.** Nothing from this session is committed yet — review the diff, then `git add -A && git commit` and push when ready.
5. **Deploy.** Connect the GitHub repo to Netlify for continuous deploy (publish directory = repo root, no build command needed since these are static files), or use `netlify deploy` from the CLI.

## Assets + Optimization Session Update

Once outbound access to `amchealthcareinc.com` was whitelisted, the biggest
open gaps were closed:

- **Real palette + font.** Pulled the live Kadence global palette from source:
  navy `#102343` (palette2), copper `#be7048` (palette1, the real
  button/link accent — the old teal `#1c7c9c` was wrong and is gone), slate
  `#405f7a`, gold `#d8ae4f`. Body font stack now leads with Aptos (the live
  site's font). Footer is now navy with white text/logo, matching the live
  site (its footer background is palette2, which is why the "Secondary_Dark"
  logo is a light logo).
- **Self-hosted, optimized assets.** All images downloaded and converted to
  `.webp` (73 files, ~5 MB total — the raster originals were ~120 MB, so they
  are intentionally NOT committed). Videos downloaded and re-encoded with
  ffmpeg: homepage background loop downscaled 4K→1080p (MP4 + WebM, no audio),
  the promo/feature films compressed to 720p/1080p MP4 with `preload="none"`
  and webp poster frames (~39 MB total). No more hotlinking except the press
  article destination links (intentional).
- **Homepage upgraded** from the gradient placeholder to a real video-hero
  (autoplay muted loop + navy overlay) plus a featured hospital film and an
  "Our Story" promo row.
- **Reproducibility:** `tools/fetch_and_optimize.py` re-downloads and
  re-optimizes everything from the live site (`--videos` to also re-encode),
  so the pruned originals are always one command away.
- **Visual QA** done via headless Chromium against local renders (the live
  site sits behind Cloudflare, which resets the headless browser's connection,
  so side-by-side live capture wasn't possible — the match was driven off the
  extracted source CSS instead).

## Known Gaps

- Partners page uses text tiles instead of the partners' actual logos (their
  logo images are now downloaded under `assets/img/` if you want to wire them
  in).
- webp is served directly with no `<img>` fallback — fine for current browsers
  (~97% support); revisit only if you must support very old clients.
- Contact form is wired to **Netlify Forms** (`data-netlify="true"`, hidden
  `form-name`, `name` attributes on every field, a `bot-field` honeypot, and a
  `/thank-you.html` success redirect). Submissions appear in the Netlify
  dashboard under Forms once deployed; no backend code needed.

## Claude Code Session Update (this session)

- `css/style.css` didn't make it into the upload bundle, so it was written from scratch here, covering every class referenced across the seven pages (nav incl. dropdown/hamburger, hero sections, galleries, press list, contact form, people grid, partner tiles, footer) plus responsive breakpoints at 900/720/480px. Palette follows the navy/teal/`--text-light` values documented above.
- `build.py` was writing to a `site/` subfolder (`SITE = os.path.join(os.path.dirname(__file__), "site")`), which didn't match this doc's "writes directly into the repo root" claim or the Netlify publish-directory assumption. Changed `SITE` to resolve to the script's own directory so `python3 build.py` now writes `*.html` straight into the repo root, matching the documented layout.
- Ran `build.py` and diffed the output against the three reference HTML files in the handoff bundle (`about-us.html`, `contact-us.html`, `index.html`) — byte-identical, confirming the generator logic is sound.
- Verified all internal links across all 7 pages resolve to files that exist.
- Checked every page (all Python `html.parser` well-formedness clean) and rendered all 7 pages plus a mobile viewport + hamburger-menu-open state via headless Chromium. Layout, nav, footer, contrast, and the mobile menu toggle all work as intended. The only console errors were `ERR_TUNNEL_CONNECTION_FAILED` on the hotlinked AMC images — expected, this sandbox blocks outbound requests to `amchealthcareinc.com` the same way the original Cowork session did.
- Re-saved `README.md` as plain UTF-8 (was UTF-16LE, per the note above).
- Added a `.gitignore` for `.claude/settings.local.json` (session-local permission state, not project content).
- First commit made and pushed from this session.