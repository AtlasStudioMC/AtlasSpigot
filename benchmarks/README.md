# Benchmarks

Source for the measurement plugin behind the numbers on the website's
[Benchmarks](https://www.atlasspigot.dev/benchmarks) page (real MSPT comparison, AtlasSpigot vs
stock Paper, 1.21.4).

`atlas-bench/` is a minimal Paper plugin: after the server fully boots, it force-loads a fixed
chunk region around a fixed test coordinate, spawns a fixed, seeded set of entities (identical
positions across runs), waits a warmup period, then samples real per-tick timing via Paper's
`ServerTickEndEvent` for 400 consecutive ticks and writes the average to `atlas-bench-result.txt`
before shutting the server down. Same plugin, same seed, same JVM flags on both servers being
compared.

`results-1.21.4.txt` is the raw, unedited output from the actual runs behind the current
Benchmarks page - test environment: Apple M3 Pro, 18GB RAM, OpenJDK 21.0.10, `-Xms4G -Xmx4G`,
seed `2618050634530417871`, coords `183 67 -201`. AtlasSpigot ran with this project's documented
tuned config (see [`1.21.4/`](../1.21.4/)); Paper ran with its own untouched defaults.

To reproduce: build `atlas-bench` with `gradle jar` (needs the `io.papermc.paper:paper-api`
dependency from PaperMC's Maven repo), drop the jar in both servers' `plugins/` folders, and
launch each with `-Datlas.bench.label=<name> -Datlas.bench.mobcount=<N>` (plus
`-Datlas.bench.warmup=<ticks>` / `-Datlas.bench.measure=<ticks>` to override the 140/400 tick
defaults).

## Chunk generation

`atlas-chunkbench/` is the plugin behind the Benchmarks page's "Chunk generation time" section.
After startup it force-generates a fixed square chunk region (`World#getChunkAtAsync(x, z, true)`
for every chunk) centered on the same test coordinates, timing real wall-clock elapsed time from
the first request to the last chunk completing, then writes the result to
`atlas-chunkbench-result.txt` and shuts down. No players connected - a clean measure of raw
generation throughput, separate from the steady-state tick cost `atlas-bench` measures.

`results-chunkgen-1.21.4.txt` is the raw output from the runs behind the current page: same seed,
same JVM flags, same hardware as the entity-performance test, radius 50 (10,201 chunks), one run
each. AtlasSpigot: 121.868s. Paper: 134.805s.

Launch with `-Datlas.chunkbench.label=<name> -Datlas.chunkbench.radius=<N>` (radius is chunks in
each direction from center, so `N=50` generates a 101x101 region).
