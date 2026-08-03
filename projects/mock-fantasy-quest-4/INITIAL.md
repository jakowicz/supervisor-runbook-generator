# Initial project brief

This file is the source of truth for the document-producing collection. Later
runbooks must preserve its scope and record unanswered questions rather than
inventing requirements.

## Project workspace

- Project name: mock-fantasy-quest-4
- Workspace: `projects/mock-fantasy-quest-4/`

## What are we creating?

A deliberately small offline 2D fantasy adventure, scoped to require roughly 18 implementation runbooks: exploration, one town, one dungeon, turn-based combat, inventory, quests, save/load, settings, and a short ending.

## Product category

- [x] Game

## Game characteristics

- [x] 2D presentation
- [x] Single-player game
- [x] Role-playing game (RPG).

## Shared product requirements

- Accessible controls, text, captions, and visual settings
- Save, resume, and data-loss recovery behaviour
- Crash reporting and player-facing error recovery
- Long-session save, checkpoint, and recovery rules
- Readable dialogue, inventory, quest, and progression UI

## Who is it for, and what must it help them do?

- Intended users: - Casual players
- Adult players
- Their primary outcome: Progress through a story or campaign.
- What makes the first useful session successful: Finish a first battle and understand how saving works.

## Required first-release capabilities

- Playable core loop
- Onboarding and tutorial
- Save/load and progression
- Settings and accessibility
- Audio and visual feedback
- Content/level delivery
- Player account and identity
- Multiplayer services and player safety
- Live-service operations
- In-app purchases and entitlement handling
- Crash/error recovery

## Later or deferred capabilities

- Live events or seasonal content
- Player-created and shared content (custom levels, mods, designs, or stories)
- Advanced analytics or monetisation

## Target systems and delivery surfaces

Responsive public web application and Progressive web app (PWA) are included by
default. The selected compatible delivery profile is:

- [x] Automated compatible profile

Additional selected targets:

- [x] Responsive public web application
- [x] Progressive web app (PWA)

## Per-target requirements

### Responsive public web application

- Keyboard, mouse, touch, and gamepad input
- Responsive layout across phone, tablet, and desktop screens
- Browser compatibility and web performance budget
### Progressive web app (PWA)

- Installable PWA experience
- Offline asset and save-data behaviour
- Safe game update and cache-refresh behaviour

## Constraints and non-goals

- Technology and repository constraints: Determine from the product brief and selected platforms.
- Privacy, security, accessibility, offline, integration, cost, and delivery constraints: Determine from the product brief and selected platforms.
- Explicitly excluded work: No copied branding, assets, text, layouts, or distinctive interactions.

## Cross-platform product decisions

- Shared versus platform-specific capabilities: Use a shared core with platform adaptations only where necessary.
- Data synchronisation, offline, and conflict policy: Use remote account-linked state with safe local cache where applicable.
- Accessibility, localisation, privacy, parental-control, store, or certification requirements: Provide accessibility, localisation, privacy, and applicable platform requirements.
- Minimum supported OS, browser, device class, and network condition: Support widely used devices and feasible slow-network behaviour.

## Functional references

Final Fantasy V for party-based turn-based adventure scope only

## Art direction

- User direction: Original warm hand-painted fantasy, readable silhouettes, restrained palette
- The project `.env` has been updated to use this direction.

## Open decisions

- Resolve remaining decisions from the brief and references; record only genuine ambiguities.
