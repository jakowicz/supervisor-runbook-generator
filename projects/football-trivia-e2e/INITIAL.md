# Initial project brief

This file is the source of truth for the document-producing collection. Later
runbooks must preserve its scope and record unanswered questions rather than
inventing requirements.

## Project workspace

- Project name: football-trivia-e2e
- Workspace: `projects/football-trivia-e2e/`

## What are we creating?

A feature-rich football trivia game for quick mobile sessions: themed rounds, multiple question formats, answer validation, scoring streaks, accessible feedback, local progress, and a curated first-release question bank.

## Product category

- [x] Game

## Game characteristics

- [x] 2D presentation
- [x] Single-player game
- [x] Puzzle
- [x] card
- [x] board
- [x] or turn-based game

## Shared product requirements

- Accessible controls, text, captions, and visual settings
- Save, resume, and data-loss recovery behaviour
- Crash reporting and player-facing error recovery

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
- [x] Android phone
- [x] iPhone (iOS)

## Per-target requirements

### Responsive public web application

- Keyboard, mouse, touch, and gamepad input
- Responsive layout across phone, tablet, and desktop screens
- Browser compatibility and web performance budget
### Progressive web app (PWA)

- Installable PWA experience
- Offline asset and save-data behaviour
- Safe game update and cache-refresh behaviour
### Android phone

- Touch controls and orientation rules
- Mobile performance, battery, thermal, and download-size budget
- App-store packaging, privacy disclosures, and release requirements
### iPhone (iOS)

- Touch controls and orientation rules
- Mobile performance, battery, thermal, and download-size budget
- App-store packaging, privacy disclosures, and release requirements

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

The Athletic quiz formats for football-topic breadth and QuizUp for short competitive trivia sessions only

## Art direction

- User direction: Original modern football broadcast graphics, bold category colours, readable typography, and celebratory but accessible feedback
- The project `.env` has been updated to use this direction.

## Audio direction

- No custom direction supplied. Gemma 4 12B will create an original music and sound direction for audio work; ACE-Step 1.5 XL Turbo will generate the selected cues locally.

## Open decisions

- Resolve remaining decisions from the brief and references; record only genuine ambiguities.
