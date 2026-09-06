# Low-spec profile

A configuration for AtlasSpigot 26.2 sized for a genuinely small machine: around **3GB of RAM**, an
older CPU already sitting near 100% thread usage, roughly **10GB of disk**, and a heavy plugin set
(~45).

This is not the main config with a couple of numbers nudged. It trades visible world and mob
density for tick time, deliberately and everywhere.

## Use it

Copy everything in this folder next to `AtlasSpigot-26.2.jar`, set `eula=true`, then `./start.sh`.

## The heap is the thing to get right

`start.sh` asks for **1600M**, not 3G, and that is not a mistake.

A Java server needs a significant amount of memory *outside* the heap: metaspace (which grows with
plugin count — 45 plugins is a lot of loaded classes), thread stacks, Netty's direct byte buffers,
and the JIT code cache. Budget roughly 1.0–1.4GB for that plus the OS.

Setting `-Xmx3G` on a 3GB box does not give you a bigger server. It gives you one the kernel kills,
or one that swaps and runs far worse than a smaller heap would have. If it runs comfortably for a
few days, raise it in 256M steps and watch.

`G1HeapRegionSize` is 4M rather than the usual 8M: G1 balances best with something near 2048
regions, and at a 1600M heap the standard 8M would leave it only about 200.

**Be realistic about 45 plugins on 3GB.** That is a lot of plugins for this much memory, and no
server configuration fixes it. If it will not hold, the fastest win available to you is removing
plugins you do not need — each one costs memory permanently, whether or not anyone uses it.

## What is turned down, and what it costs

**Distances** — `view-distance` 3, `simulation-distance` 2. The single biggest CPU saving here.
Players see and load far less world. Below this, chunks stop arriving fast enough to walk into.

**Entity broadcast 25%** — entities are sent to clients at a quarter of the normal distance, so
mobs and players pop in late. Large network and CPU saving on a weak machine.

**Mob caps** — monsters 40 → 15, animals 6 → 3, ambient 4 → 1. Every mob alive costs ticks forever,
so this is the biggest sustained saving after view distance. Caves and fields feel noticeably
emptier, and farm rates drop.

**Activation ranges** — animals 8, monsters 12, misc and water 4. Mobs stop ticking very close in.
Distant mobs freeze until a player is nearly on top of them.

**Despawn ranges** — monsters at 16/32, down from vanilla's 32/128.

**Merging and despawning** — item merge radius 6.0, XP merge 8.0, arrows gone in 10 seconds, junk
items in 7.5. Fewer entities on the ground at any moment.

**Tick rates** — grass spreads 8× slower, spawners tick 4× slower, container updates 5× slower.

**Chunk rates capped** — `player-max-chunk-load-rate` 25 and send rate 20, and `max-joins-per-tick`
back to 1. The main config leaves these uncapped, which is right on hardware that can absorb a
spike. Yours cannot: capping them trades slightly slower chunk loading for a server that does not
freeze when someone flies into new terrain.

**Saving spread out** — autosave every 10 minutes instead of 5, 6 chunks per tick instead of 24,
and `sync-chunk-writes=false` so the main thread does not block on disk. On an old drive this is
the difference between a periodic freeze and a smooth tick.

**Disk** — the region format is already `B_LINEAR`, which uses zstd instead of zlib and saves
roughly half the disk space. That matters at 10GB. Keep an eye on world size anyway; a pre-generated
or worldborder-limited map is the only real fix if you run out.

## What is deliberately NOT enabled here

**`hopper.disable-move-event` is off in this profile**, unlike the main config. It is the single
biggest remaining performance win, and it stops `InventoryMoveItemEvent` from firing — which shop,
sorting and economy plugins subscribe to. With 45 plugins the odds that something depends on it are
high, and a fast server that breaks your shop is not a faster server. Turn it on in
`config/paper-world-defaults.yml` if you know nothing you run watches hoppers.

**`density-function-compiler` stays off.** It compiles worldgen density functions to JVM bytecode
and sounds ideal for a CPU-bound machine, but Leaf marks the module `@Experimental`, which this
project treats as a hard no regardless of how attractive the win looks.

## About the patches

The source patches are compiled into the jar; there is nothing to switch on. Build 25 carries
sixteen of them. Using this profile means using that jar.

## Honest expectations

No performance figures are claimed. 26.2 was benchmarked against Paper and the measurement was too
noisy to publish a number from — see [`benchmarks/results-26.2.txt`](../benchmarks/results-26.2.txt).
This profile is built from settings whose behaviour is understood and documented, not from a
measured result on your hardware. Watch your own MSPT with `/spark` or `/tps` and adjust.
