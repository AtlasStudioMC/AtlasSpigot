# 1.21.3-specific notes

First Purpur-based track. Confirmed by reading the actual generated config and source, not assumed.

## Build/fork differences vs the Leaf tracks

- **Different config surface entirely.** Purpur doesn't have Leaf's reflection-scanned config
  module system. Its own settings live directly in `org.purpurmc.purpur.PurpurConfig.java`
  (mostly gameplay/feature toggles, not perf-tuning — confirmed by grepping for
  `async`/`optimiz`/`throttle` patterns, which returned nothing there). The actual perf-tuning
  surface for this fork family is `gg.pufferfish.pufferfish.PufferfishConfig.java`
  (generates `pufferfish.yml`), plus the same Paper `config/paper-global.yml` /
  `config/paper-world-defaults.yml` split Paper itself ships.
- **Single global config file (`atlas.yml`, renamed from `purpur.yml`)** instead of Leaf's
  two-file global/per-world split — Purpur nests per-world overrides inside the same file under
  `world-settings.<name>.*`, there's no separate world-defaults file for it.
- **Build task naming differs from Leaf's `applyAllPatches`/`leaf-server` layout**: this fork uses
  the `paperweight.patcher` Gradle plugin, so the task is `applyPatches` and the generated/patched
  working tree is `Purpur-Server/` (a real git repo here, not gitignored like Leaf's
  `leaf-server/build.gradle.kts` was — so these patches came straight from `git diff`).
  `createMojmapPaperclipJar` is the correct jar-build task (same conclusion as 1.21.4's Leaf
  track — `reobf` is deprecated upstream and fails outright if attempted).

## Tuning applied (verified against source before enabling)

- `pufferfish.yml`: `dab.enabled` and `inactive-goal-selector-throttle` both default to `false` on
  this fork (unlike Leaf, where the DAB-equivalent typically defaults `true`) — enabled both after
  confirming neither carries any experimental/risk disclaimer in `PufferfishConfig.java`'s source
  comments.
- `config/paper-global.yml` / `config/paper-world-defaults.yml`: same three settings as every
  Leaf track (`max-joins-per-tick`, `optimize-explosions`, `redstone-implementation`), same stock
  defaults, same tuned values — this part of Paper's config is unchanged by either fork.

## Runtime finding (not a config change, just worth knowing)

- Pufferfish's SIMD optimizations only self-enable on Java 17–21; booting on Java 25 (this
  project's default dev/runtime JDK) logs `[Pufferfish] Will not enable SIMD!` and silently skips
  that optimization. The server still boots and runs fine either way — this is a real, observed
  runtime message, not an error, but worth knowing if you want that specific optimization active.
