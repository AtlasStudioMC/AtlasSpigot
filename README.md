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

**If you only copy the jar and skip step 2**: the server still boots, but every setting in this
README is gone - branding falls back to "Leaf", and none of the performance tuning is active. It
fails silently, not with an error, so it's easy to miss. If your console banner says "Leaf" instead
of "AtlasSpigot", this is almost always why - check that `config/atlas-global.yml` actually exists
alongside the jar and has the `misc.rebrand` section shown below.

**On a hosting panel** (Pterodactyl/Spaceify/etc.) that generates its own startup command: that
command replaces `start.sh`'s JVM flags, which is usually fine (panels often size the heap via
`-XX:MaxRAMPercentage` against the container's memory limit instead of a fixed `-Xmx`, which is a
reasonable alternative) - but you still need to upload the config files from this repo into the
container's server directory yourself, since the panel has no way to know they exist.

## What's tuned here

- **Branding**: MOTD, server-list name, console title, crash-report identifier, the console startup
  banner, the client-facing F3 brand text, and `Bukkit.getName()` (used by plugins for
  compatibility checks) all read "AtlasSpigot". The config-level pieces come from
  `server.properties` + `config/atlas-global.yml`'s `misc.rebrand` section. The rest required one
  source change - `CraftServer.getName()` hardcoded Leaf's raw build-info name instead of using
  the same configurable brand `getServerModName()` (the method that actually feeds the client's F3
  brand packet) already used. Verified with an actual simulated client connection, not just a log
  line - see `source-patches/craftserver-brand-fix.diff` for the exact change, applied against
  `paper-server/src/main/java/org/bukkit/craftbukkit/CraftServer.java` after running
  `./gradlew applyAllPatches` on a Leaf `ver/26.2` checkout.
  - Config files renamed too: `purpur.yml` -> `atlas.yml`, `config/leaf-global.yml` ->
    `config/atlas-global.yml` (source change in `Main.java` and `LeafConfig.java` respectively -
    see `source-patches/`). In-file credit comments pointing at the real upstream projects
    (Leaf/Purpur websites, docs, GitHub) are left alone - that's honest attribution to the actual
    code this is built on, not something worth papering over.
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
