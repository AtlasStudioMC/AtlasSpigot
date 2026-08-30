# 1.20.6-specific notes

Same profile as 1.21: no Pufferfish integration in this branch (no `PufferfishConfig.java`,
no `pufferfish.yml`, no `spark` dependency at all), so only the standard
`config/paper-global.yml` / `config/paper-world-defaults.yml` tuning applies
(`max-joins-per-tick`, `optimize-explosions`, `redstone-implementation`). No crashes or missing
dependencies hit during build/boot this time.
