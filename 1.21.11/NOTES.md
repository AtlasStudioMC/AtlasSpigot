# 1.21.11-specific notes

Full audit pass over every setting still disabled on this track, checked against **this version's
own source** rather than assumed from another track. That distinction mattered — see MC-301114
below, which behaves completely differently here than on 26.2.

## MC-301114: a real memory leak fix on this version

`fixes.vanilla-bug-fix.mc-301114` is enabled here, and it's worth being precise about why, because
the same setting means something much weaker on 26.2.

On 26.2, Paper already caps the combat tracker itself (`max-tracking-combat-entries: 10240` in
`paper-global.yml`), so Leaf's toggle only swaps *how* the cap is enforced — a cheaper ring buffer
instead of a per-damage-event scan. No new protection.

On 1.21.11 there is **no Paper cap at all**. Checked directly in this branch's
`CombatTracker.java`: the field initialises as

```java
this.entries = MCBugFix.mc301114 ? new EvictingRingList<>(max) : Lists.newArrayList();
```

…the `else` branch is a plain unbounded `ArrayList`, `recordDamageAndCheckCombatState` does a bare
`this.entries.add(combatEntry)`, and `maxTrackingCombatEntries` appears nowhere in the file. So with
this setting off — which is the stock default — a mob taking sustained damage (lava, cactus,
drowning, fire) accumulates combat entries forever. That's the actual MC-301114 leak, live and
unmitigated.

Enabling it here is a genuine bug fix, not a micro-optimisation. Note that Leaf rounds the capacity
up to the next power of two internally, so the effective bound is 16384 rather than the 10240 in
the config — still bounded, leak still fixed.

## Also enabled

- **`cache-biome`** (enabled + mob-spawning + advancements): memoises biome lookups on the paths
  that call them repeatedly per tick. Verified wired in this tree in `LocationPredicate.java` and
  four call sites in `NaturalSpawner.java` (including the chunk-aware variant). Pure cache, no
  `@Experimental`.
- **`use-virtual-thread.bukkit-async-scheduler`** and **`.download-pool`**: this branch already
  ships `auth-pool` and `paper-configuration-pool` on by default — two pools 26.2 doesn't even
  have — so this just brings the remaining two in line. No gameplay effect.

## Reviewed and deliberately left off

- **`fast-biome-manager-seed-obfuscation`** — a setting that exists on this track but not on 26.2,
  so it got a fresh look. Its module still *imports* the `Experimental` annotation without applying
  it any more, which is ambiguous, so the deciding factor was what it actually does: it replaces
  vanilla's SHA-256 seed obfuscation in `BiomeManager` with XXHash. That seed drives biome edge
  fuzzing, so changing the hash shifts biome boundaries — a worldgen deviation, same category as
  `faster-random-generator` (shifts slime chunks) and `mc-152094`. Left off.
- Everything else disabled here was assessed in the 26.2 audit for reasons that apply identically:
  `async-pathfinding` (open upstream PR), `OptimizeNonFlushPacketSending` (ProtocolLib
  incompatible), `async-switch-state` (login-handshake concurrency), `sleeping-block-entity`,
  `throttle-mob-spawning`, `cactus-check-survival`, `skip-inactive-entity-for-execute-command`, and
  the `@Experimental`-tagged modules (11 of them on this branch).

## Build notes

- Gradle 9.4.1 on this branch; built with a Java 21 toolchain. `createMojmapPaperclipJar` is the
  correct task (`createReobfPaperclipJar` exists but reobf is deprecated upstream).
- Two of the six branding patches touch files that upstream gitignores
  (`leaf-server/build.gradle.kts` and `PurpurConfig.java`), so those two diffs in
  [`source-patches/`](source-patches/) are hand-written rather than produced by `git diff`.

## Verified

Booted with the full tuned config: config loaded clean, no exceptions, brand string reads
`AtlasSpigot version 1.21.11-DEV-ver/1.21.11@762f884`, the renames produced `config/atlas-global.yml`
and `atlas.yml` (not the Leaf/Purpur names), every changed setting survived the server writing the
config back (byte-identical diff, no silent overrides), and shutdown was clean.
