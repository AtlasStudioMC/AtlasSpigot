# 1.21.6-specific notes

Same profile as 1.21.7, confirmed by checking the actual generated config, not assumed:

- **No `region-format`/`B_LINEAR` support at all.** `RegionFormatConfig.java` doesn't exist in this
  branch's source. World storage stays on vanilla `MCA` here.
- **`reduce-packets` only has `reduce-entity-move-packets`.** `reduce-entity-motion-packets` and
  `disable-useless-particles` aren't present in this branch's `ReduceUselessPackets.java`.
- **`dab.enabled` defaults to `true` out of the box** (verified in `DynamicActivationofBrain.java`),
  unlike the newer tracks where it defaults `false`. No config change was needed for it here.

Everything else matches the other Leaf tracks' tuning exactly.
