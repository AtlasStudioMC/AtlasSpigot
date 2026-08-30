# 1.21-specific notes

## No Pufferfish tuning surface at all here

Confirmed by checking the actual decompiled source, not assumed: unlike 1.21.1 and 1.21.3, this
branch has **no `gg.pufferfish.pufferfish` package at all** - no `PufferfishConfig.java`, no
generated `pufferfish.yml`, and `org.purpurmc.purpur.PurpurConfig.java` itself has nothing
matching `dab`/`activation-range` either. Purpur merged in Pufferfish's patches (and the DAB /
inactive-goal-selector-throttle settings that come with them) starting somewhere between this
version and 1.21.1 - for this track, the only applicable tuning surface is the same
`config/paper-global.yml` / `config/paper-world-defaults.yml` settings every other track gets
(`max-joins-per-tick`, `optimize-explosions`, `redstone-implementation`). No Purpur/Pufferfish-
specific perf settings exist to enable here, so none are claimed.

## Build-tooling fix: spark's bundled native profiler crashes on boot

This branch pins `me.lucko:spark-paper:1.10.84-20240720.204128-1`. On first boot with this build,
the server crashed with a real, reproduced JVM-level segfault:

```
SIGSEGV (0xb) ... Problematic frame:
C  [spark-2a7ac38adcdd-libasyncProfiler.so.tmp+0x2dcb4]  VMThread::nativeThreadId(...)
```

This is spark's bundled native async-profiler library crashing against this environment's JVM
(Java 25, macOS arm64) - the process kept running briefly after boot but never survived to
process the `stop` command; a real crash, not a fluke. Bumped `spark-paper` to the newest
available snapshot (`1.10.133-20250413.112336-1`) and the crash was gone - clean boot, clean
shutdown, confirmed by re-running the exact same boot-test. This is a build-tooling/dependency
fix only, not a gameplay or feature change; documented in
[`source-patches/build-manifest-brand-fix.diff`](source-patches/build-manifest-brand-fix.diff).
