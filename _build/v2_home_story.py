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

def page_hero(img, h1, lede, credit, pos="50% 50%", tone="sepia", extra=""):
    return f'''<header class="phero {tone}">
  <img class="phero-bg" src="assets/img/{img}" alt="" style="object-position:{pos}">
  <div class="wrap phero-in">
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
    {extra}
  </div>
  <p class="credit wrap">{esc(credit)}</p>
</header>'''

CARS = "".join('<i></i>' for _ in range(330))

home = f'''
<section class="cine" id="cine" aria-label="From 1858 to today">
  <div class="cine-stage">
    <div class="scene s1">
      <img class="bg sepia" src="assets/img/sandridge-pier-1858-hero.jpg" alt="Sepia photograph of Hobsons Bay about 1858: a long timber pier, sailing ships at anchor, and timber cottages on the sandy shore" fetchpriority="high">
      <div class="scrim"></div>
      <div class="wrap copy">
        <p class="kicker">Melbourne, about 1858</p>
        <h1>Before it was called recycling, it was called a marine store.</h1>
        <p class="lede">Marine store dealers bought old metal, rags and glass, sorted it, and shipped it to England. One of them traded as Robert Hyde &amp; Co.</p>
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
          <p class="lede">Hyde&rsquo;s Marine Store is listed at 11 Albert Street, East Melbourne. A year later <em>The Age</em> calls it the colony&rsquo;s principal rag exporter.</p>
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

<section class="band scale" aria-labelledby="scale-h">
  <div class="wrap scale-grid">
    <div>
      <p class="kicker dark">The Age, 19 January 1863</p>
      <h2 id="scale-h"><span class="big">500 tons</span> of rags a year, shipped to England.</h2>
      <p class="lede">That was Hyde&rsquo;s trade in 1863, along with zinc and broken glass, sorted in Melbourne by a team of sorters and sent to England by sail. It weighs about as much as 330 family cars.</p>
      <p class="small muted">Tonnage as reported by <em>The Age</em>; the car comparison is ours, at about 1.5 tonnes a car. <a href="{SRC["age1863"][1]}">Read the report on Trove</a>.</p>
    </div>
    <div class="cars" data-cars role="img" aria-label="330 small car shapes, roughly the weight of 500 tons">{CARS}</div>
  </div>
</section>

<section class="band buy-band" aria-labelledby="buy-h">
  <div class="wrap split">
    <div>
      <div class="section-head">
        <h2 id="buy-h">What we buy</h2>
        <p>Steel, copper, brass, aluminium and whole items made of them, priced by metal, grade and weight on the day.</p>
      </div>
      <ul class="mat-list">
        <li><a href="what-we-buy.html#steel"><h3>Steel and iron</h3><span>Whitegoods, hot water services, roofing iron, shelving, pipe and offcuts</span><b class="go">See items</b></a></li>
        <li><a href="what-we-buy.html#nonferrous"><h3>Copper, brass and aluminium</h3><span>Pipe, wire, fittings, window frames, stainless sinks</span><b class="go">See items</b></a></li>
        <li><a href="what-we-buy.html#vehicles"><h3>Cars, trailers and caravans</h3><span>Collected by tilt tray, with proof of ownership</span><b class="go">See items</b></a></li>
        <li><a href="what-we-buy.html#farm"><h3>Machinery and farm metal</h3><span>Old equipment, containers, site offices, wheels</span><b class="go">See items</b></a></li>
      </ul>
    </div>
    <figure class="photo tall">
      <img src="assets/img/loose-steel.jpg" width="1500" height="843" alt="A steel bin filled with loose, tangled steel wire after separation" loading="lazy">
      <figcaption>Loose steel after separation, before baling.</figcaption>
    </figure>
  </div>
</section>

<section class="band" aria-labelledby="how-h">
  <div class="wrap">
    <div class="section-head"><h2 id="how-h">How selling works</h2></div>
    <ol class="steps">
      <li><h3>Tell us what you have</h3><p>Send a few details and photos online. It takes about two minutes.</p></li>
      <li><h3>Get a price and a time</h3><p>We confirm a guide price and book a pickup or a drop-off.</p></li>
      <li><h3>Weighed, then paid by EFT</h3><p>Every load is weighed. Bring ID, which Victorian law requires us to record. Cash for scrap metal is banned.</p></li>
    </ol>
    <div class="actions"><a class="btn" href="sell.html">Start a request</a></div>
  </div>
</section>

<section class="band night token-band" aria-labelledby="tok-h">
  <div class="wrap teaser">
    <div class="coin big" data-coin data-coin-drag>{token("tz", label="The 1857 token. Drag to turn it.")}</div>
    <div>
      <p class="kicker">Copper, 28 millimetres, 1857</p>
      <h2 id="tok-h">Turn the token</h2>
      <p class="lede">Hyde&rsquo;s halfpenny reads <em>General Marine Store. Shippers of rags, glass, metals &amp;c.</em> on one side, and <em>Peace &amp; Plenty</em> on the other. Ours is a fresh redraw of the original held by Museums Victoria. Drag it round.</p>
      <div class="actions"><a class="btn" href="story.html">Open the time machine</a></div>
    </div>
  </div>
</section>

<section class="fullbleed" aria-labelledby="trade-h">
  <img src="assets/img/steel-bales-forklift.jpg" alt="A forklift carries a bale of compressed steel past stacked bales in a warehouse" loading="lazy">
  <div class="scrim"></div>
  <div class="wrap fb-in">
    <h2 id="trade-h">For workshops, builders, farms and sites</h2>
    <p class="lede">Regular metal coming off your site? We can place bins, collect on a schedule and send a statement for every load.</p>
    <div class="actions"><a class="btn" href="trade.html">Trade and business</a></div>
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

story = page_hero("bourke-st-1858.jpg", "The time machine",
    "Seven stops in the life of a Melbourne marine store, and an eighth for why we took up its name. Scroll, or jump to a year. Each stop links to the source we used.",
    CREDIT["bourke"], "50% 60%") + f'''
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

<section class="band" aria-labelledby="ms-h">
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

<section class="band on-zinc2" aria-labelledby="src-h">
  <div class="wrap">
    <h2 id="src-h" style="margin-bottom:1.25rem">Sources</h2>
    <ol class="sources">
      {''.join(f'<li><a href="{u}">{esc(t)}</a></li>' for t, u in SRC.values())}
      <li>Historic photographs and chart: State Library Victoria collection, public domain, via Wikimedia Commons.</li>
    </ol>
  </div>
</section>
'''
