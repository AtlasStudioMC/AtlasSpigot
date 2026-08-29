# AtlasSpigot

A tuned, rebranded build of [Leaf](https://github.com/Winds-Studio/Leaf) (a performance-focused
Paper fork) for Minecraft 26.2.

## Getting the server jar

Grab `AtlasSpigot-26.2.jar` from this repo's [Releases](../../releases) page. It's a real source
rebuild of Leaf 26.2 (build 90) - not the stock jar - see "What's tuned here" below for what
changed and why.

## Setup

1. Put `AtlasSpigot-26.2.jar` in a folder.
2. Copy everything else from this repo into that same folder (`start.sh`, `server.properties`,
   `spigot.yml`, `purpur.yml`, `bukkit.yml`, `commands.yml`, `eula.txt`, `config/`).
3. Run it:
   ```bash
   ./start.sh
   ```
   (or `java -jar AtlasSpigot-26.2.jar nogui` directly, though `start.sh` carries the tuned JVM
   flags)

Requires Java 25 to build from source (see `source-patches/`); the built jar itself only needs
Java 17+ to run.

## What's tuned here

- **Branding**: MOTD, server-list name, console title, crash-report identifier, the console startup
  banner, the client-facing F3 brand text, and `Bukkit.getName()` (used by plugins for
  compatibility checks) all read "AtlasSpigot". The config-level pieces come from
  `server.properties` + `config/leaf-global.yml`'s `misc.rebrand` section. The rest required one
  source change - `CraftServer.getName()` hardcoded Leaf's raw build-info name instead of using
  the same configurable brand `getServerModName()` (the method that actually feeds the client's F3
  brand packet) already used. See `source-patches/craftserver-brand-fix.diff` for the exact change,
  applied against `paper-server/src/main/java/org/bukkit/craftbukkit/CraftServer.java` after
  running `./gradlew applyAllPatches` on a Leaf `ver/26.2` checkout.
- **JVM/GC** (`start.sh`): Aikar's flags, G1GC tuned for an 8GB heap. `-XX:+AlwaysPreTouch` is
  deliberately left out - it roughly doubles startup time in exchange for a marginal, usually
  unnoticeable steady-state benefit.
- **Scale** (`server.properties`, `spigot.yml`): `view-distance`/`simulation-distance` lowered
  (10/10 -> 6/4), `entity-tracking-range` roughly halved, `max-players` raised, network compression
  threshold lowered - all aimed at keeping per-player memory/CPU/network cost down as concurrent
  players climb.
- **Chunk loading/storage** (`config/paper-global.yml`, `config/leaf-global.yml`): chunk
  load/send rate uncapped, async chunk packet sending, `region-format: B_LINEAR` for smaller world
  files. (`LINEAR_V2` was tested and rejected - Leaf's own config prints a stability warning for it
  on boot; `B_LINEAR` showed no such warning.)
- **Misc performance** (`config/leaf-global.yml`): async player-data saves, distance-based mob AI
  throttling (DAB), `ALTERNATE_CURRENT` redstone engine, explosion optimization, reduced entity
  packets, item-merge radius increased, only-tick-items-in-hand.

## Credits

Built on [Leaf](https://github.com/Winds-Studio/Leaf), which itself aggregates work from
[Gale](https://github.com/GaleMC/Gale), [Pufferfish](https://github.com/pufferfish-gg/Pufferfish),
[Purpur](https://github.com/PurpurMC/Purpur), and others - see Leaf's own README for its full
credits list.
