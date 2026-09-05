# 26.1.2-specific notes

This track shipped without a config audit — every other released version had one. This is that
pass, checked against **26.1.2's own source** rather than carried over from 26.2, which turned out
to matter in both directions.

Upstream base: `3c591d7` on `ver/26.1.2`.

## Upstream has frozen this branch

The tip commit of `ver/26.1.2` is literally titled **"Mark as unsupported"** (Dreeam, 16 Jun 2026).
Leaf is no longer maintaining this branch, so anything wrong here stays wrong — no upstream fix is
coming. That raises the value of auditing it rather than lowering it, but it's worth knowing before
choosing this track: **26.2 is the maintained one.**

## MC-301114: a mechanism swap here, not a leak fix

On 1.21.11 this setting fixes a live, unmitigated memory leak. **It does not do that here**, and
the difference is worth being exact about.

`0300-Fix-MC-301114-Combat-Tracker-memory-leak.patch` on this branch reads:

```java
this.entries = MCBugFix.mc301114
    ? new EvictingRingList<>(MCBugFix.mc301114maxCombatEntries)
    : new net.minecraft.util.ArrayListDeque<>(); // Paper - Fix mem leak (MC-301114)
```

…and the `else` path keeps Paper's own trimming in `recordDamageAndCheckCombatState`, guarded by
`maxTrackingCombatEntries`. So the entry list is bounded either way. Enabling Leaf's toggle swaps a
per-damage-event trimming scan for a ring buffer that evicts in constant time — cheaper, but not
new protection. Enabled as a small win, not as a bug fix.

This is the same posture as 26.2 and the opposite of 1.21.11, where the `else` branch is an
unbounded `ArrayList` with no Paper cap at all.

## cache-biome — enabled

Memoises biome lookups on paths that hit them repeatedly per tick. Verified wired on this branch
through `0227-cache-biome-for-mob-spawning-and-advancements.patch` and
`0228-optimize-mob-spawning.patch` — six call sites across `LocationPredicate` (advancements) and
`NaturalSpawner` (mob spawning, including the chunk-aware variant). `OptimizeBiome` carries no
`@Experimental`. Pure cache, so all three keys are on.

## Virtual threads — two of four enabled

`VirtualThreadSupport` on this branch exposes `bukkit-async-scheduler`, `folia-async-scheduler`,
`async-chat-executor` and `download-pool`. Note it does **not** have `auth-pool` or
`paper-configuration-pool`, which 1.21.11 does and ships on by default — the pool set genuinely
differs per branch, so it can't be copied across.

- **`bukkit-async-scheduler`** and **`download-pool`** enabled. Both are thread-pool
  implementation swaps for work that is I/O-bound (plugin async tasks, profile fetching), which is
  what virtual threads are for. No annotations on the module.
- **`folia-async-scheduler`** left off — this isn't a Folia server, so it would be inert.
- **`async-chat-executor`** was already on; it's the upstream default.

## Left as-is

`skip-ai-for-non-aware-mob` is `true` here, which reads like a deliberate choice but is simply
`SkipAIForNonAwareMob`'s upstream default (`enabled = true`). No change.

Everything else disabled on this track was assessed in the 26.2 audit for reasons that apply
identically, including the `@Experimental`-tagged modules.

## Verified

Boot-tested with the **released** `AtlasSpigot-26.1.2.jar` rather than a local build, since config
is read at runtime and that's what users actually run:

- Booted clean on Java 25 in 13.07s, brand string `AtlasSpigot version 26.1.2-DEV-ver/26.1.2@3c591d7`.
- The config after the server wrote it back is **byte-identical** to the one supplied — none of the
  six changes were silently overridden or rejected.
- No warnings relating to biome caching, virtual threads or the combat tracker in the log.
- Clean shutdown.

Not benchmarked. No performance numbers are claimed for this track.
