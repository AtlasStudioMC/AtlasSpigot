# AtlasSpigot

A tuned, rebranded build of [Leaf](https://github.com/Winds-Studio/Leaf) (a performance-focused
Paper fork) for Minecraft 26.2.

## Getting the server jar

Grab `AtlasSpigot-26.2.jar` from this repo's [Releases](../../releases) page. It's a real source
rebuild of Leaf 26.2 (build 90) - not the stock jar - see "What's tuned here" below for what
changed and why.

## Setup

1. Put `AtlasSpigot-26.2.jar` in a folder.
2. Copy **everything else from this repo** into that same folder (`start.sh`, `server.properties`,
   `spigot.yml`, `atlas.yml`, `bukkit.yml`, `commands.yml`, `eula.txt`, and the whole `config/`
   directory).
3. Set `eula=true` in `eula.txt` - the server refuses to start without it (that's a vanilla
   requirement, not something this fork can skip).
4. Run it:
   ```bash
   ./start.sh
   ```
   (or `java -jar AtlasSpigot-26.2.jar nogui` directly, though `start.sh` carries the tuned JVM
   flags)

Requires Java 25 to build from source (see `source-patches/`); the built jar itself only needs
Java 17+ to run.

**If you only copy the jar and skip step 2**: branding still shows "AtlasSpigot" (it's now baked
into the jar's build manifest, not just config - see below), but none of the performance tuning
(view distance, chunk settings, JVM flags, etc.) is active, and that part fails silently with no
error. Copy the config files anyway if you want the tuning, not just the name.

**On a hosting panel** (Pterodactyl/Spaceify/etc.) that generates its own startup command: that
command replaces `start.sh`'s JVM flags, which is usually fine (panels often size the heap via
`-XX:MaxRAMPercentage` against the container's memory limit instead of a fixed `-Xmx`, which is a
reasonable alternative) - but you still need to upload the config files from this repo into the
container's server directory yourself, since the panel has no way to know they exist.

## What's tuned here

- **Branding**: MOTD, server-list name, console title, crash-report identifier, the early
  `[bootstrap]` startup line, the console startup banner, the client-facing F3 brand text, and
  `Bukkit.getName()` (used by plugins for compatibility checks) all read "AtlasSpigot" - **by
  default, with zero config present**. This is now fixed at the actual build-time source of truth:
  Paper/Leaf's `Brand-Name` jar manifest attribute (`leaf-server/build.gradle.kts`), which is what
  `ServerBuildInfo.brandName()` reads and every other brand-related call ultimately traces back to.
  On top of that, `CraftServer.getName()` was hardcoded to a `final` field snapshotting the
  build-info name at construction time instead of reading the same live, configurable brand
  `getServerModName()` (the method that actually feeds the client's F3 brand packet) already used -
  fixed so runtime customization via `misc.rebrand.server-mod-name` still works for anyone who wants
  a name other than "AtlasSpigot". Verified twice: once with an actual simulated client connection
  capturing the literal brand packet bytes, and again by booting with *no config directory at all*
  and confirming every one of the lines above still said "AtlasSpigot". See
  `source-patches/build-manifest-brand-fix.diff` and `source-patches/craftserver-brand-fix.diff`.
  - Config files renamed too: `purpur.yml` -> `atlas.yml`, `config/leaf-global.yml` ->
    `config/atlas-global.yml` (source change in `Main.java` and `LeafConfig.java` respectively -
    see `source-patches/`). In-file credit comments pointing at the real upstream projects
    (Leaf/Purpur websites, docs, GitHub) and the `LICENSE.md`/copyright notices are left alone -
    that's honest attribution and a legal requirement of the MIT license this is built under, not
    branding to strip. The internal `Brand-Id` (`winds-studio:leaf`, used for plugin compatibility
    checks against Paper/Gale/Pufferfish/Purpur) is also left untouched deliberately - that's an
    identifier other code checks against, not display text, and changing it risks breaking plugin
    compatibility detection for no visible benefit.
- **JVM/GC** (`start.sh`): Aikar's flags, G1GC tuned for an 8GB heap. `-XX:+AlwaysPreTouch` is
  deliberately left out - it roughly doubles startup time in exchange for a marginal, usually
  unnoticeable steady-state benefit.
- **Scale** (`server.properties`, `spigot.yml`): `view-distance`/`simulation-distance` lowered
  (10/10 -> 6/4), `entity-tracking-range` roughly halved, `max-players` raised, network compression
  threshold lowered - all aimed at keeping per-player memory/CPU/network cost down as concurrent
  players climb.
- **Chunk loading/storage** (`config/paper-global.yml`, `config/atlas-global.yml`): chunk
  load/send rate uncapped, async chunk packet sending, `region-format: B_LINEAR` for smaller world
  files. (`LINEAR_V2` was tested and rejected - Leaf's own config prints a stability warning for it
  on boot; `B_LINEAR` showed no such warning.)
- **Misc performance** (`config/atlas-global.yml`): async player-data saves, distance-based mob AI
  throttling (DAB), `ALTERNATE_CURRENT` redstone engine, explosion optimization, reduced entity
  packets, item-merge radius increased, only-tick-items-in-hand, `optimize-entity-activation`
  (collects entities once per chunk region instead of re-scanning per overlapping player - verified
  against the actual source patch as behavior-preserving), `dont-save-primed-tnt` /
  `dont-save-falling-block` (cuts disk I/O when lots of TNT/falling blocks are active, at the cost
  of those entities not surviving an unload+reload).
  - Deliberately **not** enabled from the same source area: `optimize-mob-spawning` and
    `optimize-random-tick`. Both are deep rewrites of core vanilla mechanics (spawning, and the
    random ticks that drive crop growth/leaf decay/fire spread) - `optimize-mob-spawning`'s own
    patch notes say it "reduce[s] random calls," which changes vanilla's RNG consumption pattern,
    not just its speed. Not enabling either without being able to verify they're truly
    behavior-preserving.
  - Also checked and intentionally never enabled: `parallel-world-ticking`. Leaf's own issue
    tracker has a real cluster of open concurrency bugs tied to this exact experimental feature
    (crashes, a memory leak, thread blocking) - left off.

## First-boot startup time

A brand-new world's spawn chunks have to be generated before the server can finish starting -
that's a one-time cost, not something this fork controls, and it scales with how much CPU the host
gives you. On a single-vCPU container (`Paper is using 1 worker threads` in your log is the tell),
expect 30-60s on the very first boot; once the world exists on disk, restarts skip generation
entirely and are much faster.

## Credits

Built on [Leaf](https://github.com/Winds-Studio/Leaf), which itself aggregates work from
[Gale](https://github.com/GaleMC/Gale), [Pufferfish](https://github.com/pufferfish-gg/Pufferfish),
[Purpur](https://github.com/PurpurMC/Purpur), and others - see Leaf's own README for its full
credits list.
