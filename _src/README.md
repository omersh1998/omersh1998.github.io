# Tomato Games studio: website and new-app playbook

This repository is the **studio website**, https://tomatotomatogames.com. It's built from `_src/` by `python _src/build.py`. GitHub Pages doesn't publish folders that start with `_`, so these notes stay private to the repo.

## Shared by every game (set up once, done ✅)

| What | Where | Notes |
|---|---|---|
| Domain + website | `tomatotomatogames.com`, DNS at Squarespace → GitHub Pages | One page per game at `/<slug>/` |
| Support email | `support@tomatotomatogames.com` (Google Workspace alias) | Use it in every game and every store listing |
| Privacy policy | `https://tomatotomatogames.com/privacy-policy.html` | **One policy for all games.** It lists every game automatically. Use this URL in each game's Play Console and in its in-game Settings link. |
| Terms of service | `https://tomatotomatogames.com/terms.html` | **One set of terms for all games** (virtual items have no cash value, purchases via Google Play, ads, fair play, Israeli law). Link it in each game's Settings and on the Google Cloud consent screen. |
| app-ads.txt | `https://tomatotomatogames.com/app-ads.txt` | One line per AdMob publisher ID. It covers **all** apps in that AdMob account. Nothing to do per game. |
| Play Console developer account | Tomato Games | All games live in it. Its "website" is this domain. |
| AdMob account | publisher `pub-2119263671751122` | Add each new app inside the same account |
| Google Workspace | `tomatotomatogames.com` | Mail, and verified domain ownership for Google Cloud consent screens |

## Per new game (checklist)

**Website (5 minutes)**
1. Add an entry to `games` in `_src/studio.json` (slug, name, package, status, texts, features, screenshot captions).
2. Put `icon.png` (512×512), `banner.png` (1024×500) and `shots/1.jpg…N.jpg` (540×960) in `_src/games/<slug>/`.
   Optional: `"online": true` for a game that keeps accounts on our own server (the privacy policy and terms then say so), `"shots_wide": true` for landscape screenshots, `"credit"` for a line under the features.
3. Run `python _src/build.py`, then commit and push. The privacy policy and the home page pick up the new game by themselves.
4. When the game is public on Google Play, set its `"status"` to `"live"`. The page then shows a "Get it on Google Play" link.

**Play Console:** create the app, then:
- Store settings: website `https://tomatotomatogames.com`, email `support@tomatotomatogames.com`
- App content → Privacy policy: `https://tomatotomatogames.com/privacy-policy.html`
- (Terms aren't a Play Console field: they go in the game's Settings, `Config.TermsUrl`, and the consent screen's optional terms link.)
- New personal accounts: a closed test with 12 testers for 14 days, per app. With an organization account (D-U-N-S) this step is skipped.

**AdMob:** add the app to the existing account and create its ad units. No app-ads.txt work is needed.

**Firebase:** you can add the new app to the **same** Firebase project, as another Android app with its own `google-services.json`, or give it its own project. Analytics stays separate per app either way.

**Play Games Services:** each game gets its own Play Games project and OAuth client (SHA-1 of that app's signing key). On the Google Cloud consent screen, reuse the same branding: home page, this privacy policy, authorized domain `tomatotomatogames.com`.

**Unity project:** the Evolution Race project has reusable pieces:
- AdMob service with consent, rewarded ads and run-break interstitials
- Unity IAP service with store diagnostics
- Firebase `Telemetry`
- Play Games cloud save with automatic sign-in
- In-app update popup (`AppUpdates`)
- Release build (`.aab` with signing kept outside the project, debug symbols, and a fix for spaces in the project path)

Copy them into the new game and change only:
- package ID
- `Config` IDs: AdMob app and unit IDs, products, `PrivacyPolicyUrl`, `SupportEmail`
- the Play Games app ID
- `google-services.json`

**Signing:** each app gets its own upload key, created with `tools/create-upload-keystore.ps1` and kept in `%USERPROFILE%`. Never commit it.

## Things that can never be shared

- The package ID, Play Console listing, IAP products and ratings belong to each app.
- The 12-tester closed test applies per app while the developer account is a new personal account.
