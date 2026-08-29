# AtlasSpigot

A tuned, rebranded configuration layer on top of [Leaf](https://github.com/Winds-Studio/Leaf) (a
performance-focused Paper fork) for Minecraft 26.2.

This repo contains the **configuration**, not a custom-built server jar. Leaf itself is unmodified -
grab the official release jar from the link below (or the latest one from Leaf's own releases page)
and drop these config files in alongside it.

## Getting the server jar

Download the official Leaf 26.2 release jar directly from upstream:

https://github.com/Winds-Studio/Leaf/releases/download/ver-26.2/leaf-26.2-90.jar

Or grab it from this repo's [Releases](../../releases) page, where it's attached alongside these
configs for convenience.

## Setup

1. Put `leaf-26.2-90.jar` in a folder.
2. Copy everything from this repo into that same folder (`start.sh`, `server.properties`,
   `spigot.yml`, `purpur.yml`, `bukkit.yml`, `commands.yml`, `eula.txt`, `config/`).
3. Run it:
   ```bash
   ./start.sh
   ```
   (or `java -jar leaf-26.2-90.jar nogui` directly, though `start.sh` carries the tuned JVM flags)

Requires Java 17+.

## What's tuned here

- **Branding**: MOTD, server-list name, console title, and crash-report identifier all read
  "AtlasSpigot" (`server.properties` + `config/leaf-global.yml`'s `misc.rebrand` section). The
  console startup banner and F3 client brand are unaffected - those are hardcoded in Leaf's own
  source and would require a full source rebuild to change.
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
