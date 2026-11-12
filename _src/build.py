"""Builds the Tomato Games website (https://tomatotomatogames.com) from _src/studio.json.

    python _src/build.py          (run from the repository root, then commit and push)

One site for every game the studio publishes:
  /                      studio home, a card per game
  /<slug>/               a page per game (banner, icon, screenshots, features, Play link once live)
  /terms.html            ONE studio-wide terms of service (virtual items, purchases, ads, fair play, Israeli law)
  /privacy-policy.html   ONE studio-wide privacy policy covering all games (each game's Play listing and in-game
                         Settings link point here)
  /app-ads.txt           ONE file for the AdMob account: it authorises ads for every app of the publisher
  /CNAME                 the custom domain

Adding a game: add an entry to "games" in studio.json, put its icon.png (512x512), banner.png (1024x500) and
shots/1.jpg..N.jpg (540x960) in _src/games/<slug>/, run this script, commit, push. Folders starting with "_" are
not published by GitHub Pages (Jekyll), so _src stays out of the live site.
"""
import html, json, os, shutil

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(SRC)

CSS = """
  :root { --bg: #fff8f2; --card: #ffffff; --ink: #24161a; --muted: #6f5f63; --line: #f0dfd5; --accent: #e8462f; --accent-ink: #fff; }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) { --bg: #1a1214; --card: #251a1d; --ink: #f6ece8; --muted: #b9a8ab; --line: #3a2a2e; --accent: #ff6a52; --accent-ink: #1a1214; }
  }
  :root[data-theme="dark"] { --bg: #1a1214; --card: #251a1d; --ink: #f6ece8; --muted: #b9a8ab; --line: #3a2a2e; --accent: #ff6a52; --accent-ink: #1a1214; }
  * { box-sizing: border-box; }
  body { margin: 0; background: var(--bg); color: var(--ink); font: 17px/1.6 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
  main { max-width: 860px; margin: 0 auto; padding: 40px 16px 56px; }
  header { display: flex; align-items: center; gap: 12px; margin-bottom: 30px; }
  header a { color: inherit; text-decoration: none; display: flex; align-items: center; gap: 12px; }
  .logo { width: 40px; height: 40px; border-radius: 50%; background: var(--accent); display: grid; place-items: center; font-size: 22px; }
  header b { font-size: 20px; }
  .lead { color: var(--muted); margin: -10px 0 26px; }
  .game { background: var(--card); border: 1px solid var(--line); border-radius: 22px; overflow: hidden; margin-bottom: 18px; }
  .game > a { color: inherit; text-decoration: none; display: block; }
  .game img.banner { width: 100%; display: block; }
  .body { padding: 22px 24px 26px; display: flex; gap: 20px; align-items: flex-start; flex-wrap: wrap; }
  .body img.icon { width: 96px; height: 96px; border-radius: 22px; flex: none; }
  .body div { flex: 1 1 280px; }
  h1 { margin: 0 0 4px; font-size: 28px; }
  h1.small { font-size: 24px; }
  .tag { color: var(--muted); margin: 0 0 12px; }
  .badge { display: inline-block; background: var(--accent); color: var(--accent-ink); font-weight: 700; border-radius: 999px;
           padding: 7px 16px; font-size: 15px; text-decoration: none; }
  h2 { font-size: 21px; margin: 34px 0 14px; }
  .shots { display: grid; grid-auto-flow: column; grid-auto-columns: minmax(150px, 30%); gap: 12px; overflow-x: auto;
           scroll-snap-type: x mandatory; padding-bottom: 8px; }
  .shots img { width: 100%; border-radius: 16px; border: 1px solid var(--line); scroll-snap-align: start; display: block; }
  @media (min-width: 760px) { .shots { grid-auto-columns: calc((100% - 36px) / 4); } }
  .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; padding: 0; list-style: none; margin: 0; }
  .features li { background: var(--card); border: 1px solid var(--line); border-radius: 16px; padding: 14px 16px; }
  .features b { display: block; }
  .features span { color: var(--muted); font-size: 15px; }
  footer { margin-top: 36px; color: var(--muted); font-size: 15px; display: flex; gap: 18px; flex-wrap: wrap; }
  a { color: var(--accent); }
  .policy h2 { font-size: 19px; margin: 26px 0 8px; }
  .policy p, .policy li { overflow-wrap: anywhere; }
  .muted { color: var(--muted); }
"""

e = html.escape


def page(title, desc, body, s, icon="/favicon.png"):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="icon" href="{icon}">
<style>{CSS}</style>
</head>
<body>
<main>
  <header><a href="/"><span class="logo" aria-hidden="true">🍅</span><b>{e(s['studio'])}</b></a></header>
{body}
  <footer>
    <a href="/privacy-policy.html">Privacy Policy</a>
    <a href="/terms.html">Terms of Service</a>
    <span>Support: <a href="mailto:{e(s['support_email'])}">{e(s['support_email'])}</a></span>
    <span>© 2026 {e(s['studio'])}</span>
  </footer>
</main>
</body>
</html>
"""


def store_badge(g):
    if g.get("status") == "live":
        url = "https://play.google.com/store/apps/details?id=" + g["package"]
        return f'<a class="badge" href="{url}">Get it on Google Play</a>'
    return '<span class="badge">Coming soon to Google Play</span>'


def home(s):
    cards = []
    for g in s["games"]:
        slug = g["slug"]
        cards.append(f"""  <section class="game">
    <a href="/{slug}/">
      <img class="banner" src="/{slug}/banner.png" alt="{e(g['name'])}">
      <div class="body">
        <img class="icon" src="/{slug}/icon.png" alt="{e(g['name'])} icon">
        <div><h1 class="small">{e(g['name'])}</h1><p class="tag">{e(g['short'])}</p>{store_badge(g)}</div>
      </div>
    </a>
  </section>""")
    body = f"  <p class=\"lead\">{e(s['tagline'])}</p>\n" + "\n".join(cards)
    return page(s["studio"], s["tagline"], body, s)


def game_page(s, g):
    slug = g["slug"]
    shots = "\n".join(f'    <img src="/{slug}/shots/{i}.jpg" alt="{e(cap)}" loading="lazy">'
                      for i, cap in enumerate(g.get("screenshots", []), 1))
    feats = "\n".join(f"    <li><b>{e(t)}</b><span>{e(d)}</span></li>" for t, d in g.get("features", []))
    body = f"""  <section class="game">
    <img class="banner" src="/{slug}/banner.png" alt="{e(g['name'])}">
    <div class="body">
      <img class="icon" src="/{slug}/icon.png" alt="{e(g['name'])} app icon">
      <div>
        <h1>{e(g['name'])}</h1>
        <p class="tag">{e(g['description'])}</p>
        {store_badge(g)}
      </div>
    </div>
  </section>
""" + (f"""
  <h2>Screenshots</h2>
  <div class="shots">
{shots}
  </div>
""" if shots else "") + (f"""
  <h2>Features</h2>
  <ul class="features">
{feats}
  </ul>
""" if feats else "")
    return page(f"{g['name']} · {s['studio']}", g["short"], body, s, icon=f"/{slug}/icon.png")


def privacy(s):
    names = ", ".join(f'<a href="/{g["slug"]}/">{e(g["name"])}</a>' for g in s["games"])
    st, mail = e(s["studio"]), e(s["support_email"])
    body = f"""  <article class="policy">
  <h1>Privacy Policy</h1>
  <p class="muted">{st} &middot; Last updated: {e(s['policy_updated'])}</p>

  <p>This policy applies to all mobile games published by <strong>{st}</strong> ("we", "us") on Google Play
  (each a "Game"), currently: {names}. It explains what information the Games collect, how it is used and the
  choices you have. The Games do not ask you to create an account and we do not ask for your name, email or phone number.</p>

  <h2>1. Information stored on your device</h2>
  <p>Your game progress (levels, coins, gems, upgrades, settings such as sound and vibration) is saved on your device.
  It is not sent to us. Deleting a Game deletes this data, unless you use cloud save (section 3).</p>

  <h2>2. Information we collect</h2>
  <p>We do not run our own servers and do not collect personal information ourselves. The third-party services below,
  which the Games use, may collect information as described in their own policies.</p>

  <h2>3. Third-party services</h2>
  <ul>
    <li><strong>Google AdMob</strong> (advertising). The Games show ads: short ad breaks between rounds, and "rewarded"
      ads you choose to watch for an in-game bonus. AdMob may collect your device's advertising ID, IP address, device and
      app information and ad interaction data to show, measure and (if you agree) personalise ads.
      <a href="https://policies.google.com/technologies/partner-sites">How Google uses data from apps that use its services</a>.</li>
    <li><strong>Google User Messaging Platform</strong> (consent). In the EEA, the UK and Switzerland, and where else
      required, the Games ask for your consent before personalised ads are shown. You can change your choice at any time
      from a Game's Settings ("Privacy").</li>
    <li><strong>Google Analytics for Firebase</strong> (game analytics). The Games send anonymous usage events (for
      example rounds started and finished, levels cleared, upgrades bought, tutorial completion, ads watched and
      purchases) with an app instance ID, the advertising ID, device and app information and an approximate location
      derived from the IP address. We use this only in aggregate to improve the Games. The data is kept for 2 months.
      <a href="https://firebase.google.com/support/privacy">Firebase privacy information</a>.</li>
    <li><strong>Google Play Billing</strong> (in-app purchases). Purchases are handled by Google Play. We never see your
      payment details; we only receive a confirmation and an order ID so the purchase can be delivered and restored.
      <a href="https://payments.google.com/payments/apis-secure/u/0/get_legal_document?ldo=0&amp;ldt=privacynotice">Google Payments Privacy Notice</a>.</li>
    <li><strong>Google Play Games Services</strong> (sign-in and cloud save). If you use Google Play Games, a Game signs
      you in automatically when it starts; your Play Games player ID and your saved game are then stored in your Google
      account so progress can be restored on another device. You can decline or sign out in Play Games at any time.
      <a href="https://policies.google.com/privacy">Google Privacy Policy</a>.</li>
    <li><strong>Unity</strong> (game engine). The Games are built with Unity, which may collect basic, non-identifying
      device and performance information.
      <a href="https://unity.com/legal/game-player-and-app-user-privacy-policy">Unity Player Privacy Policy</a>.</li>
  </ul>
  <p>Not every Game uses every service above; a Game never uses a service that is not listed here.</p>

  <h2>4. How information is used</h2>
  <ul>
    <li>to show ads and give you the rewards for watching them;</li>
    <li>to process and restore in-app purchases;</li>
    <li>to save and restore your progress (if you use cloud save);</li>
    <li>to understand, in aggregate, how the Games are played (for example where players get stuck) and improve them;</li>
    <li>to keep the Games working, fix problems and prevent fraud.</li>
  </ul>
  <p>We do not sell your personal information.</p>

  <h2>5. Your choices</h2>
  <ul>
    <li><strong>Ad personalisation:</strong> change your consent in a Game's Settings, or reset / opt out of your
      advertising ID in your phone's settings (Android: Settings &gt; Google &gt; Ads).</li>
    <li><strong>No ads:</strong> a Game's "No Ads" purchase removes its ad breaks and gives ad rewards instantly, without ads.</li>
    <li><strong>Cloud save:</strong> you can decline the Play Games sign-in, or sign out of Play Games at any time.</li>
    <li><strong>Deletion:</strong> uninstall a Game to delete its local data. To delete cloud-saved data, remove the Game's
      data from your Google Play Games settings, or contact us.</li>
  </ul>

  <h2>6. Your rights (GDPR, UK GDPR, CCPA and similar laws)</h2>
  <p>Depending on where you live, you may have the right to access, correct or delete personal information, to object to
  or restrict its processing, and to withdraw consent. Because we do not hold personal information ourselves, most
  requests are handled by the services in section 3; we will help you with any request sent to the contact address
  below. The legal bases for processing are your consent (personalised ads) and our legitimate interest in providing and
  improving the Games.</p>

  <h2>7. Children</h2>
  <p>The Games are not directed at children under 13 (or the minimum age in your country) and we do not knowingly collect
  personal information from them. If you believe a child has provided personal information, contact us and we will help
  remove it.</p>

  <h2>8. Data retention and security</h2>
  <p>Local data stays on your device until you delete the Game. Third-party services keep data according to their own
  policies. We use the security measures provided by these services; no method of transmission or storage is completely
  secure.</p>

  <h2>9. Changes to this policy</h2>
  <p>We may update this policy. The date at the top shows the latest version; important changes will be announced in the
  Games or on their store pages.</p>

  <h2>10. Contact</h2>
  <p>{st}, {e(s['country'])}<br>Email: <a href="mailto:{mail}">{mail}</a></p>
  </article>
"""
    return page(f"Privacy Policy · {s['studio']}", f"Privacy policy for all {s['studio']} games.", body, s)


def terms(s):
    names = ", ".join(f'<a href="/{g["slug"]}/">{e(g["name"])}</a>' for g in s["games"])
    st, mail = e(s["studio"]), e(s["support_email"])
    body = f"""  <article class="policy">
  <h1>Terms of Service</h1>
  <p class="muted">{st} &middot; Last updated: {e(s.get('terms_updated', s['policy_updated']))}</p>

  <p>These terms apply to all mobile games published by <strong>{st}</strong> ("we", "us") on Google Play (each a
  "Game"), currently: {names}. By downloading or playing a Game you agree to these terms. If you do not agree, please do
  not use the Game. Our <a href="/privacy-policy.html">Privacy Policy</a> explains how information is handled.</p>

  <h2>1. Your licence</h2>
  <p>We give you a personal, non-exclusive, non-transferable, revocable licence to download and play the Games on your
  own devices for your own non-commercial entertainment. The Games, including their code, art, music, characters and
  names, belong to {st} or its licensors. You may not copy, modify, sell, rent, reverse engineer or redistribute a Game,
  except where the law expressly allows it.</p>

  <h2>2. Virtual items and currency</h2>
  <p>The Games contain virtual items such as coins, gems, boosts, passes and upgrades ("Virtual Items"), some of which can
  be bought with real money. Virtual Items are licensed to you, not sold; they have <strong>no real-world monetary
  value</strong>, cannot be exchanged for money or anything of value outside the Game, and cannot be transferred or sold
  to anyone else. We may change, rebalance or remove Virtual Items (for example in an update), and time-limited items such
  as passes expire as described in the Game.</p>

  <h2>3. Purchases and refunds</h2>
  <p>All purchases are made through Google Play and are subject to Google Play's terms and its refund policy. Purchases
  are final once the Virtual Item is delivered, except where Google Play's policy or applicable law gives you a right to
  a refund. If a purchase was charged but not delivered, contact us and we will help, or request a refund from Google
  Play. Purchases that remove ads remove the Game's ad breaks; rewards that are normally earned by watching an ad are then
  given without one. Your purchases can be restored on the same Google account with the Game's "Restore purchases"
  option.</p>

  <h2>4. Ads</h2>
  <p>Free versions of the Games show ads, including short ad breaks between rounds and optional ads you can choose to
  watch for a reward. Ads are provided by third parties; we are not responsible for the content of third-party ads or
  the sites they link to.</p>

  <h2>5. Fair play</h2>
  <p>Please do not cheat. You agree not to use hacks, modified versions, bots, exploits of bugs, or any other unauthorised
  means to gain an advantage, obtain Virtual Items or interfere with a Game. We may remove Virtual Items or progress
  obtained this way, and may suspend access to features for anyone who breaks these terms.</p>

  <h2>6. Progress, updates and availability</h2>
  <p>Progress is stored on your device, and in your Google account if you use cloud save. Uninstalling a Game without
  cloud save deletes local progress, and we cannot recover it. We may update a Game at any time, which may change
  features or gameplay, and some updates may be required to keep playing. We may stop offering or supporting a Game; if a
  Game is discontinued, Virtual Items in it may stop being usable, subject to applicable law.</p>

  <h2>7. Disclaimers</h2>
  <p>The Games are provided "as is" and "as available". To the fullest extent permitted by law, we make no warranties
  of any kind, including that a Game will be uninterrupted, error-free or compatible with every device.</p>

  <h2>8. Limitation of liability</h2>
  <p>To the fullest extent permitted by law, {st} is not liable for any indirect, incidental, special or consequential
  damages, or for loss of data or progress, arising from your use of the Games. Our total liability for any claim
  relating to the Games is limited to the amount you paid us for the Game or Virtual Items in the 12 months before the
  claim. Nothing in these terms limits rights you have as a consumer that cannot be limited by contract.</p>

  <h2>9. Third-party services</h2>
  <p>The Games use services provided by third parties, such as Google Play, Google Play Games, AdMob and Firebase. Your
  use of those services is also subject to their own terms.</p>

  <h2>10. Changes to these terms</h2>
  <p>We may update these terms. The date at the top shows the latest version. If you keep playing after an update, the
  new terms apply; important changes will be announced in the Games or on their store pages.</p>

  <h2>11. Governing law</h2>
  <p>These terms are governed by the laws of the State of Israel, without regard to its conflict-of-laws rules, unless
  the mandatory consumer laws of your country of residence say otherwise.</p>

  <h2>12. Contact</h2>
  <p>{st}, {e(s['country'])}<br>Email: <a href="mailto:{mail}">{mail}</a></p>
  </article>
"""
    return page(f"Terms of Service · {s['studio']}", f"Terms of service for all {s['studio']} games.", body, s)


def write(rel, text):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def main():
    with open(os.path.join(SRC, "studio.json"), encoding="utf-8") as f:
        s = json.load(f)
    write("index.html", home(s))
    write("privacy-policy.html", privacy(s))
    write("terms.html", terms(s))
    write("app-ads.txt", "".join(f"google.com, {p}, DIRECT, f08c47fec0942fa0\n" for p in s["admob_publisher_ids"]))
    write("CNAME", s["domain"] + "\n")
    for g in s["games"]:
        slug = g["slug"]
        write(f"{slug}/index.html", game_page(s, g))
        src = os.path.join(SRC, "games", slug)
        dst = os.path.join(OUT, slug)
        for name in ("icon.png", "banner.png"):
            shutil.copy2(os.path.join(src, name), os.path.join(dst, name))
        shots = os.path.join(src, "shots")
        if os.path.isdir(shots):
            shutil.rmtree(os.path.join(dst, "shots"), ignore_errors=True)
            shutil.copytree(shots, os.path.join(dst, "shots"))
    # The studio favicon: the first game's icon until the studio has its own logo.
    shutil.copy2(os.path.join(SRC, "games", s["games"][0]["slug"], "icon.png"), os.path.join(OUT, "favicon.png"))
    print("built:", ", ".join(["/", "/privacy-policy.html", "/terms.html", "/app-ads.txt"] + [f"/{g['slug']}/" for g in s["games"]]))


if __name__ == "__main__":
    main()
