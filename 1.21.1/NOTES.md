# 1.21.1-specific notes

Same Purpur-based profile as 1.21.3: `dab.enabled` and `inactive-goal-selector-throttle` both
default `false` in `pufferfish.yml` here with no risk disclaimers, both enabled. Same
`paper-global.yml`/`paper-world-defaults.yml` tuning as every other track
(`max-joins-per-tick`, `optimize-explosions`, `redstone-implementation`). Same single `atlas.yml`
(renamed from `purpur.yml`) config layout as 1.21.3.

## Build-tooling fix (not a gameplay/tuning change)

This branch pins `me.lucko:spark-paper:1.10.105-SNAPSHOT` in `build.gradle.kts`, but that
specific snapshot has since been purged from PaperMC's Maven repo (normal snapshot-artifact
lifecycle - snapshots get garbage collected over time, this is expected and not specific to this
project). Confirmed by checking the repo's actual listing: `1.10.105-SNAPSHOT` isn't there
anymore, but `1.10.84-SNAPSHOT` and `1.10.119-SNAPSHOT` still are. Bumped to `1.10.119-SNAPSHOT`
(the nearest available, and newer rather than older) purely to make this historical branch
buildable again - this only affects the bundled spark profiler dependency resolution at build
time, not any AtlasSpigot tuning or gameplay behavior. Documented in
[`source-patches/build-manifest-brand-fix.diff`](source-patches/build-manifest-brand-fix.diff).
