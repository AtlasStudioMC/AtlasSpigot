# 1.21.4-specific notes

Confirmed by reading the actual generated config and source, not assumed:

- **`region-format` exists here, but on an older schema than 26.2/26.1.2/1.21.11.** Unlike
  1.21.5–1.21.8 (where `RegionFormatConfig.java` doesn't exist at all), this branch's version of
  the class is present but only supports `region-format-settings.region-format: MCA` or `LINEAR`
  — there is no `B_LINEAR`/`LINEAR_V2` option here. The class's own comments explicitly flag
  `LINEAR` as an experimental feature with "potential risk to lose chunk data" and recommend
  backing up before switching. Per this project's standing policy of treating upstream's own
  risk disclaimers as a hard no, this stays on the vanilla `MCA` format here.
- **`reduce-packets` only has `reduce-entity-move-packets`.** Same slim single-setting shape as
  1.21.5/1.21.6/1.21.7/1.21.8; `reduce-entity-motion-packets` and `disable-useless-particles`
  aren't present in this branch's `ReduceUselessPackets.java`.
- **`dab.enabled` defaults to `true` out of the box**, same as the other 1.21.x tracks, unlike the
  newer 26.x/1.21.11 tracks where it defaults `false`. No config change was needed for it here.
- **`optimize-block-entities` defaults to `true` out of the box in this branch** — unlike 1.21.5
  where it needed to be explicitly flipped from `false`. Confirmed by checking the freshly
  generated config before making any changes.

Everything else matches the other Leaf 1.21.x tracks' tuning exactly.
