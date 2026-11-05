"""Builds the Robert Hyde & Co. static site into the folder above this one.
Run: python3 _build/build.py
Every page shares one header, footer and token so they can't drift apart."""
import os, math, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_URL = "https://roberthyde.com.au"  # intended domain, not yet registered

NAV = [
    ("index.html", "Home"),
    ("story.html", "Our story"),
    ("what-we-buy.html", "What we buy"),
    ("trade.html", "Trade"),
    ("faq.html", "FAQ"),
    ("contact.html", "Contact"),
]

def esc(s): return html.escape(s, quote=True)

# ---------------------------------------------------------------- token
def token(pid, cls="token", label="The 1857 Robert Hyde & Co. token, redrawn"):
    """Obverse of the 1857 trade token, redrawn as an original SVG (not a museum photo)."""
    beads = []
    n = 72
    for i in range(n):
        a = 2 * math.pi * i / n
        beads.append(f'<circle class="bead" cx="{100+89*math.cos(a):.2f}" cy="{100+89*math.sin(a):.2f}" r="1.35"/>')
    lines = ["GENERAL", "MARINE", "STORE", "—", "SHIPPERS OF", "RAGS GLASS", "METALS", "&amp;c."]
    sizes = [11, 11, 11, 9, 8.6, 8.6, 8.6, 8.6]
    ys = [70, 83, 96, 106, 117, 128, 139, 150]
    centre = "".join(f'<text x="100" y="{y}" text-anchor="middle" font-size="{s}" letter-spacing=".6">{t}</text>' for t, s, y in zip(lines, sizes, ys))
    return f'''<svg class="{cls}" viewBox="0 0 200 200" role="img" aria-label="{esc(label)}">
<defs>
<path id="{pid}-top" d="M 27,100 A 73,73 0 0 1 173,100"/>
<path id="{pid}-bot" d="M 21,100 A 79,79 0 0 0 179,100"/>
</defs>
<circle class="face" cx="100" cy="100" r="97"/>
<circle class="line" cx="100" cy="100" r="93.5" stroke-width="1.4"/>
{''.join(beads)}
<circle class="line" cx="100" cy="100" r="58" stroke-width="1.6"/>
<text font-size="15" letter-spacing="2.4"><textPath href="#{pid}-top" startOffset="50%" text-anchor="middle">ROBERT HYDE &amp; Co</textPath></text>
<text font-size="13" letter-spacing="3"><textPath href="#{pid}-bot" startOffset="50%" text-anchor="middle">MELBOURNE</textPath></text>
<circle class="ink" cx="40" cy="100" r="2.2"/><circle class="ink" cx="160" cy="100" r="2.2"/>
{centre}
</svg>'''

def mark(pid):
    """Small brand mark: the token's rim and beads with the monogram."""
    beads = "".join(f'<circle class="bead" cx="{50+42*math.cos(2*math.pi*i/36):.2f}" cy="{50+42*math.sin(2*math.pi*i/36):.2f}" r="1.6"/>' for i in range(36))
    return f'''<svg class="token" viewBox="0 0 100 100" aria-hidden="true" focusable="false">
<circle class="face" cx="50" cy="50" r="48"/>{beads}
<circle class="line" cx="50" cy="50" r="34" stroke-width="1.6"/>
<text x="50" y="58" text-anchor="middle" font-size="25" letter-spacing=".5">RH</text>
</svg>'''

# ---------------------------------------------------------------- shell
def page(fname, title, desc, body, extra_head="", cls="", motion=False):
    cur = ' aria-current="page"'
    nav = "".join('<a href="%s"%s>%s</a>' % (h, cur if h == fname else "", t) for h, t in NAV)
    canonical = f"{SITE_URL}/{'' if fname == 'index.html' else fname}"
    full_title = "Robert Hyde & Co. | Scrap metal buyers, Victoria" if fname == "index.html" else f"{title} | Robert Hyde & Co."
    return f'''<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="noindex,nofollow">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="assets/img/og.jpg">
<meta name="theme-color" content="#15120E">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/newsreader-latin-opsz-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/site.css">
{extra_head}
</head>
<body class="{cls}">
<a class="skip" href="#main">Skip to content</a>
<div class="proto">Concept prototype for internal review. Prices, location and contact details are still to be confirmed.</div>
<header class="site-head{" over" if fname == "index.html" else ""}">
  <div class="wrap head-in">
    <a class="brand" href="index.html">{mark("hm")}<b>Robert Hyde &amp; Co.</b></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="nav" id="site-nav" aria-label="Main">
      {nav}
      <a class="btn" href="sell.html">Get a price</a>
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        {mark("fm")}
        <h2>Robert Hyde &amp; Co.</h2>
        <p>Scrap metal buyers. Reviving the name of Robert Hyde &amp; Co., Melbourne marine store, 1857.</p>
        <p class="small">We are a new business and not the original firm. <a href="story.html#today">Read why we chose the name</a>.</p>
      </div>
      <div>
        <h3>Selling</h3>
        <ul>
          <li><a href="sell.html">Get a price</a></li>
          <li><a href="what-we-buy.html">What we buy</a></li>
          <li><a href="trade.html">Trade and business</a></li>
          <li><a href="faq.html">FAQ</a></li>
        </ul>
      </div>
      <div>
        <h3>The company</h3>
        <ul>
          <li><a href="story.html">Our story</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-base">
      <span>We pay by EFT. Bring ID: Victorian law requires us to record it for every sale.</span>
      <span>Token artwork redrawn from the 1857 original held by Museums Victoria. Historic photographs: State Library Victoria, public domain.</span>
    </div>
  </div>
</footer>
{"<script src='assets/vendor/gsap.min.js' defer></script><script src='assets/vendor/ScrollTrigger.min.js' defer></script><script src='assets/vendor/three.min.js' defer></script><script src='assets/coin.js' defer></script>" if motion else ""}
<script src="assets/site.js" defer></script>
{"<script src='assets/cinema.js' defer></script><script src='assets/extras.js' defer></script>" if motion else ""}
</body>
</html>'''

def write(fname, html_text):
    with open(os.path.join(ROOT, fname), "w", encoding="utf-8") as f:
        f.write(html_text)

# ---------------------------------------------------------------- sources
SRC = {
    "mv1857": ("Robert Hyde & Co. halfpenny token, 1857. Museums Victoria", "https://collections.museumsvictoria.com.au/items/57490"),
    "mv1861": ("Robert Hyde & Co. halfpenny token, 1861. Museums Victoria", "https://collections.museumsvictoria.com.au/items/57502"),
    "mvart": ("Robert Hyde & Co., Merchants, Melbourne. Museums Victoria", "https://collections.museumsvictoria.com.au/articles/2401"),
    "argus1861": ("Hyde's Marine Store advertisement. The Argus, 12 March 1861 (Trove)", "https://trove.nla.gov.au/newspaper/article/5698339"),
    "age1863": ("Report on Melbourne's rag export trade. The Age, 19 January 1863 (Trove)", "https://trove.nla.gov.au/newspaper/article/154969341"),
    "auction1869": ("Hyde's Rag Store auction notice, 1869 (Trove)", "https://trove.nla.gov.au/newspaper/article/5835985"),
    "trove1872": ("R. Hyde, Little Bourke Street, 1872 (Trove)", "https://trove.nla.gov.au/newspaper/article/5863231"),
    "prov": ("Probate file for Robert Hyde, VPRS 28, 17/144. Public Record Office Victoria", "https://prov.vic.gov.au/"),
    "blackmore": ("Blackmore, marine store dealer, Bourke Street, 1848 (Trove)", "https://trove.nla.gov.au/newspaper/article/226354474"),
}
def src(*keys):
    return "; ".join(f'<a href="{SRC[k][1]}">{esc(SRC[k][0])}</a>' for k in keys)

ARCHIVE = '''<figure class="archive">
  <div class="frame">
    <img src="assets/img/archive-hyde-store.jpg" width="446" height="878" alt="Sepia photograph of 19th-century Melbourne. Across an open dirt yard and a white picket fence stands a small arched-roof timber building whose sign reads R. Hyde &amp; Co.">
    <span class="ring" aria-hidden="true"></span>
  </div>
  <figcaption>The building signed &ldquo;R. Hyde &amp; Co.&rdquo; in a 19th-century view of Melbourne. Date, place and source still to be confirmed.</figcaption>
</figure>'''

# ---------------------------------------------------------------- v2: cinematic home + story
# (spliced into build.py; uses token(), mark(), src(), SRC, ARCHIVE, esc)

CREDIT = {
    "sandridge": "The railway pier, Sandridge, about 1858. Richard Daintree and Antoine Fauchery. State Library Victoria, public domain.",
    "bourke": "Bourke Street looking west from Spring Street, about 1858. Antoine Fauchery. State Library Victoria, public domain.",
    "mail": "English mail day at the Post Office, Melbourne, 1862. Nicholas Chevalier. State Library Victoria, public domain.",
    "chart": "Hobson Bay and River Yarra, Admiralty chart by Henry L. Cox, published 1865. State Library Victoria, public domain.",
    "gpo": "The General Post Office, Melbourne, 1868. Charles Nettleton. State Library Victoria, public domain.",
    "ships": "Sailing ships at the Railway Pier, Sandridge, about 1875. Charles Nettleton. State Library Victoria, public domain.",
    "hyde": "A building signed “R. Hyde & Co.” in a 19th-century view of Melbourne. Date, place and source still to be confirmed.",
}

def page_hero(img, h1, lede, credit, pos="50% 50%", tone="sepia", extra="", depth=None):
    dd = f' data-depth="{depth}"' if depth else ""
    return f'''<header class="phero {tone}">
  <img class="phero-bg" src="assets/img/{img}" alt=""{dd} style="object-position:{pos}">
  <div class="wrap phero-in">
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
    {extra}
  </div>
  <p class="credit wrap">{esc(credit)}</p>
</header>'''

CARS = "".join('<i></i>' for _ in range(330))

home = f'''
<div class="intro" data-intro aria-hidden="true"><div class="intro-in"><span>Melbourne</span><b>1858</b></div></div>
<section class="cine" id="cine" aria-label="From 1858 to today">
  <div class="cine-stage">
    <div class="scene s1">
      <div class="bgwrap"><img class="bg sepia" data-depth="0.36" src="assets/img/sandridge-pier-1858-hero.jpg" alt="Sepia photograph of Hobsons Bay about 1858: a long timber pier, sailing ships at anchor, and timber cottages on the sandy shore" fetchpriority="high"></div>
      <div class="scrim"></div>
      <div class="wrap copy">
        <p class="kicker">Melbourne, about 1858</p>
        <h1>Before it was called recycling, it was called a marine store.</h1>
        <p class="lede">Marine store dealers bought old metal, rags and glass and sold it on. One of them, Robert Hyde &amp; Co., shipped it to England by the ton.</p>
        <p class="cue" aria-hidden="true">Scroll to travel forward</p>
      </div>
      <p class="credit">{esc(CREDIT["sandridge"])}</p>
    </div>
    <div class="scene s2">
      <img class="bg sepia dim" src="assets/img/bourke-st-1858.jpg" alt="">
      <div class="scrim"></div>
      <div class="wrap s2-grid">
        <figure class="mount">
          <div class="frame"><img src="assets/img/archive-hyde-store.jpg" width="446" height="878" alt="Sepia photograph: a small arched-roof timber building behind a picket fence, its sign reading R. Hyde &amp; Co."></div>
          <figcaption>{esc(CREDIT["hyde"])}</figcaption>
        </figure>
        <div class="copy">
          <p class="kicker">East Melbourne, 1862</p>
          <h2>The sign reads &ldquo;R.&nbsp;Hyde &amp;&nbsp;Co.&rdquo;</h2>
          <p class="lede">Hyde&rsquo;s Marine Store is listed at 11 Albert Street, East Melbourne. A year later <em>The Age</em> calls it Melbourne&rsquo;s principal rag exporter.</p>
        </div>
      </div>
    </div>
    <div class="scene s3">
      <img class="bg colour" src="assets/img/bales-into-container.jpg" alt="A forklift loads a bale of compressed steel into a shipping container stacked with bales">
      <div class="scrim"></div>
      <div class="wrap s3-grid">
        <div class="copy">
          <p class="kicker">Today</p>
          <h2>The name is back. So is the trade.</h2>
          <p class="lede">Robert Hyde &amp; Co. is a new scrap metal business that has taken up the name. We buy steel, copper, brass, aluminium, cars and farm metal, and pay by EFT.</p>
          <div class="actions"><a class="btn" href="sell.html">Get a price for your scrap</a><a class="btn ghost light" href="story.html">Open the time machine</a></div>
        </div>
        <div class="coin" data-coin data-coin-idle>{token("cz", label="The 1857 Robert Hyde & Co. token, in copper")}</div>
      </div>
    </div>
    <div class="cine-year" aria-hidden="true"><span>1858</span></div>
    <div class="cine-progress" aria-hidden="true"><i></i></div>
  </div>
</section>

<section class="band paper buy-band" aria-labelledby="buy-h">
  <div class="wrap">
    <div class="section-head">
      <p class="kicker dark">The trade today</p>
      <h2 id="buy-h">What we buy</h2>
      <p>Steel, copper, brass, aluminium and whole items made of them, priced by metal, grade and weight on the day.</p>
    </div>
    <div class="split">
      <ul class="mat-list">
        <li><a href="what-we-buy.html#steel"><h3>Steel and iron</h3><span>Whitegoods, hot water services, roofing iron, shelving, pipe and offcuts</span><b class="go" aria-hidden="true">&rarr;</b></a></li>
        <li><a href="what-we-buy.html#nonferrous"><h3>Copper, brass and aluminium</h3><span>Pipe, wire, fittings, window frames, stainless sinks</span><b class="go" aria-hidden="true">&rarr;</b></a></li>
        <li><a href="what-we-buy.html#vehicles"><h3>Cars, trailers and caravans</h3><span>Collected by tilt tray, with proof of ownership</span><b class="go" aria-hidden="true">&rarr;</b></a></li>
        <li><a href="what-we-buy.html#farm"><h3>Machinery and farm metal</h3><span>Old equipment, containers, site offices, wheels</span><b class="go" aria-hidden="true">&rarr;</b></a></li>
      </ul>
      <figure class="photo">
        <img src="assets/img/loose-steel.jpg" width="1500" height="843" alt="A steel bin filled with loose, tangled steel wire after separation" loading="lazy">
        <figcaption>Loose steel after separation, before baling.</figcaption>
      </figure>
    </div>
  </div>
</section>

<section class="band paper ruled" aria-labelledby="how-h">
  <div class="wrap">
    <div class="section-head row">
      <h2 id="how-h">How selling works</h2>
      <a class="btn" href="sell.html">Start a request</a>
    </div>
    <ol class="steps">
      <li><h3>Tell us what you have</h3><p>Send a few details and photos online. It takes about two minutes.</p></li>
      <li><h3>Get a price and a time</h3><p>We confirm a guide price and book a pickup or a drop-off.</p></li>
      <li><h3>Weighed, then paid by EFT</h3><p>Every load is weighed. Bring ID, which Victorian law requires us to record. Cash for scrap metal is banned.</p></li>
    </ol>
  </div>
</section>

<section class="band paper ruled" aria-labelledby="trade-h">
  <div class="wrap split center">
    <figure class="photo">
      <img src="assets/img/steel-bales-forklift.jpg" alt="A forklift carries a bale of compressed steel past stacked bales in a warehouse" loading="lazy">
      <figcaption>Baled steel, ready to ship.</figcaption>
    </figure>
    <div>
      <p class="kicker dark">Trade and business</p>
      <h2 id="trade-h">For workshops, builders, farms and sites</h2>
      <p class="lede">Regular metal coming off your site? We can place bins, collect on a schedule and send a statement for every load.</p>
      <div class="actions"><a class="btn ghost" href="trade.html">Trade and business</a></div>
    </div>
  </div>
</section>

<section class="band night archive-band scale" aria-labelledby="arc-h">
  <div class="wrap">
    <div class="section-head">
      <p class="kicker">From the archive</p>
      <h2 id="arc-h">The trade was here first</h2>
      <p>Robert Hyde &amp; Co. was buying and shipping Melbourne&rsquo;s cast-offs a century and a half before anyone called it recycling.</p>
    </div>
    <div class="scale-grid">
      <div>
        <p class="stat"><span class="big">500</span><span class="unit">tons a year</span></p>
        <p class="lede">of rags, zinc and broken glass, sorted in Melbourne and shipped to England by sail. <em>The Age</em>, 19 January 1863. That&rsquo;s about the weight of 330 family cars.</p>
        <p class="small muted">The car comparison is ours, at about 1.5 tonnes a car. <a href="{SRC["age1863"][1]}">Read the report on Trove</a>.</p>
      </div>
      <div class="cars" data-cars role="img" aria-label="330 small car shapes, roughly the weight of 500 tons">{CARS}</div>
    </div>
  </div>
</section>

<section class="band night ruled tn-band" aria-labelledby="tn-h">
  <div class="wrap">
    <div class="section-head">
      <h2 id="tn-h">Same street, 168 years apart</h2>
      <p>Bourke Street, looking west from Spring Street. Drag the handle to travel between about 1858 and today.</p>
    </div>
    <figure class="tn" data-tn>
      <div class="tn-frame">
        <img class="tn-now" src="assets/img/tn-bourke-today.jpg" alt="Bourke Street today, from Parliament House: trams, a yellow taxi, office towers and plane trees" loading="lazy">
        <img class="tn-then" src="assets/img/tn-bourke-1858.jpg" alt="Bourke Street about 1858 from the same corner: a wide dirt road, the Old White Hart hotel and low shopfronts" loading="lazy">
        <span class="tn-handle" aria-hidden="true"></span>
        <span class="tn-tag then" aria-hidden="true">1858</span><span class="tn-tag now" aria-hidden="true">Today</span>
        <input type="range" min="0" max="100" value="50" aria-label="Compare 1858 with today. Higher shows more of 1858.">
      </div>
      <figcaption>1858: Antoine Fauchery, State Library Victoria, public domain. Today: &ldquo;View of Bourke Street from Parliament House in Melbourne&rdquo; by Yang.square, <a href="https://commons.wikimedia.org/wiki/File:View_of_Bourke_Street_from_Parliament_House_in_Melbourne.jpg">Wikimedia Commons</a>, CC BY 2.0, cropped.</figcaption>
    </figure>
  </div>
</section>

<section class="band night ruled token-band" aria-labelledby="tok-h">
  <div class="wrap teaser">
    <div class="coin big" data-coin data-coin-drag>{token("tz", label="The 1857 token. Drag to turn it.")}</div>
    <div>
      <p class="kicker">Copper, 28 millimetres, 1857</p>
      <h2 id="tok-h">Turn the token</h2>
      <p class="lede">Hyde&rsquo;s halfpenny reads <em>General Marine Store. Shippers of rags, glass, metals &amp;c.</em> on one side, and <em>Peace &amp; Plenty</em> on the other. Ours is a simplified redraw of the original held by Museums Victoria. Drag it round.</p>
      <div class="actions"><a class="btn" href="story.html">Open the time machine</a></div>
    </div>
  </div>
</section>
'''

# ---------------------------------------------------------------- story
ERAS = [
    ("1857", "1857", "The token",
     "<p class=\"lede\">Robert Hyde &amp; Co. issues copper trade tokens, probably struck by Heaton &amp; Sons of Birmingham.</p><p>Melbourne was short of small change, and traders issued their own pennies and halfpennies. Each one doubled as an advertisement.</p>",
     '''<div class="label-card"><p class="lc-k">Museums Victoria, NU 11310 and related</p><p class="lc-t">ROBERT HYDE &amp; Co &middot; MELBOURNE<br>GENERAL MARINE STORE<br>SHIPPERS OF RAGS GLASS METALS &amp;c.</p><dl><div><dt>Material</dt><dd>Copper</dd></div><div><dt>Size</dt><dd>28 mm halfpenny, 34 mm penny</dd></div><div><dt>Reverse</dt><dd>Peace &amp; Plenty, Advance Australia</dd></div></dl></div>''',
     src("mv1857")),
    ("1861", "1861", "A second issue",
     "<p class=\"lede\">A second run of tokens is struck. Hyde&rsquo;s Marine Store advertises in <em>The Argus</em> from Albert Street, East Melbourne.</p>",
     f'''<figure class="era-fig"><img src="assets/img/bourke-st-1858.jpg" alt="Sepia photograph of a wide, unpaved Bourke Street with two-storey shops and the Old White Hart hotel on the corner" loading="lazy"><figcaption>{esc(CREDIT["bourke"])}</figcaption></figure>''',
     src("mv1861", "argus1861")),
    ("1862", "1862", "In the directory",
     "<p class=\"lede\">Hyde&rsquo;s Marine Store appears in a Melbourne directory for the first time, at 11 Albert Street, East Melbourne.</p>",
     '''<div class="dir-card" aria-label="Recreated directory listing"><p class="dc-h">Melbourne Directory &middot; 1862</p><p class="dc-row"><span>Hyde, Robert, &amp; Co.</span><i></i><span>marine store, 11 Albert st. E.</span></p><p class="dc-note">Our recreation of the listing as recorded by Museums Victoria, not a scan of the page.</p></div>''',
     src("mvart")),
    ("1863", "1863", "Shipping to England",
     "<p class=\"lede\"><em>The Age</em> describes Hyde&rsquo;s as Melbourne&rsquo;s principal rag exporter, sending about 500 tons of rags a year to England, along with zinc and broken glass.</p><p>From 1863 to 1865, Hyde trades in partnership with Richard Hodgson as Hyde, Hodgson &amp; Co.</p>",
     f'''<figure class="era-fig"><img src="assets/img/ships-railway-pier-1875.jpg" alt="Sepia photograph of a long pier lined with tall-masted sailing ships, a steam locomotive and goods wagons on the rails between them" loading="lazy"><figcaption>{esc(CREDIT["ships"])}</figcaption></figure>''',
     src("age1863", "mvart")),
    ("1868", "1868", "Rags, then metal again",
     "<p class=\"lede\">The business is listed as a rag merchant in 1868, then as a marine store again in 1869 and 1870.</p>",
     f'''<figure class="era-fig"><img src="assets/img/gpo-1868.jpg" alt="Sepia photograph of Melbourne's new General Post Office, an ornate two-storey building with a clock tower, on an empty corner" loading="lazy"><figcaption>{esc(CREDIT["gpo"])}</figcaption></figure>''',
     src("mvart", "auction1869")),
    ("1872", "1872", "The last trace",
     "<p class=\"lede\">The last record found of the business is R. Hyde, Little Bourke Street.</p>",
     ARCHIVE,
     src("trove1872")),
    ("1878", "1878", "Probate",
     "<p class=\"lede\">Probate is granted for a Robert Hyde of Richmond, marine store dealer, very likely the same man. No successor business has been found.</p>",
     '''<div class="doc-card"><p class="dk">Public Record Office Victoria</p><p class="dt">Probate and administration files</p><p class="dd">VPRS 28 &middot; 17/144</p><p class="dn">Robert Hyde, Richmond, marine store dealer</p><p class="dc-note">The file is listed in the PROV catalogue; we haven&rsquo;t viewed it yet.</p></div>''',
     src("prov")),
    ("today", "Today", "The name, revived",
     "<p class=\"lede\">Robert Hyde &amp; Co. is a new business carrying an old name. We aren&rsquo;t the original firm and we don&rsquo;t claim its years.</p><p class=\"quote\">The firm is gone. The trade isn&rsquo;t.</p><p>What we share is the trade: buying old metal and sending it back into use. We took up the name because it had fallen out of use, and because its story is a reminder that recycling in Melbourne is older than the word.</p><div class=\"actions\"><a class=\"btn\" href=\"sell.html\">Get a price for your scrap</a></div>",
     '''<figure class="era-fig colour"><img src="assets/img/bales-into-container.jpg" alt="A forklift loads a bale of compressed steel into a shipping container stacked with bales" loading="lazy"><figcaption>Baled steel going into a shipping container.</figcaption></figure>''',
     ""),
]

era_nav = "".join(f'<li><a href="#{slug}" data-era-link="{slug}">{year}</a></li>' for slug, year, *_ in ERAS)
eras_html = "".join(f'''<section class="era" id="{slug}" data-era="{slug}" data-year="{year}" aria-labelledby="h-{slug}">
  <p class="era-year" aria-hidden="true">{year}</p>
  <h2 id="h-{slug}">{title}</h2>
  {body}
  {artefact}
  {f'<p class="src">Source: {s}</p>' if s else ''}
</section>''' for slug, year, title, body, artefact, s in ERAS)


# ---------------------------------------------------------------- v3: Hyde's Melbourne map + pier slider
PINS = [
  ("1862", "Albert Street, East Melbourne", "Hyde&rsquo;s Marine Store, 11 Albert Street. First listed in a directory in 1862, and listed here again in 1866 and 1867.", 79.7, 18.3),
  ("1863", "Railway Pier, Sandridge", "Where Melbourne&rsquo;s exports met the ships. <em>The Age</em> reported Hyde&rsquo;s sending about 500 tons of rags a year to England; we don&rsquo;t know which pier was used.", 55.6, 56.3),
  ("1863&ndash;65", "Albert Street, Emerald Hill", "Listed in partnership with Richard Hodgson as Hyde, Hodgson &amp; Co.", 66.0, 43.4),
  ("1868", "Lonsdale Street West", "Listed as a rag merchant at 120 Lonsdale Street West.", 65.6, 19.0),
  ("1872", "Little Bourke Street", "The last record found of the business: R. Hyde, Little Bourke Street.", 70.9, 21.4),
  ("1878", "Richmond", "Probate granted for a Robert Hyde of Richmond, marine store dealer.", 89.8, 28.6),
]
pins_html = "".join(f'<button class="hm-pin" type="button" style="left:{x}%;top:{y}%" aria-label="{w.replace("&ndash;", " to ")}: {n}" aria-pressed="false"><span>{w}</span></button>' for w, n, d, x, y in PINS)
list_html = "".join(f'<li data-pin-item data-when="{w}"><button type="button"><em>{w}</em><b>{n}</b><span>{d}</span></button></li>' for w, n, d, x, y in PINS)
MAP = f"""
<section class="band night" aria-labelledby="map-h">
  <div class="wrap">
    <div class="section-head">
      <h2 id="map-h">Hyde&rsquo;s Melbourne</h2>
      <p>Every address the record gives for the business, pinned on an Admiralty chart of 1864. Zoom, drag, or choose a place from the list.</p>
    </div>
    <div class="hmap-grid">
      <div class="hmap" data-hmap>
        <div class="hm-view" tabindex="0" role="region" aria-label="Chart of Melbourne and Hobsons Bay, 1864, with Hyde&rsquo;s addresses pinned. Arrow keys pan, plus and minus zoom.">
          <div class="hm-canvas">
            <img src="assets/img/hobsons-bay-chart-1864.jpg" alt="" draggable="false">
            {pins_html}
          </div>
        </div>
        <div class="hm-ctrls"><button type="button" data-zoom-in aria-label="Zoom in">+</button><button type="button" data-zoom-out aria-label="Zoom out">&minus;</button><button type="button" class="reset" data-zoom-reset aria-label="Reset the map">Reset</button></div>
        <div class="hm-panel" aria-live="polite"></div>
      </div>
      <div>
        <ol class="hm-list">{list_html}</ol>
        <p class="hm-note">Pins are placed by us and are approximate. {esc(CREDIT["chart"])}</p>
      </div>
    </div>
  </div>
</section>

<section class="band paper tn-band" aria-labelledby="pier-h">
  <div class="wrap">
    <div class="section-head">
      <h2 id="pier-h">The pier, then and now</h2>
      <p>Sandridge about 1858, where ships for England tied up, and the same shore at Port Melbourne today. Drag to compare.</p>
    </div>
    <figure class="tn" data-tn>
      <div class="tn-frame">
        <img class="tn-now" src="assets/img/tn-pier-today.jpg" alt="Port Melbourne today: grassy dunes, the beach, and cruise ships and the Spirit of Tasmania at Station Pier under a cloudy sky" loading="lazy">
        <img class="tn-then" src="assets/img/tn-pier-1858.jpg" alt="Sandridge about 1858: a long timber railway pier, sailing ships in the bay and timber cottages on the sand" loading="lazy">
        <span class="tn-handle" aria-hidden="true"></span>
        <span class="tn-tag then" aria-hidden="true">1858</span><span class="tn-tag now" aria-hidden="true">Today</span>
        <input type="range" min="0" max="100" value="50" aria-label="Compare 1858 with today. Higher shows more of 1858.">
      </div>
      <figcaption>1858: Richard Daintree and Antoine Fauchery, State Library Victoria, public domain. Today: &ldquo;Station Pier Melbourne 20191106&rdquo; by JoeHard, <a href="https://commons.wikimedia.org/wiki/File:Station_Pier_Melbourne_20191106.jpg">Wikimedia Commons</a>, CC BY-SA 4.0, cropped.</figcaption>
    </figure>
  </div>
</section>
"""

story = page_hero("bourke-st-1858.jpg", "The time machine",
    "Seven stops in the life of a Melbourne marine store, and an eighth for why we took up its name. Scroll, or jump to a year. Each stop links to the source we used.",
    CREDIT["bourke"], "50% 60%", depth=0.42) + f'''
<div class="tm2 night">
  <div class="wrap tm2-grid">
    <aside class="tm2-side" aria-label="Years">
      <div class="coin" data-coin data-story-coin>{token("tm", label="The 1857 token. It turns as you travel through the years.")}</div>
      <p class="tm2-year" aria-hidden="true">1857</p>
      <ol class="tm2-nav">{era_nav}</ol>
    </aside>
    <div class="tm2-eras">{eras_html}</div>
  </div>
</div>

{MAP}
<section class="band paper ruled" aria-labelledby="ms-h">
  <div class="wrap split center">
    <div>
      <h2 id="ms-h">What was a marine store?</h2>
      <p class="lede" style="margin-top:1rem">In colonial Melbourne, a marine store dealer bought and sold second-hand goods and scrap: old rope and ships&rsquo; stores, bottles, rags, bones and metal.</p>
      <p>Nobody can claim to be Victoria&rsquo;s first. Unnamed marine stores appear in Melbourne papers from 1841, and a named dealer, Blackmore of Bourke Street, by 1848. Hyde&rsquo;s is one of the early marine stores that left a documented trail: tokens, advertisements, directory listings and a newspaper report on its trade.</p>
    </div>
    <figure class="photo">
      <img src="assets/img/hobsons-bay-chart-1864.jpg" alt="Admiralty chart of Hobsons Bay and the Yarra River, showing Melbourne, Williamstown and Sandridge" loading="lazy">
      <figcaption>{esc(CREDIT["chart"])}</figcaption>
    </figure>
  </div>
</section>

<section class="band paper ruled" aria-labelledby="src-h">
  <div class="wrap">
    <h2 id="src-h" style="margin-bottom:1.25rem">Sources</h2>
    <ol class="sources">
      {''.join(f'<li><a href="{u}">{esc(t)}</a></li>' for t, u in SRC.values())}
      <li>Historic photographs and chart: State Library Victoria collection, public domain, via Wikimedia Commons.</li>
    </ol>
  </div>
</section>
'''

# ---------------------------------------------------------------- what we buy
ITEMS = [
    ("steel", "Steel and iron", "Fridges and freezers", "Clean and empty. Keep the pipes uncut: the refrigerant is recovered by an ARC-licensed technician before processing."),
    ("steel", "Steel and iron", "Hot water services", "Drained and already disconnected by a plumber. Heat-pump units: tell us, as the refrigerant must be recovered first."),
    ("steel", "Steel and iron", "Washing machines, dryers and stoves", "Empty. No gas bottles attached."),
    ("steel", "Steel and iron", "Roofing iron, fencing and gates", "Already taken down. No fibro or cement sheet mixed in."),
    ("steel", "Steel and iron", "Shelving, racking and filing cabinets", "Empty. Pallet racking welcome."),
    ("steel", "Steel and iron", "Pipe, angle, beams and offcuts", "Any length. Tell us if pieces are over 6 metres."),
    ("steel", "Steel and iron", "Cast-iron baths, sinks and BBQs", "BBQ gas bottles removed and kept by you."),
    ("steel", "Steel and iron", "Bikes, frames and tools", "No e-bikes or lithium batteries."),
    ("nonferrous", "Copper, brass and aluminium", "Copper pipe, wire and cylinders", "Stripped or unstripped. Clean copper fetches more."),
    ("nonferrous", "Copper, brass and aluminium", "Brass taps and fittings", "Remove plastic and steel parts where you can."),
    ("nonferrous", "Copper, brass and aluminium", "Aluminium window frames and sheet", "Glass removed if possible."),
    ("nonferrous", "Copper, brass and aluminium", "Stainless steel sinks and troughs", "Taps can stay on."),
    ("nonferrous", "Copper, brass and aluminium", "Electric motors and radiators", "Drained of fluids."),
    ("vehicles", "Cars, trailers and caravans", "Car bodies and broken-down cars", "Proof of ownership needed. Tilt-tray access required."),
    ("vehicles", "Cars, trailers and caravans", "Trailers", "Any condition. Registration papers if you have them."),
    ("vehicles", "Cars, trailers and caravans", "Old caravans", "Older caravans may contain asbestos. Tell us the build year; we may need a clearance before we can take it."),
    ("vehicles", "Cars, trailers and caravans", "Boats and boat trailers", "Ask first. Fuel tanks must be empty."),
    ("farm", "Machinery and farm metal", "Old farm equipment", "Ploughs, harrows, tanks and frames. Fluids drained."),
    ("farm", "Machinery and farm metal", "Shipping containers and site offices", "Tell us the size and how a truck gets to it."),
    ("farm", "Machinery and farm metal", "Car and farm wheels", "Ask about tyres still on rims."),
    ("farm", "Machinery and farm metal", "Warehouse shelving and steel structures", "Dismantled, or ask us about dismantling."),
    ("batteries", "Batteries", "Lead-acid car and truck batteries", "Intact and carried upright. Not lithium."),
]
FILTERS = [("all", "All"), ("steel", "Steel and iron"), ("nonferrous", "Copper, brass and aluminium"), ("vehicles", "Vehicles"), ("farm", "Machinery and farm"), ("batteries", "Batteries")]
items_html = "".join(f'<li data-kind="{k}"><span class="kind">{esc(kl)}</span><h3>{esc(n)}</h3><p>{esc(d)}</p></li>' for k, kl, n, d in ITEMS)
chips_html = "".join(f'<li><button class="chip" type="button" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{esc(l)}</button></li>' for k, l in FILTERS)

buy = f'''
{page_hero("hobsons-bay-chart-1864.jpg", "What we buy", "Most things made of metal. We price by metal type, grade and weight on the day, so ask for today&rsquo;s rate.", CREDIT["chart"], "62% 30%")}
<section class="wrap band tight" aria-label="Items we buy">
  <h2 class="sr">Items we buy</h2>
  <ul class="chips" aria-label="Filter by material">{chips_html}</ul>
  <p class="count" data-count aria-live="polite"></p>
  <ul class="items">{items_html}</ul>
</section>
<section class="band on-zinc2" aria-labelledby="ask-h">
  <div class="wrap notes">
    <div>
      <h2 id="ask-h" style="font-size:var(--step-2)">Ask us first</h2>
      <ul>
        <li>Gas cylinders of any kind, including BBQ bottles and fire extinguishers</li>
        <li>Lithium batteries, e-bikes and e-scooters</li>
        <li>Metal e-waste such as computers and power tools</li>
        <li>Tyres still on rims</li>
      </ul>
    </div>
    <div>
      <h2 style="font-size:var(--step-2)">We can&rsquo;t take</h2>
      <ul>
        <li>Anything with asbestos, or suspected asbestos</li>
        <li>Drums or containers with liquid or residue in them</li>
        <li>Fuel tanks or engines that haven&rsquo;t been drained</li>
        <li>General rubbish, timber, mattresses or green waste</li>
      </ul>
    </div>
  </div>
</section>
<section class="band" aria-labelledby="price-h">
  <div class="wrap split">
    <div>
      <h2 id="price-h">How we price</h2>
      <p class="lede" style="margin-top:1rem">Metal prices move every day with the commodity markets, so we don&rsquo;t publish a fixed list.</p>
      <p>Send us photos and a rough amount and we&rsquo;ll give you a guide price. The final figure comes from the weighed load, by metal and grade. Clean, sorted metal is worth more: copper with the plastic stripped off, aluminium without steel screws, brass without taps attached.</p>
      <div class="actions"><a class="btn" href="sell.html">Get a price</a></div>
    </div>
    <figure class="photo">
      <img src="assets/img/granulated-copper.jpg" width="800" height="600" alt="Plastic tubs full of small granules of recovered copper">
      <figcaption>Granulated copper, sorted from the rest of the load.</figcaption>
    </figure>
  </div>
</section>
'''

# ---------------------------------------------------------------- sell (multi-step)
MATS = [("steel", "Steel and iron", "Whitegoods, roofing, shelving"), ("copper", "Copper", "Pipe, wire, cylinders"),
        ("brass", "Brass", "Taps, fittings"), ("aluminium", "Aluminium", "Frames, sheet"),
        ("stainless", "Stainless steel", "Sinks, troughs"), ("vehicle", "Car, trailer or caravan", "Proof of ownership needed"),
        ("farm", "Machinery or farm metal", "Equipment, containers"), ("batteries", "Lead-acid batteries", "Car and truck")]
AMOUNTS = [("boot", "A car boot or less", ""), ("ute", "A ute or trailer load", ""), ("truck", "A truck load or more", ""), ("ongoing", "Ongoing, from a business", "We'll talk about regular collections")]

def pick(name, opts, kind="checkbox"):
    return "".join(
        f'<label><input type="{kind}" name="{name}" value="{v}"{(' required data-msg="' + ("Choose how much you have." if name == "amount" else "Choose pickup or drop-off.") + '"') if kind == "radio" and i == 0 else ""}><span><b>{esc(t)}</b>{f"<small>{esc(s)}</small>" if s else ""}</span></label>'
        for i, (v, t, s) in enumerate(opts))

sell = f'''
{page_hero("loose-steel.jpg", "Get a price for your scrap", "Tell us what you have and we&rsquo;ll come back with a guide price and a time. It takes about two minutes.", "Loose steel after separation, before baling.", "50% 50%", "colour")}
<div class="wrap band tight">
  <div class="form-wrap">
    <div class="panel">
      <ol class="progress" aria-label="Progress">
        <li><span>Your metal</span></li><li><span>Where</span></li><li><span>Photos</span></li><li><span>Your details</span></li><li><span>Check and send</span></li>
      </ol>
      <p class="stepline" data-stepline aria-live="polite"></p>
      <form data-steps novalidate>
        <p class="restored" data-restored hidden>We&rsquo;ve kept what you entered last time.</p>
        <fieldset class="step">
          <legend>What do you have?</legend>
          <p class="hint">Choose everything that applies.</p>
          <div class="pick" data-min-one="materials" data-msg="Choose at least one type of metal.">{pick("materials", MATS)}</div>
          <p class="err" id="materials-err" role="alert"></p>
          <div class="field">
            <label for="other">Anything else to mention? <span class="opt">(optional)</span></label>
            <input type="text" id="other" name="other" placeholder="For example: an old ute, 20 metres of copper pipe">
          </div>
          <div class="field">
            <span class="label" id="amount-l">Roughly how much?</span>
            <div class="pick" role="radiogroup" aria-labelledby="amount-l">{pick("amount", AMOUNTS, "radio")}</div>
            <p class="err" id="amount-err" role="alert"></p>
          </div>
        </fieldset>

        <fieldset class="step" hidden>
          <legend>Pickup or drop-off?</legend>
          <p class="hint">Pickups depend on the amount and your area. We&rsquo;ll confirm when we call.</p>
          <div class="field">
            <div class="pick" role="radiogroup" aria-label="Pickup or drop-off">{pick("method", [("pickup", "Pick it up from me", "Truck depends on the load"), ("dropoff", "I'll drop it off", "We'll send the yard address")], "radio")}</div>
            <p class="err" id="method-err" role="alert"></p>
          </div>
          <div class="row2">
            <div class="field"><label for="suburb">Suburb or town</label><input type="text" id="suburb" name="suburb" required autocomplete="address-level2" data-msg="Enter your suburb or town."><p class="err" id="suburb-err"></p></div>
            <div class="field"><label for="postcode">Postcode</label><input type="text" id="postcode" name="postcode" inputmode="numeric" maxlength="4" required data-postcode autocomplete="postal-code" data-msg="Enter your postcode."><p class="err" id="postcode-err"></p></div>
          </div>
          <div data-when="pickup" hidden>
            <div class="field"><label for="access">How do we get to it? <span class="opt">(optional)</span></label>
            <textarea id="access" name="access" placeholder="Driveway, backyard, upstairs, gate width, anything a truck needs to know"></textarea></div>
          </div>
        </fieldset>

        <fieldset class="step" hidden>
          <legend>Add some photos</legend>
          <p class="hint">Photos help us price it right first time. Up to six. You can skip this. Photos aren&rsquo;t saved if you leave the page.</p>
          <div class="field">
            <label for="photos">Choose photos <span class="opt">(optional)</span></label>
            <input type="file" id="photos" accept="image/*" multiple>
            <p class="small muted" data-photo-count aria-live="polite"></p>
            <div class="thumbs"></div>
          </div>
        </fieldset>

        <fieldset class="step" hidden>
          <legend>Your details</legend>
          <p class="hint">We&rsquo;ll call or text to confirm the price and a time.</p>
          <div class="field"><label for="name">Full name</label><input type="text" id="name" name="name" required autocomplete="name" data-msg="Enter your name."><p class="err" id="name-err"></p></div>
          <div class="row2">
            <div class="field"><label for="phone">Mobile</label><input type="tel" id="phone" name="phone" required autocomplete="tel" data-msg="Enter a mobile number so we can confirm."><p class="err" id="phone-err"></p></div>
            <div class="field"><label for="email">Email <span class="opt">(optional)</span></label><input type="email" id="email" name="email" autocomplete="email"><p class="err" id="email-err"></p></div>
          </div>
          <div class="field"><label for="notes">Best time to call, or anything else <span class="opt">(optional)</span></label><textarea id="notes" name="notes"></textarea></div>
          <label class="checkline"><input type="checkbox" name="idok" value="yes" required data-msg="Tick to confirm you can show ID."> I can show ID when the metal is weighed, and I&rsquo;m happy to be paid by EFT.</label>
          <p class="err" id="idok-err" role="alert"></p>
        </fieldset>

        <fieldset class="step" hidden>
          <legend>Check and send</legend>
          <p class="hint">Make sure this is right, then send it.</p>
          <dl class="review" data-review></dl>
          <p class="err" data-send-err role="alert"></p>
        </fieldset>

        <div class="form-nav">
          <button class="btn ghost" type="button" data-back hidden>Back</button>
          <span></span>
          <button class="btn" type="button" data-next>Continue</button>
          <button class="btn" type="submit" data-submit hidden>Send request</button>
        </div>
      </form>
      <div class="done-card" data-done hidden>
        <h2>Request sent. Thanks, <span data-done-name></span>.</h2>
        <p class="muted">Your reference</p>
        <p class="ref"></p>
        <p>We aim to call or text within one business day with a guide price and a time. Keep your reference handy.</p>
        <p class="callout warn small" data-done-proto>This is a prototype, so nothing was actually sent. In the live site this request goes straight to the team.</p>
        <div class="actions"><a class="btn ghost" href="what-we-buy.html">See what we buy</a><a class="btn ghost" href="index.html">Back to home</a></div>
      </div>
    </div>
    <aside class="aside" aria-labelledby="bring-h">
      <h2 id="bring-h">Before you sell</h2>
      <div class="callout"><p><b>Bring ID.</b> Victorian scrap metal law means we record the seller&rsquo;s name, address and identification for every purchase. A driver licence is easiest.</p></div>
      <div class="callout"><p><b>Paid by EFT.</b> Cash payments for scrap metal are banned in Victoria, so we pay straight into your account.</p></div>
      <div class="callout warn"><p><b>Keep hazards out of the load.</b> Ask us first about gas bottles and lithium batteries, and drain any fuel. <a href="what-we-buy.html">See what we can&rsquo;t take</a>.</p></div>
    </aside>
  </div>
</div>
'''

# ---------------------------------------------------------------- trade
trade = f'''
{page_hero("bales-into-container.jpg", "Trade and business", "For businesses with metal coming off site every week: workshops, builders, farms, manufacturers and facilities.", "Baled steel going into a shipping container.", "50% 55%", "colour", '<ul class="sectors"><li>Workshops and fabricators</li><li>Builders and demolition</li><li>Farms</li><li>Manufacturers</li><li>Property and facilities</li></ul>')}
<section class="band tight" aria-labelledby="offer-h">
  <div class="wrap">
    <h2 id="offer-h" class="sr">What we offer</h2>
    <div class="offer">
      <div><h3>Bins and cages on site</h3><p>We size the bin to your space and your volume, and swap it when it&rsquo;s full.</p></div>
      <div><h3>Collections on a schedule</h3><p>Weekly, fortnightly or monthly runs, or a call-out when you need one.</p></div>
      <div><h3>Strip-outs and one-off clear-outs</h3><p>Old racking, plant and structures at the end of a job or a lease.</p></div>
      <div><h3>A statement for every load</h3><p>Each load is weighed and recorded by metal and grade, and paid by EFT.</p></div>
    </div>
  </div>
</section>
<section class="band on-zinc2" aria-labelledby="enq-h">
  <div class="wrap form-wrap">
    <div class="panel">
      <h2 id="enq-h" style="font-size:var(--step-2);margin-bottom:.4rem">Tell us about your site</h2>
      <p class="hint">We&rsquo;ll come back with a plan and a rate.</p>
      <form data-simple="trade" data-done="trade-done" data-prefix="RHT" novalidate>
        <div class="row2">
          <div class="field"><label for="t-company">Business name</label><input type="text" id="t-company" name="company" required autocomplete="organization" data-msg="Enter your business name."><p class="err" id="company-err"></p></div>
          <div class="field"><label for="t-contact">Your name</label><input type="text" id="t-contact" name="contact" required autocomplete="name" data-msg="Enter your name."><p class="err" id="contact-err"></p></div>
        </div>
        <div class="row2">
          <div class="field"><label for="t-phone">Phone</label><input type="tel" id="t-phone" name="tphone" required autocomplete="tel" data-msg="Enter a phone number."><p class="err" id="tphone-err"></p></div>
          <div class="field"><label for="t-email">Email</label><input type="email" id="t-email" name="temail" required autocomplete="email" data-msg="Enter an email address."><p class="err" id="temail-err"></p></div>
        </div>
        <div class="row2">
          <div class="field"><label for="t-suburb">Site suburb</label><input type="text" id="t-suburb" name="tsuburb" required data-msg="Enter the site's suburb."><p class="err" id="tsuburb-err"></p></div>
          <div class="field"><label for="t-freq">How often?</label>
            <select id="t-freq" name="freq" required data-msg="Choose how often."><option value="">Choose one</option><option>Weekly</option><option>Fortnightly</option><option>Monthly</option><option>One-off clear-out</option><option>Not sure yet</option></select><p class="err" id="freq-err"></p></div>
        </div>
        <div class="field"><label for="t-what">What metal, and roughly how much?</label><textarea id="t-what" name="what" required data-msg="Tell us a little about the metal." placeholder="For example: steel offcuts, about one tonne a month"></textarea><p class="err" id="what-err"></p></div>
        <p class="err" data-send-err role="alert"></p>
        <button class="btn" type="submit">Send enquiry</button>
      </form>
      <div class="done-card" id="trade-done" hidden>
        <h2>Enquiry sent.</h2>
        <p class="muted">Your reference</p><p class="ref"></p>
        <p>We aim to be in touch within one business day.</p>
        <p class="callout warn small" data-done-proto>This is a prototype, so nothing was actually sent.</p>
      </div>
    </div>
    <figure class="photo">
      <img src="assets/img/bales-into-container.jpg" width="1400" height="787" alt="A forklift loads a bale of compressed steel into a shipping container already stacked with bales">
      <figcaption>Baled steel going into a shipping container.</figcaption>
    </figure>
  </div>
</section>
'''

# ---------------------------------------------------------------- faq
FAQ = [
    ("Selling", [
        ("Do you pay cash?", "No. Victorian law bans cash payments for scrap metal, and we pay by EFT into your bank account."),
        ("Why do you need my ID?", "Victoria's scrap metal laws require us to record the seller's name, address and identification, with a description and the weight, for every purchase. A driver licence is easiest, but other ID can be accepted."),
        ("How do you work out the price?", "By metal type, grade and weight on the day. Prices follow the commodity markets, so we give you a guide price first and the final figure comes from the weighed load."),
        ("Is there a minimum amount?", "Not for drop-offs. For pickups it depends on the amount and how far away you are. We'll tell you when we call."),
    ]),
    ("What we take", [
        ("Do you take fridges and air conditioners?", "Yes. Fridges and freezers should be clean and empty with the pipes uncut, and the refrigerant is recovered by an ARC-licensed technician before the metal is processed. Air conditioners must be decommissioned and removed by an ARC-licensed technician first."),
        ("Do you take car bodies?", "Yes, with proof of ownership and clear access for a tilt tray."),
        ("What about gas bottles and lithium batteries?", "Ask us first. Both are fire risks in a metal load, so they're handled separately or not at all. Never put them in with other scrap."),
        ("Do you take asbestos?", "No. If we suspect asbestos, for example in an old caravan or shed panels, we won't load it until it has been cleared."),
    ]),
    ("The name", [
        ("Are you the original Robert Hyde & Co.?", "No. The original was a Melbourne marine store dealer active from the 1850s to the 1870s. We're a new business that has taken up the name, and we don't claim its history as our own trading record."),
        ("Why revive the name?", "Because the trade is the same: buying old metal and sending it back into use. Hyde's left a clear record of that work in Melbourne, and the name had fallen out of use. The time machine on our story page tells it stop by stop."),
        ("What was a marine store?", "A colonial dealer in second-hand goods and scrap: rope and ships' stores, bottles, rags, bones and metal."),
    ]),
]
faq_html = "".join(
    f'<div class="faq-group"><h2>{esc(g)}</h2><div class="faq">' +
    "".join(f'<details><summary>{esc(q)}</summary><div class="a"><p>{esc(a)}</p></div></details>' for q, a in qs) +
    '</div></div>' for g, qs in FAQ)
faq_ld = '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[' + ",".join(
    '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}' % (__import__("json").dumps(q), __import__("json").dumps(a))
    for g, qs in FAQ for q, a in qs) + ']}'
faq = f'''
{page_hero("gpo-1868.jpg", "Questions", "Selling, what we take, and the name. <a href=\"contact.html\">Ask us</a> if yours isn&rsquo;t here.", CREDIT["gpo"], "50% 40%")}
<div class="wrap band tight faq-wrap">
  <div>{faq_html}</div>
  <aside class="aside" aria-label="Selling scrap">
    <div class="callout"><h2 style="font-size:var(--step-1);margin-bottom:.5rem">Ready to sell?</h2><p>Tell us what you have and we&rsquo;ll come back with a guide price.</p><p style="margin-top:1rem"><a class="btn" href="sell.html">Get a price</a></p></div>
  </aside>
</div>
'''

# ---------------------------------------------------------------- contact
contact = f'''
{page_hero("english-mail-day-1862.jpg", "Contact", "Selling scrap? <a href=\"sell.html\">Get a price</a> is the quickest way. For anything else, send us a message. (In 1862 you&rsquo;d have queued at the Post Office for the English mail.)", CREDIT["mail"], "50% 45%", "paint")}
<div class="wrap band tight">
  <div class="form-wrap">
    <div class="panel">
      <form data-simple="contact" data-done="contact-done" data-prefix="RHC" novalidate>
        <div class="field"><label for="c-name">Name</label><input type="text" id="c-name" name="cname" required autocomplete="name" data-msg="Enter your name."><p class="err" id="cname-err"></p></div>
        <div class="row2">
          <div class="field"><label for="c-email">Email</label><input type="email" id="c-email" name="cemail" required autocomplete="email" data-msg="Enter your email so we can reply."><p class="err" id="cemail-err"></p></div>
          <div class="field"><label for="c-phone">Phone <span class="opt">(optional)</span></label><input type="tel" id="c-phone" name="cphone" autocomplete="tel"><p class="err" id="cphone-err"></p></div>
        </div>
        <div class="field"><label for="c-msg">Message</label><textarea id="c-msg" name="cmsg" required data-msg="Write a message."></textarea><p class="err" id="cmsg-err"></p></div>
        <p class="err" data-send-err role="alert"></p>
        <button class="btn" type="submit">Send message</button>
      </form>
      <div class="done-card" id="contact-done" hidden>
        <h2>Message sent.</h2>
        <p class="muted">Your reference</p><p class="ref"></p>
        <p>We aim to reply within one business day.</p>
        <p class="callout warn small" data-done-proto>This is a prototype, so nothing was actually sent.</p>
      </div>
    </div>
    <aside class="aside">
      <h2>Find us</h2>
      <dl class="dl">
        <div><dt>Phone</dt><dd>To be confirmed<span class="tbc">TBC</span></dd></div>
        <div><dt>Email</dt><dd>hello@roberthyde.com.au<span class="tbc">TBC</span></dd></div>
        <div><dt>Yard</dt><dd>Address to be confirmed<span class="tbc">TBC</span></dd></div>
        <div><dt>Hours</dt><dd>To be confirmed<span class="tbc">TBC</span></dd></div>
      </dl>
    </aside>
  </div>
</div>
'''

lost = f'''
<div class="wrap band">
  <div class="lost">
    <div class="coin" data-coin data-coin-idle>{token("lt", label="The 1857 token")}</div>
    <div>
      <h1>This page has gone back in time</h1>
      <p class="lede" style="margin-top:1rem">We couldn&rsquo;t find it. Try one of these instead.</p>
      <div class="actions"><a class="btn" href="index.html">Home</a><a class="btn ghost" href="what-we-buy.html">What we buy</a><a class="btn ghost" href="story.html">Our story</a></div>
    </div>
  </div>
</div>
'''

ORG_LD = '<script type="application/ld+json">{"@context":"https://schema.org","@type":"LocalBusiness","name":"Robert Hyde & Co.","description":"Scrap metal buyers in Victoria, reviving the name of a Melbourne marine store from 1857.","url":"%s","areaServed":"Victoria, Australia","paymentAccepted":"Bank transfer"}</script>' % SITE_URL

write("index.html", page("index.html", "Home", "Scrap metal buyers in Victoria, reviving the name of an 1857 Melbourne marine store. Steel, copper, brass, aluminium, cars and farm metal. Get a price online.", home, ORG_LD, cls="home", motion=True))
write("story.html", page("story.html", "Our story", "The time machine: seven stops in the life of Robert Hyde & Co., a Melbourne marine store from 1857, and why we took up its name.", story, motion=True))
write("what-we-buy.html", page("what-we-buy.html", "What we buy", "The scrap metal we buy: steel, copper, brass, aluminium, cars, trailers, farm machinery and lead-acid batteries. Plus what we can't take.", buy))
write("sell.html", page("sell.html", "Get a price", "Tell us what scrap metal you have and get a guide price and a pickup or drop-off time. Bring ID; paid by EFT.", sell))
write("trade.html", page("trade.html", "Trade and business", "Scrap metal bins, scheduled collections and statements for workshops, builders, farms and manufacturers.", trade))
write("faq.html", page("faq.html", "FAQ", "Answers on selling scrap metal in Victoria: ID, EFT payment, pricing, what we take, and the Robert Hyde & Co. name.", faq, f'<script type="application/ld+json">{faq_ld}</script>'))
write("contact.html", page("contact.html", "Contact", "Contact Robert Hyde & Co., scrap metal buyers.", contact))
write("404.html", page("404.html", "Page not found", "Page not found.", lost, motion=True))

# favicon
with open(os.path.join(ROOT, "assets", "favicon.svg"), "w") as f:
    f.write(mark("fv").replace('class="token"', 'xmlns="http://www.w3.org/2000/svg"').replace('class="face"', 'fill="#A65A28"').replace('class="bead"', 'fill="#5A2E12"').replace('class="line"', 'fill="none" stroke="#3B1E0C"').replace('<text ', '<text font-family="Georgia,serif" font-weight="700" fill="#2B1408" '))
with open(os.path.join(ROOT, "robots.txt"), "w") as f:
    f.write("User-agent: *\nDisallow: /\n# Prototype: switch to 'Allow: /' and add the sitemap at launch.\n")
with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
            "".join(f"  <url><loc>{SITE_URL}/{'' if h == 'index.html' else h}</loc></url>\n" for h in [n[0] for n in NAV] + ["sell.html"]) + "</urlset>\n")
open(os.path.join(ROOT, ".nojekyll"), "w").close()
print("built")
