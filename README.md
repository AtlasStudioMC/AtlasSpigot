<div align="center">

## AtlasSpigot

[![License](https://img.shields.io/badge/license-mixed%20(MIT%2FGPL--3.0)-blue?logo=github)](LICENSE.md)
[![Minecraft](https://img.shields.io/badge/minecraft-26.2%20%7C%2026.1.2%20%7C%201.21.11-blueviolet)](https://github.com/Winds-Studio/Leaf)
[![bStats Graph Data](https://bstats.org/signatures/bukkit/AtlasSpigot.svg)](https://bstats.org/plugin/bukkit/AtlasSpigot/33733)

A tuned, rebranded Minecraft server spanning [Paper](https://github.com/PaperMC/Paper),
[Purpur](https://github.com/PurpurMC/Purpur), and [Leaf](https://github.com/Winds-Studio/Leaf) -
one build philosophy across every supported Minecraft version.

</div>

AtlasSpigot isn't a fork from scratch: each version is Paper, Purpur, or Leaf (whichever one
actually has buildable source for that Minecraft version - see [`ROADMAP.md`](ROADMAP.md)),
source-rebuilt with a real brand change baked into the jar itself (not just a config overlay) and a
set of scale/resource tuning changes layered on top, each checked against that version's own
upstream source and issue tracker before being enabled. Every change here is documented with *why*,
not just *what* — see [What's tuned here](#whats-tuned-here) and each version's own
`source-patches/` folder for the actual diffs.

This is a self-hosted build with no CI pipeline, Discord, or sponsors of its own — those usual
badge-row staples are left out rather than faked. What's above is real: a static license badge
backed by an actual [`LICENSE.md`](LICENSE.md), and a live [bStats](#statistics) graph.

### Contents

- [Downloads](#downloads)
- [Roadmap](ROADMAP.md)
- [Quick start](#quick-start)
- [What's tuned here](#whats-tuned-here) — [branding](#branding), [performance](#performance),
  [what's deliberately not enabled](#deliberately-not-enabled),
  [how settings are screened](#how-settings-are-actually-screened)
- [First-boot startup time](#first-boot-startup-time)
- [Handling a lot of players](#handling-a-lot-of-players)
- [Building and setting up](#building-and-setting-up)
- [License](#license)
- [Statistics](#statistics)
- [Credits](#credits)

## Downloads

Every Minecraft version is its own track, with its own tag prefix on the
[**Releases**](../../releases) page and its own folder for config + source-patches. The website's
[downloads page](https://github.com/AtlasStudioMC/Atlas-Website) shows the full lineup and what's
actually shipped vs still planned; here's what's released right now:

| Minecraft | Built on | Tag prefix | Config/patches |
|---|---|---|---|
| 26.2 | Leaf | `atlasspigot-26.2-N` | repo root |
| 26.1.2 | Leaf | `atlasspigot-26.1.2-N` | [`26.1.2/`](26.1.2/) |
| 1.21.11 | Leaf | `atlasspigot-1.21.11-N` | [`1.21.11/`](1.21.11/) |

A new release ships for every change on whichever track it applies to, so the top of each tag
prefix's history is always that track's current build. Same tuning philosophy on every track - a
couple of settings differ per-track only because that version's own stock defaults differ (e.g.
each `spigot.yml`'s entity-tracking-range is halved from *that specific version's* own stock
numbers, documented inline, not copy-pasted from another track).

The full roadmap - which older versions will build on Purpur, and which oldest ones fall back to
Paper/Spigot directly, and why - is in [`ROADMAP.md`](ROADMAP.md).

## Quick start

1. Copy **everything else in this repo** into the same folder as the jar you downloaded above:
   `start.sh`, `server.properties`, `spigot.yml`, `eula.txt`, and the whole `config/` directory.
2. Open `eula.txt` and set `eula=true` — vanilla Minecraft requires this; the server won't start
   without it.
3. Start it:

   ```bash
   ./start.sh
   ```

   (or `java -jar AtlasSpigot-26.2.jar nogui` directly — `start.sh` just adds the JVM tuning below)

**Running on a hosting panel** (Pterodactyl, Spaceify, etc.)? Panels generate their own startup
command and ignore `start.sh` entirely, which means the JVM tuning below never applies unless you
add it yourself — see [`PANEL_STARTUP_FLAGS.md`](PANEL_STARTUP_FLAGS.md) for the same tuning adapted
to a panel's dynamic memory-percentage style. You'll still need to upload the config files
regardless, since the panel has no way to know they exist.

> **Jar-only deployment?** Branding still shows "AtlasSpigot" with no config at all — that's baked
> into the build itself. But none of the performance tuning below is active without the config
> files, and that failure is silent (no error, it just quietly uses stock defaults). Copy the whole
> repo, not just the jar.

Java 17+ to run the jar. Java 25 if you want to build it from source yourself — see
[Building and setting up](#building-and-setting-up).

### Why so many config files, and why they can't all be one

Bukkit, Spigot, Purpur, Paper, and Leaf/Gale are five separate projects stacked on top of each
other, and each one owns and independently saves its own config file - that's not this repo's
choice, it's how the whole ecosystem is built. Merging them isn't just a copy-paste job: each
system loads its file into memory, then writes the *whole file* back out on save. Point two of them
at the same physical file and whichever one saves last silently overwrites the other's settings
with its own - a real, silent way to lose configuration, not a hypothetical one.

What *is* safe, and what this repo actually does: only ship files that have been genuinely
customized. `purpur.yml` (renamed `atlas.yml`), `bukkit.yml`, `commands.yml`, `gale-global.yml`,
and `gale-world-defaults.yml` were checked and found to have nothing worth changing at the generic
level - Purpur in particular is a gameplay-feature project, not a performance one, and its config
reflects that. They're not in this repo because the server generates them itself, with identical
content, whether they're present or not. That's five fewer files to manage without touching
anything real.

## What's tuned here

### Branding

Every brand-facing string reads **AtlasSpigot** — the early `[bootstrap]` startup line, the console
banner, the console window title, MOTD, server-list name, crash reports, the client-facing F3 brand
text, and `Bukkit.getName()` (what plugins check for compatibility). This works **even with zero
config present**, because it's fixed at the actual source of truth: the `Brand-Name` attribute baked
into the jar's build manifest, which is what every one of those code paths ultimately reads.

Two config files were renamed too, with matching source changes so the rename is real, not
cosmetic: `purpur.yml` → `atlas.yml`, `config/leaf-global.yml` → `config/atlas-global.yml`.

Left alone, on purpose:
- Leaf's own in-tree `LICENSE.md` and copyright headers (distinct from [this repo's `LICENSE.md`](LICENSE.md),
  which covers the distribution as a whole) — a license requirement, not branding.
- In-file credit comments pointing at Leaf/Purpur's real websites and docs — honest attribution to
  the code this is actually built on.
- The internal `Brand-Id` (`winds-studio:leaf`) — an identifier other code checks for plugin
  compatibility against Paper/Gale/Pufferfish/Purpur, not display text. Changing it risks breaking
  compatibility detection for no visible benefit.

Full detail and diffs: [`source-patches/build-manifest-brand-fix.diff`](source-patches/build-manifest-brand-fix.diff),
[`craftserver-brand-fix.diff`](source-patches/craftserver-brand-fix.diff),
[`main-atlas-rename.diff`](source-patches/main-atlas-rename.diff),
[`leafconfig-atlas-rename.diff`](source-patches/leafconfig-atlas-rename.diff).

### Performance

| Area | Setting | What it does |
|---|---|---|
| JVM/GC | `start.sh` — Aikar's flags, G1GC | Tuned for an 8GB heap. `-XX:+AlwaysPreTouch` deliberately left out — it roughly doubles startup time for a marginal, usually unnoticeable steady-state gain. |
| Chunks | `region-format: B_LINEAR` | Smaller world files on disk. `LINEAR_V2` was tested and rejected — Leaf's own config prints a stability warning for it on boot; `B_LINEAR` showed none. |
| Chunks | Chunk load/send rate uncapped, async chunk packet sending | Chunks reach players as fast as the server can push them instead of being artificially throttled. |
| Scale | `view-distance`/`simulation-distance`: 10/10 → 6/4 | The biggest lever for per-player memory/CPU cost at high concurrent player counts. |
| Scale | `entity-tracking-range` roughly halved | Less network/CPU overhead in crowded areas — this cost scales with entities × nearby players. |
| Scale | `max-joins-per-tick`: 5 → 25 | Removes an artificial ~100/sec cap on how fast a mass-reconnect queue drains. |
| Mobs/AI | Distance-based AI throttling (DAB) | Entities far from any player tick less often. |
| World | `ALTERNATE_CURRENT` redstone engine, `optimize-explosions` | Well-established, largely vanilla-compatible engine swaps for two of the heaviest world-simulation hot paths. |
| World | `optimized-powered-rails` | Rewrites powered/activator rail update propagation to run from a single rail instead of each block iterating separately — up to 4x faster toggling, same vanilla order, per the implementation's own description. |
| I/O | `dont-save-primed-tnt`, `dont-save-falling-block` | Skips writing these to disk on chunk save/unload — cuts I/O when a lot of TNT is active. Trade-off: those entities don't survive an unload+reload. |
| Network | Reduced entity move/motion packets, disabled decorative particles, larger item merge radius | Less per-tick network chatter and fewer duplicate item-entity ticks in busy areas. |

### Deliberately **not** enabled

Checked and rejected, with reasons — not just left at defaults by omission:

- **`optimize-entity-activation`** — briefly enabled in v8/v9, then reverted. Reading the ~76-line
  patch, it looked safe (just deduplicates entity collection across overlapping player activation
  ranges, same DAB/priority logic). What that read missed: Leaf's own source tags the field
  `@Experimental`, an explicit signal from the maintainers themselves that they don't consider it
  fully battle-tested yet, regardless of how clean the diff reads. No open bug reports found either
  way - this isn't "known broken," it's "not verified enough to keep on by this project's own
  admission." Caught during a full re-verification pass (boot log showed
  `[LeafConfig] You have following experimental module(s) enabled`) and reverted before it shipped
  any further. Worth revisiting once Leaf itself drops the annotation.
- **`optimize-mob-spawning`, `optimize-random-tick`** — both are deep rewrites of core vanilla
  mechanics (mob spawning, and the random ticks driving crop growth/leaf decay/fire spread).
  `optimize-mob-spawning`'s own patch notes say it "reduce[s] random calls" — a real change to
  vanilla's RNG consumption pattern, not just speed. Not enabled without being able to verify
  they're truly behavior-preserving.
- **`parallel-world-ticking`** — Leaf's own issue tracker has a real, open cluster of concurrency
  bugs tied to this exact experimental feature (crashes, a memory leak, thread blocking).
- **`sleeping-block-entity`** (Lithium-derived hopper/comparator sleep optimization) — broad surface
  area across hoppers, comparators, and inventory tracking, with a real history of closed bugs
  specifically about hopper item collection at chunk edges. Fixed since, but too much surface to
  fully re-verify for this build.
- **`LINEAR_V2` region format** — see the table above; `B_LINEAR` was used instead.

### How settings are actually screened

Not vibes - a checklist, applied the same way every time before anything gets enabled:

1. Read the actual patch/diff, not just the config comment.
2. Check for an explicit upstream caution flag: Leaf's `@Experimental`/`@Deprecated` annotations, or
   Paper's own `unsupported-settings` config section. Either one is treated as a hard no by itself -
   not something to override just because the code reads cleanly. This is exactly what
   `optimize-entity-activation` above slipped through on the first pass.
3. Search Leaf's issue tracker for open reports mentioning the feature.
4. Boot with it enabled and read the *entire* log, not a grep for expected lines.
5. Where practical, verify past just "it booted" - a simulated client completing login, or a
   deliberately-broken config proving a setting actually does what it claims.

A one-time systematic pass through every currently-enabled setting against steps 2-3 (not just new
additions) is done periodically, not only when adding something new - that's how the
`optimize-entity-activation` regression got caught two releases after it shipped, not zero.

## First-boot startup time

A brand-new world has to generate its spawn chunks before the server can finish starting — that's a
one-time cost tied to the host's CPU allocation, not something this build controls. A single-vCPU
container (`Paper is using 1 worker threads` in your log is the tell) will always take longer here;
expect 30–60s on the very first boot. Once the world exists on disk, restarts skip generation
entirely.

## Handling a lot of players

The tuning above genuinely raises what one instance can hold on limited RAM — but there's a real
ceiling. A single JVM process has a per-player memory/CPU floor (network buffers, entity tracking,
chunk data) that no setting erases. Getting into the thousands of concurrent players is a
[Velocity](https://papermc.io/software/velocity) proxy in front of multiple backend instances, not
a single-server config problem.

## Building and setting up

#### Initial setup

Clone Leaf itself (this repo only holds the config layer and the diffs on top of it, not Leaf's
own source) and apply its patches:

```bash
git clone --branch ver/26.2 --single-branch https://github.com/Winds-Studio/Leaf.git
cd Leaf
./gradlew applyAllPatches
```

Then apply every diff in this repo's [`source-patches/`](source-patches/) to the resulting tree -
each one documents the exact file and hunk it touches.

#### Compiling

```bash
./gradlew createPaperclipJar
```

Requires Java 25. The output is a self-bootstrapping Paperclip jar - the same kind published on
this repo's [Releases](../../releases) page.

## License

No single license covers this the way "MIT" alone would suggest - Leaf inherits a mix from
upstream (Paperweight/most patches: MIT; some patches: GPL-3.0, LGPL-3.0, or Apache-2.0 per their
own header; **compiled binaries: GPL-3.0-only**), and this repo's own additions
([`source-patches/`](source-patches/)) are MIT. Full text for each license lives in
[`licenses/`](licenses/), copied verbatim from Leaf itself; [`LICENSE.md`](LICENSE.md) has the
breakdown of what covers what. The badge at the top links there rather than overclaiming a single
license that wouldn't be accurate.

## Statistics

[![bStats Graph Data](https://bstats.org/signatures/bukkit/AtlasSpigot.svg)](https://bstats.org/plugin/bukkit/AtlasSpigot/33733)

This is a real, registered bStats project (id `33733`) - it started at zero, same as any new software's
does, and only grows as real AtlasSpigot servers actually run and report in. Getting the jar to report
here at all took two real fixes, not just a config toggle:

1. The bundled metrics client was originally hardcoded to Leaf's own bStats project - every AtlasSpigot
   server was silently reporting into *Leaf's* stats, not one of its own.
2. The special curated "Server Software" category Paper/Purpur/Leaf/Yatopia use (the one behind their
   `signatures/server-implementation/*` badges) turned out not to be self-serve creatable - it's an
   admin-curated list, confirmed by that exact badge path 404ing for an unregistered name. What *is*
   self-serve is registering as a regular Bukkit/Spigot service, which is what this project actually is -
   so the jar's metrics client was rewritten to speak that schema (a real service id, not just a name
   string) instead. See [`metrics-atlas-bstats-service.diff`](source-patches/metrics-atlas-bstats-service.diff).

Made with <span style="color: #e25555;">&#9829;</span> on Earth.

## Credits

Built on **[Leaf](https://github.com/Winds-Studio/Leaf)**, which itself aggregates work from
[Gale](https://github.com/GaleMC/Gale), [Pufferfish](https://github.com/pufferfish-gg/Pufferfish),
[Purpur](https://github.com/PurpurMC/Purpur), [KTP](https://github.com/lynxplay/ktp),
[Patina](https://github.com/PatinaMC/Patina), and others — see Leaf's own README for its full
credits list. None of the underlying performance work in the table above is original to this
repo; what's original here is the branding fix, the scale/resource tuning choices, and the
verification behind each one.
