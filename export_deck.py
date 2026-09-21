# -*- coding: utf-8 -*-
"""English deck for foreign suppliers met at Moscow trade shows.

A shorter, honest version of the Click Out audit. A foreign exporter cannot buy
Ozon Performance or VK Ads directly — platform accounts are opened for a Russian
legal entity only. So this deck leads with market entry and says plainly what
has to be in place before advertising starts.

Slides: 01 title · 02 why we are writing · 03 your category in Russia ·
04 how entry works · 05 where Russians buy · 06 Ozon · 07 Yandex · 08 Wildberries ·
09 what we measure · 10 terms · 11 next step
"""
import generate

CSS = generate.CSS

CATEGORIES = {

"Fruits & vegetables": {
 "headline": "Russia imports 6.1 million tonnes<br>of fruit and nuts a year",
 "stats": [
   ("6.1", "million tonnes of fruit and nuts imported into Russia in 2025 (Rosselkhoznadzor)"),
   ("4th", "largest importer of fresh produce in the world, after the USA, Germany and the Netherlands"),
   ("1.5", "trillion ₽ — Russian online grocery market in 2025, up 23% year on year"),
   ("6", "trillion ₽ — combined sales of Wildberries, Ozon and Yandex Market over 9 months of 2025, +36.4%"),
 ],
 "text": ("Russia is one of the largest fresh-produce importers in the world, and the way "
   "that produce reaches the buyer is changing fast: online grocery grew 23% in a single year. "
   "For a supplier this shifts the question. Getting a container into the country is the easy "
   "part; being the name a Russian buyer recognises on a marketplace shelf is the hard part, "
   "and it is where price competition stops."),
 "sources": "Sources: Rosselkhoznadzor / Argus-Phyto (2026), agbz.ru (2025), Data Insight (2026), retail.ru (2025).",
 "segments": [
   'Buyers in the <b>Groceries → Fruit and vegetables</b> category on Ozon and Yandex Market',
   'Buyers in <b>Healthy eating</b> and <b>Baby food</b> — categories driven by produce quality',
   'Yandex Lavka and Yandex Eda users — daily fresh grocery delivery',
   'B2B segment on Ozon: wholesale buyers, HoReCa and retail chains',
 ],
},

"Coffee & tea": {
 "headline": "Instant coffee in Russia:<br>₽316 bn and growing 16% a year",
 "stats": [
   ("316", "billion ₽ — Russian instant coffee market in 2025, up 16% in a year (BusinesStat)"),
   ("+37%", "growth of the instant coffee market over five years, from ₽231 bn in 2021"),
   ("30", "billion ₽ — coffee sold through Russian e-commerce, with whole-bean demand up 20%"),
   ("6", "trillion ₽ — combined sales of Wildberries, Ozon and Yandex Market over 9 months of 2025"),
 ],
 "text": ("Coffee is one of the most competitive categories on Russian marketplaces, and almost "
   "all of that competition is on price: the buyer compares grams and roast level, and rarely "
   "sees who produced the beans. That is the opening. A supplier whose name the buyer already "
   "recognises stops competing on price alone — and in a market growing 16% a year, that "
   "recognition is still cheap to build."),
 "sources": "Sources: BusinesStat / TAdviser (2026), 1prime.ru (2025), retail.ru (2025).",
 "segments": [
   'Buyers in the <b>Groceries → Coffee and tea</b> category on Ozon, Yandex Market and Wildberries',
   'Buyers of coffee machines and accessories — the equipment signals a regular coffee drinker',
   'Yandex Lavka and Yandex Eda users — daily grocery delivery',
   'B2B segment on Ozon: HoReCa, offices, coffee shop chains and private-label buyers',
 ],
},

"Confectionery & snacks": {
 "headline": "Confectionery in Russia:<br>₽2.15 trn and +58% on Wildberries",
 "stats": [
   ("2.15", "trillion ₽ — Russian confectionery market in 2025, up 16% in money terms"),
   ("+58%", "growth of confectionery sales on Wildberries during 2025"),
   ("<3%", "share of the online channel in Russian confectionery — the category is only starting to move online"),
   ("93%", "of confectionery sold in Russia is produced domestically — imports compete as a distinct offer"),
 ],
 "text": ("Two numbers matter here. Confectionery sales on Wildberries grew 58% in a year, while "
   "the online channel still accounts for under 3% of the market. This is a category at the very "
   "start of its move online, which means shelf space and buyer attention cost far less now than "
   "they will in a year. For an importer there is a second advantage: 93% of what Russians buy "
   "is made locally, so a foreign product reads as something different rather than as one more "
   "option on a crowded shelf."),
 "sources": "Sources: logistics.ru (2025), MegaResearch (2025), Flowwow / Daily Dozen (2025).",
 "segments": [
   'Buyers in <b>Groceries → Sweets and snacks</b> on Ozon, Yandex Market and Wildberries',
   'Buyers in <b>Tea and coffee</b> — the classic pairing scenario in Russia',
   'Buyers in <b>Healthy eating</b> — for reduced-sugar and functional lines',
   'Gift and seasonal segments: New Year and 8 March are the two peaks of the Russian year',
 ],
},

"Spices & dried foods": {
 "headline": "Russia is India's third largest<br>import partner",
 "stats": [
   ("3rd", "place Russia holds among India's import partners, after China and the UAE"),
   ("1.5", "trillion ₽ — Russian online grocery market in 2025, up 23% year on year"),
   ("6", "trillion ₽ — combined sales of Wildberries, Ozon and Yandex Market over 9 months of 2025, +36.4%"),
   ("83%", "of Ozon's audience lives outside Moscow and St Petersburg"),
 ],
 "text": ("Trade between Russia and India is growing, and food ingredients follow. But there is a "
   "gap between trade volume and brand presence: Russian buyers purchase spices and dried "
   "vegetables constantly and almost never know who supplied them. On marketplaces these "
   "categories are dominated by unbranded listings competing purely on price per kilo. "
   "A supplier who becomes a recognised name in that space is no longer interchangeable."),
 "sources": "Sources: TAdviser (2026), Data Insight (2026), retail.ru (2025), Ozon (2025).",
 "segments": [
   'Buyers in <b>Groceries → Spices and seasonings</b> on Ozon, Yandex Market and Wildberries',
   'Buyers in <b>Healthy eating</b> and <b>Superfoods</b> categories',
   'B2B segment on Ozon: food manufacturers, HoReCa and private-label buyers',
   'Buyers of ethnic and Indian cuisine products — a small but fast-growing segment',
 ],
},

"Toys & kids products": {
 "headline": "Russian kids market:<br>55% online and ₽254 bn in toys",
 "stats": [
   ("254.4", "billion ₽ — Russian games and toys market in 2025 (AIDT)"),
   ("55%", "share of online channels in Russian kids goods sales"),
   ("+30%", "growth of toy sales on Wildberries over the first five months of 2025"),
   ("60%", "share of domestic brands in the top 50 best-selling toys — the category is being redivided"),
 ],
 "text": ("After the western retail chains left, the Russian toy market was redivided between "
   "local and imported brands, and it is still moving. 55% of kids goods are already bought "
   "online, and toy sales on Wildberries grew 30% in five months while the average price rose "
   "only 3% — the category is growing by volume, not by price. Kids goods already top the list "
   "of advertiser brands on Ozon and Wildberries, which tells you where the competition is."),
 "sources": "Sources: AIDT (2025), delprof.ru (2025), rdt-info.ru (2025), Moneyplace (2025).",
 "segments": [
   'Buyers in <b>Kids → Toys and games</b> on Ozon, Yandex Market and Wildberries',
   'Buyers in <b>Kids → Newborn products</b> — the start of the parental purchase cycle',
   'Parents aged 25–45; on Wildberries 78% of the audience are women aged 25–44',
   'Seasonal flight: the New Year peak is prepared in October',
 ],
},

"Beverages": {
 "headline": "Soft drinks in Russia:<br>₽1.8 trn and growing above inflation",
 "stats": [
   ("1.8", "trillion ₽ — Russian soft drinks retail turnover in 2025"),
   ("26.7", "billion litres produced in Russia, up 52% between 2020 and 2025"),
   ("70–100%", "retail mark-up on carbonated drinks in 2025, against 20% in 2021"),
   ("1.5", "trillion ₽ — Russian online grocery market in 2025, up 23%"),
 ],
 "text": ("Soft drinks are one of the few FMCG segments in Russia growing faster than inflation "
   "across production, advertising and online sales at once. At the same time retail has taken "
   "the margin: the mark-up on carbonated drinks went from 20% to 70–100% in four years. "
   "For a supplier that translates into one simple rule — the stronger the direct demand for "
   "your name, the less your economics depend on shelf terms you do not control."),
 "sources": "Sources: AIPR (2025), sostav.ru (2026), foodmarket.spb.ru (2025), Data Insight (2026).",
 "segments": [
   'Buyers in <b>Groceries → Beverages</b> on Ozon, Yandex Market and Wildberries',
   'Yandex Lavka and Yandex Eda users — the shortest path from impression to order',
   'Buyers in <b>Healthy eating</b> — for reduced-sugar and functional drinks',
   'B2B segment on Ozon: HoReCa, offices and vending operators',
 ],
},

"Meat & seafood": {
 "headline": "Russian food e-commerce:<br>₽1.5 trn and +23% in a year",
 "stats": [
   ("1.5", "trillion ₽ — Russian online grocery market in 2025, up 23% year on year"),
   ("+26%", "growth in the number of online grocery orders during 2025"),
   ("6", "trillion ₽ — combined sales of Wildberries, Ozon and Yandex Market over 9 months of 2025"),
   ("83%", "of Ozon's audience lives outside Moscow and St Petersburg"),
 ],
 "text": ("Frozen and chilled protein is moving online in Russia together with the rest of the "
   "grocery basket, and the buyer in this category behaves differently from any other: they are "
   "buying trust. Origin, certification and the name of the producer matter more than the "
   "position of a listing in search results. That is exactly what brand media inside the "
   "marketplaces is for."),
 "sources": "Sources: Data Insight (2026), retail.ru (2025), Ozon (2025).",
 "segments": [
   'Buyers in <b>Groceries → Meat, fish and seafood</b> on Ozon and Yandex Market',
   'Buyers in <b>Halal</b> and <b>Delicatessen</b> segments',
   'B2B segment on Ozon: HoReCa, processors and retail chains',
   'Yandex Lavka users — premium daily grocery delivery',
 ],
},

"Food & grocery": {
 "headline": "Russian online grocery:<br>₽1.5 trn and +23% in a year",
 "stats": [
   ("1.5", "trillion ₽ — Russian online grocery market in 2025, up 23% year on year"),
   ("+26%", "growth in the number of online grocery orders during 2025"),
   ("6", "trillion ₽ — combined sales of Wildberries, Ozon and Yandex Market over 9 months of 2025, +36.4%"),
   ("83%", "of Ozon's audience lives outside Moscow and St Petersburg"),
 ],
 "text": ("Russian grocery is moving online quickly — 23% growth in a single year — and the "
   "structure of the market is changing with it. Marketplaces and delivery services now reach "
   "buyers in cities where no importer could build distribution on its own. The entry barrier "
   "is no longer logistics. It is being recognised."),
 "sources": "Sources: Data Insight (2026), Forbes (2026), retail.ru (2025).",
 "segments": [
   'Buyers in the relevant <b>Groceries</b> subcategory on Ozon, Yandex Market and Wildberries',
   'Yandex Lavka and Yandex Eda users — daily grocery delivery',
   'Buyers in <b>Healthy eating</b>',
   'B2B segment on Ozon: HoReCa, processors and retail chains',
 ],
},
}


def build(c):
    """c: dict with company, headline_sub, why_rows, category, next_sub, note."""
    cat = CATEGORIES[c["category"]]
    n = [0]

    def num():
        n[0] += 1
        return f"{n[0]:02d}"

    def rows(items):
        return '<div class="rows">' + "".join(
            f'<div class="row"><div class="l">{l}</div><div class="r">{r}</div></div>'
            for l, r in items) + "</div>"

    def bullets(items):
        return '<div class="rows">' + "".join(
            f'<div class="row"><div class="r">{i}</div></div>' for i in items) + "</div>"

    s = []

    s.append(f"""
<section>
  <div class="logo"><div class="sign">Ц</div><div class="nm">Cerebro<br>Target</div></div>
  <div class="kicker"><div class="bar"></div><span>Preliminary audit · Entering the Russian market</span></div>
  <h1>{c['title_h1']}</h1>
  <p class="sub">{c['title_sub']}</p>
  <div class="yline">Ozon Performance · Yandex Urban Ads · Wildberries Media</div>
  <div class="mark">Ц</div>
</section>""")

    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>Why we are writing</span></div>
  <h2>What we know about you<br>and what we can do</h2>
  {rows(c['why_rows'])}
  <div class="foot">{c['foot']}</div>
  <div class="mark">Ц</div>
</section>""")

    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>Your category in Russia</span></div>
  <h2>{cat['headline']}</h2>
  <div class="stats">{"".join(f'<div class="stat"><div class="n">{v}</div><div class="t">{t}</div></div>' for v, t in cat['stats'])}
  </div>
  <p class="sub" style="margin-top:34px">{cat['text']}</p>
  <div class="foot">{cat['sources']}</div>
  <div class="mark">Ц</div>
</section>""")

    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>How market entry works</span></div>
  <h2>Three things have to be in place<br>before advertising starts</h2>
  {rows([
    ("1 · A Russian legal entity",
     "Ozon, Yandex and Wildberries open advertising accounts for a Russian company or sole "
     "trader only — yours or your distributor's. This is the one hard requirement, and it is "
     "the reason we put it first rather than at the end of a proposal. If you do not have one "
     "yet, we can help you arrange it together with our partners."),
    ("2 · Presence on the shelf",
     "Your product needs listings on the marketplaces, or a Russian website. Advertising inside "
     "the platforms sends the buyer to your site or brand page — it cannot send them to a "
     "listing on a competing marketplace, that is a platform rule."),
    ("3 · A way to count results",
     "Analytics on the landing page and platform pixels from day one. Without them the "
     "post-view layer — orders from people who saw the banner and did not click — is simply "
     "not recorded."),
  ])}
  <div class="foot">Account opening takes 3–5 working days once the legal entity is in place; a campaign
  goes live 7 days after platform approval. We say this plainly because the sequence matters more
  than the budget.</div>
  <div class="mark">Ц</div>
</section>""")

    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>Where Russians buy</span></div>
  <h2>Three platforms, one buying moment</h2>
  <div class="cards">
    <div class="card"><div class="big">65 M</div><h3>Ozon</h3><p>active buyers in 2025, 38 orders per person on average. 83% of them live outside Moscow and St Petersburg.</p></div>
    <div class="card"><div class="big">94 M</div><h3>Yandex</h3><p>monthly audience across Market, Eda, Lavka, Go and Kinopoisk. 60% have middle income or above.</p></div>
    <div class="card"><div class="big">78%</div><h3>Wildberries</h3><p>of the audience are women aged 25–44 — the core grocery and kids-goods decision maker in a Russian household.</p></div>
  </div>
  <p class="sub" style="margin-top:30px">These platforms sell advertising impressions to outside advertisers. The buyer sees
  your banner inside the marketplace, in the moment they are already shopping, and the click takes them to your site.
  Very few suppliers in food and kids categories buy these formats — the auction there is far cheaper than
  the one for a position inside search results.</p>
  <div class="mark">Ц</div>
</section>""")

    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>Targeting · your category</span></div>
  <h2>Who we can select for your product</h2>
  {bullets(cat['segments'])}
  <div class="foot">Ozon targeting: authorisation status, demographics, region, category buyers and viewers,
  Active Premium, B2B client, custom segment from hashed phone numbers. Yandex adds income, Plus subscription
  and CRM retargeting. Wildberries adds DMP behaviour — cart and wishlist activity over the last 30 days.</div>
  <div class="mark">Ц</div>
</section>""")

    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>Formats and benchmarks</span></div>
  <h2>What the formats cost</h2>
  {rows([
    ("Ozon Performance", "Video banner, banner on the home page and in search, placement inside a product "
     "card, and the order-complete screen. Paid on a vCPM basis: an impression counts when at least 50% of "
     "the banner is visible for at least 2 seconds."),
    ("Yandex Urban Ads", "Video banner — average CPM 641 ₽, average CPC 100 ₽. Stretch banner — CPM 182 ₽, "
     "CPC 44 ₽. Horizontal banner — CPM 342 ₽, CPC 98 ₽. Vertical banner — CPM 96 ₽, CPC 29 ₽. "
     "Minimum CPM bid 50 ₽."),
    ("Wildberries Media", "Banner placements across the platform with DMP behavioural targeting. "
     "The category with the strongest audience match for food and kids goods."),
    ("Benchmarks for you", "Reach, impressions, clicks, CPM, CTR and CPC for your specific segments are "
     "pulled from the platform accounts during the audit. We do not quote category averages as if they "
     "were your numbers."),
  ])}
  <div class="mark">Ц</div>
</section>""")

    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>What we measure</span></div>
  <h2>How you will know<br>whether it worked</h2>
  {rows([
    ("Search lift", "A study by Easy Commerce across 20 brands running media on Ozon measured the increase "
     "in branded search: up to ₽100k budget — 5–12% growth; ₽100–300k — 15–35%; above ₽300k — 40–90%. "
     "For a supplier entering a new market this is the clearest early signal: more people are typing your name."),
    ("Brand lift", "Yandex Brand Lift is free at budgets from around ₽1m and reach from 2m: ad recall, brand "
     "awareness, purchase intent, top of mind."),
    ("Sales lift", "Yandex Sales Lift, reach from 2m over 4–6 weeks. In the Polaris case, people who saw the "
     "media campaign made 34% of all the brand's online purchases, while post-click attribution credited "
     "under 1%."),
    ("Post-view", "Ozon attributes orders for 30 days after banner contact. Yandex offers a post-view window "
     "of up to 90 days through the Metrica pixel."),
  ])}
  <div class="foot">These are Russian retail media benchmarks from published studies, not our own client results
  and not a forecast for your brand. Your own numbers appear after the first 6–8 week flight.</div>
  <div class="mark">Ц</div>
</section>""")

    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>Commercial terms</span></div>
  <h2>What working together looks like</h2>
  <div class="cards">
    <div class="card"><div class="big">1</div><h3>One source</h3><p>50 000 ₽ per month of management. Ozon, Urban Ads or Wildberries — your choice.</p></div>
    <div class="card"><div class="big">2</div><h3>Two sources</h3><p>80 000 ₽ per month for the test period. Comparison between platforms on your own data.</p></div>
    <div class="card"><div class="big">3</div><h3>Three sources</h3><p>90 000 ₽ per month for the test period. Different environments, frequency one channel cannot give.</p></div>
  </div>
  {rows([
    ("Media budget", "From 100 000 ₽ per month per source — below that a platform does not gather enough "
     "volume to draw conclusions. We recommend from 200 000 ₽ per source."),
    ("Term", "From six months. Media effects read on a 6–8 week horizon; budget decisions are taken quarterly."),
    ("Included", "Campaign management, creatives, the analytics setup, lift measurement, reporting, "
     "and a written go / no-go decision at the end of the cycle."),
    ("What we do not promise", "Guaranteed results, a number or cost of orders, or a refund. We promise "
     "transparent budgets, tested hypotheses and an honest answer when the test says no."),
  ])}
  <div class="mark">Ц</div>
</section>""")

    s.append(f"""
<section>
  <div class="num">{num()}</div>
  <div class="kicker"><div class="bar"></div><span>Next step</span></div>
  <h1>Next step — a 20 minute call</h1>
  <p class="sub">{c['next_sub']}</p>
  <div class="yline">Cerebro Target · Click Out<br>clickout.cerebrotarget.ru</div>
  <div class="mark">Ц</div>
</section>""")

    body = "".join(s)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{c['page_title']}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@500;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
{body}
</body>
</html>
"""
