# Initial project brief

This file is the source of truth for the document-producing collection. Later
runbooks must preserve its scope and record unanswered questions rather than
inventing requirements.

## Project workspace

- Project name: final fantasy
- Workspace: `projects/final-fantasy/`

## What are we creating?

A turn-based fantasy role-playing game for short mobile and desktop sessions.

## Product category

- [x] Game

## Game characteristics

- [x] 3D presentation
- [x] Single-player and multiplayer game
- [x] Role-playing game (RPG)

## Shared product requirements

- Accessible controls, text, captions, and visual settings
- Save, resume, and data-loss recovery behaviour
- Crash reporting and player-facing error recovery
- Long-session save, checkpoint, and recovery rules
- Readable dialogue, inventory, quest, and progression UI
- Online identity, matchmaking, moderation, and reporting requirements
- Social features, communities, and player-safety requirements
- Network-loss, reconnection, and multiplayer state-recovery behaviour

## Who is it for, and what must it help them do?

- Intended users: - Core/hobby players
- Teen players
- Their primary outcome: Progress through a story or campaign
- What makes the first useful session successful: Complete onboarding and play the core loop

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

- [x] Cross-platform game (web, mobile, and desktop)

Additional selected targets:

- [x] Responsive public web application
- [x] Progressive web app (PWA)
- [x] Android phone
- [x] Android tablet / ChromeOS
- [x] iPhone (iOS)
- [x] iPad (iPadOS)
- [x] Desktop web application
- [x] macOS
- [x] Windows
- [x] Linux
- [x] PC game storefronts (Steam, Epic Games Store, GOG, itch.io)

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
### Android tablet / ChromeOS

- Touch controls and orientation rules
- Mobile performance, battery, thermal, and download-size budget
- App-store packaging, privacy disclosures, and release requirements
### iPhone (iOS)

- Touch controls and orientation rules
- Mobile performance, battery, thermal, and download-size budget
- App-store packaging, privacy disclosures, and release requirements
### iPad (iPadOS)

- Touch controls and orientation rules
- Mobile performance, battery, thermal, and download-size budget
- App-store packaging, privacy disclosures, and release requirements
### Desktop web application

- Keyboard, mouse, touch, and gamepad input
- Responsive layout across phone, tablet, and desktop screens
- Browser compatibility and web performance budget
### macOS

- Keyboard, mouse, and gamepad support
- Window, display-resolution, graphics-quality, and accessibility settings
- Desktop packaging, installation, update, and storefront requirements
### Windows

- Keyboard, mouse, and gamepad support
- Window, display-resolution, graphics-quality, and accessibility settings
- Desktop packaging, installation, update, and storefront requirements
### Linux

- Keyboard, mouse, and gamepad support
- Window, display-resolution, graphics-quality, and accessibility settings
- Desktop packaging, installation, update, and storefront requirements
### PC game storefronts (Steam, Epic Games Store, GOG, itch.io)

- Keyboard, mouse, and gamepad support
- Window, display-resolution, graphics-quality, and accessibility settings
- Desktop packaging, installation, update, and storefront requirements

## Constraints and non-goals

- Technology and repository constraints: To be determined by the factory from the game format, selected platforms, and project brief.
- Privacy, security, accessibility, offline, integration, cost, and delivery constraints: To be determined by the factory from the game format, selected platforms, and project brief.
- Explicitly excluded work: No copied branding, assets, text, layouts, or distinctive interactions.

## Cross-platform product decisions

- Shared versus platform-specific capabilities: Build every selected platform in tandem from one shared core, with feature parity by default and platform-specific input or UI adaptations only where necessary.
- Data synchronisation, offline, and conflict policy: Store player state remotely against the player account so it can be shared across selected devices wherever possible. Provide a local offline cache, safe synchronisation, and conflict recovery. Design the save-state service as a reusable platform capability rather than a game-specific silo.
- Accessibility, localisation, privacy, parental-control, store, or certification requirements: Provide localisation support, privacy consent and player data controls, and age-rating or parental-control requirements. Apply platform-appropriate accessibility requirements (including WCAG guidance for web surfaces). Build the appropriate distributable package for every selected platform.
- Minimum supported OS, browser, device class, and network condition: Support device classes and OS/browser versions that remain widely used for every selected platform. Make slow or offline network conditions usable wherever feasible without compromising the core game design or required online features.

## Functional references

Final Fantasy V for turn-based party combat and world progression.

## Art direction

- No custom direction supplied. Gemma 4 12B will create an original art direction for asset work.
- The project `.env` has been configured for Gemma 4 12B automatic art direction.

## Open decisions

- Infer suitable technical services, including analytics, from the product brief and selected platforms.
- Infer remaining product decisions from the functional references unless they conflict with an explicit requirement.
- Record only genuine ambiguities that cannot be resolved safely from the available context.
