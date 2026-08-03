# Platform appendix — web and PWA

Both selected targets share the same campaign, save semantics, original-content boundary, accessibility intent, and P0 requirements. No target may change campaign rules or make connection/account use mandatory.

| Area | Responsive public web application | Progressive web app | Parity / policy |
| --- | --- | --- | --- |
| Input | keyboard, mouse, touch, feature-detected gamepad | same adapters | REQ-0009; unavailable hardware has visible fallback |
| Layout/accessibility | phone/tablet/desktop semantic responsive UI | same | REQ-0010/NFR-0004; exact matrix remains GATE-0002 |
| Capability | browser launch; initial assets required before offline play | install affordance when browser permits | declined/unavailable installation never blocks web play |
| Offline/data | local saves and preferences; no network required for campaign | cached assets enable offline run; saves are distinct from cache | NFR-0001–0003; storage choice GATE-0003 |
| Update | normal browser reload may obtain a release | cache refresh/update activates only title/pause after confirmed save | known-good cache retained; rollout GATE-0005 |
| Performance | measure load, bundle, startup, interaction and slow network | additionally measure warm/offline startup and cache size | numeric budgets/matrix not selected (GATE-0002) |
| Distribution/policy | public web host not selected | manifest/service worker/host policy not selected | no store/certification claim; GATE-0005/0007 |
| Privacy/errors | minimal consent-gated diagnostics and player recovery | same, including cache/storage recovery | NFR-0006, REQ-0012 |

There are no selected native, TV, console, account, multiplayer, commerce, or live-service targets. Any later target receives its own adaptation row and requirements; it does not reinterpret the shared core.
