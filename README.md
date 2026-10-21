# App web pages (privacy, support, landing): static, no JS, GitHub Pages-ready
Built by Designer, Oct 21 2026. Layout: `apps/quietwell/{,privacy/,support/}` and `apps/glasswell/{,privacy/,support/}` (each an `index.html`, so URLs end in `/`).

## Files
| Path | What |
|---|---|
| `config.json` | **`SELLER` (placeholder until the rebrand) and `EMAIL`.** The only place to change them |
| `src/<app>/privacy.md`, `support.md` | Copy. Glasswell = Growth Lead's copy from `water/site/`; Quietwell = Designer copy, reviewed and finalized by Growth Lead Oct 21 2026. Glasswell src is synced from `water/site/` with {{SELLER}}/{{EMAIL}} placeholders |
| `build.py` | Renders `apps/` from `src/` + `config.json` + the app's design tokens (`design-kit/tools/tokens.py`), copies a 180 px icon, and fails if any text color pair is under 4.5:1 |
| `apps/` | Generated site (commit this) |
| `index.html`, `.nojekyll` | Root list of apps; `.nojekyll` makes Pages serve files as-is |
| `screenshots/` | Headless Chrome renders, mobile (390 px) and desktop (1280 px) |

## Change the seller name or email
Edit `config.json`, then run `python3 build.py` (needs `pip install markdown pillow`) and commit. The seller also appears in generated HTML inside `<span class="seller">`, so a plain find-and-replace on `Nimbus Web Design LLC` across `apps/` works too.

## Deploy to GitHub Pages (free)
1. Put the **contents** of this folder at the root of a public repo (or a `docs/` folder), so `apps/quietwell/privacy/index.html` sits at `<root>/apps/quietwell/privacy/index.html`.
2. Repo Settings › Pages › Build and deployment › Source: *Deploy from a branch*, branch `main`, folder `/ (root)` (or `/docs`). Save.
3. Pages URL: `https://<user>.github.io/<repo>/apps/quietwell/privacy/`. All internal links are relative, so it works at any base path.
4. Custom domain (optional, the URLs in the listings expect `https://nimbuswebdesign.com/apps/<app>/privacy/`): add the domain in Settings › Pages (this writes a `CNAME` file), point DNS (`CNAME www → <user>.github.io`, or apex A records 185.199.108–111.153), and tick *Enforce HTTPS*. Only do this if that domain isn't already hosting the Keepwell pages elsewhere. If it is, copy `apps/*` into that site instead.
5. Put the final URLs into App Store Connect (Privacy Policy URL, Support URL) and into each app's Settings links.

Local check: `python3 -m http.server 8931` and open `http://127.0.0.1:8931/apps/glasswell/`.
