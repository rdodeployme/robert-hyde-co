# Robert Hyde & Co. website (concept prototype)

**Live (concept, noindex):** https://rdodeployme.github.io/robert-hyde-co/
**Repo:** github.com/rdodeployme/robert-hyde-co (public). Local copy on Ryan's Mac: ~/Documents/GitHub/robert-hyde-co (GitHub Desktop; fetch/pull to update it).

A static, multi-page site. No build tools are needed to host it: upload the folder as-is to GitHub Pages or any static host.

## Pages
- `index.html`: home
- `story.html`: the time machine (eight stops, 1857 to today, each with sources). Deep links work, e.g. `story.html#1863`.
- `what-we-buy.html`: filterable item list, "ask us first" and "we can't take"
- `sell.html`: five-step "get a price" form with photo upload, review and confirmation
- `trade.html`, `contact.html`: enquiry forms
- `faq.html`: questions, with FAQ structured data
- `404.html`

## Editing
Content lives in `_build/build.py`. Change it, then run `python3 _build/build.py` to regenerate every page. Styles are in `assets/site.css` and behaviour in `assets/site.js`.

## Before it goes live
- **Protect the name first:** register "Robert Hyde & Co" as a business name, register roberthyde.com.au and roberthyde.au, and file the trade mark.
- **Forms:** set `CONFIG.endpoint` at the top of `assets/site.js` to a form endpoint (for example a Google Apps Script web app writing to a Google Sheet). Until then, forms run in prototype mode and nothing is sent.
- **Details marked TBC:** phone, email, yard address and hours on `contact.html`.
- **Archive photo:** the current image is cropped from a phone screenshot. Replace `assets/img/archive-hyde-store.jpg` with the original file, and confirm its date, place, source and reuse rights.
- **Accepted items:** confirm the lists on `what-we-buy.html` with operations.
- **Search engines:** the site is set to `noindex`. At launch, remove the robots meta tag in `_build/build.py` and change `robots.txt` to allow crawling.
- **Token artwork:** an original redraw of the 1857 token face. Commission a final version before printing it on trucks or signage.

## What the copy may and may not claim
- Do say: "Reviving the name of Robert Hyde & Co., Melbourne marine store, 1857"; "one of the early marine stores that left a documented trail".
- Don't say: "since 1857", "est. 1857", "Victoria's first", or anything implying we are the original firm (Australian Consumer Law s29).

## v2: the cinematic layer
- **Home** opens on a pinned, scroll-driven time machine: Sandridge 1858, then the "R. Hyde & Co." photo zooming to its sign, then today in colour, with a year counter running from 1858 to the current year. Then the 500-tons scale band and a draggable 3D token.
- **Story** is a scroll-driven timeline: the 3D token flips at each stop, with period photos and recreated artefacts (museum label, directory listing, probate file card). Every recreation is labelled as one.
- **Every page** has an archival or site photograph as its header.
- **Libraries**, self-hosted in `assets/vendor`: GSAP and ScrollTrigger (scroll animation) and three.js r128 (3D token). `assets/coin.js` draws and embosses the token; `assets/cinema.js` runs the motion.
- **Fallbacks:** with reduced motion turned on, the home sequence shows as three stacked panels. Without WebGL, the SVG token shows instead of the 3D one.
- **Historic photographs and chart:** State Library Victoria collection, public domain, downloaded via Wikimedia Commons. Credits are on every image.

## v3: interactive extras
- **Then and now:** drag sliders comparing Bourke Street (home) and Sandridge pier (story) in 1858 and today. Modern photos: Yang.square (CC BY 2.0) and JoeHard (CC BY-SA 4.0), via Wikimedia Commons, cropped and credited under each slider.
- **Hyde's Melbourne (story page):** the 1864 Admiralty chart with every documented address pinned. Zoom, drag, keyboard pan, and a list that flies to each pin. Pins are placed by hand and approximate.
- **Depth:** the 1858 photos on the home and story heroes move in 3D with the mouse, and drift slowly on phones (WebGL; the plain photo shows if WebGL is unavailable).
- **Intro:** a darkroom iris reveal ("Melbourne, 1858"), shown once per visit and skipped with reduced motion.
- **Page transitions:** pages cross-fade and the logo holds its place between pages (Chrome and Edge now; Safari 18.2+).

## v4: polish pass
- **One palette:** warm paper (#EDE6DA) and warm ink (#15120E), with aged copper as the only accent. The verdigris green buttons and the cool greys are gone.
- **One serif:** Newsreader for every heading. Zilla Slab stays only for the lettering on the token.
- **One label style:** small uppercase copper kicker with a rule. It's used for years, sections and tags.
- **Home in three acts:** the cinema (1858 to today), then the business on paper (what we buy, how selling works, trade), then the archive on ink (500 tons, Bourke Street then and now, the token).
- **Token:** aged copper rather than bright orange.
- **Publishing:** Pages serves from `gh-pages`. Push to both `main` and `gh-pages`.
