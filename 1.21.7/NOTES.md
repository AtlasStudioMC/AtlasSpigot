# 1.21.7-specific notes

Same limitations as 1.21.8, caught by checking the actual generated config, not assumed:

- **No `region-format`/`B_LINEAR` support at all.** `RegionFormatConfig.java` doesn't exist in this
  branch's source. World storage stays on vanilla `MCA` here.
- **`reduce-packets` only has `reduce-entity-move-packets`.** `reduce-entity-motion-packets` and
  `disable-useless-particles` aren't present in this branch's `ReduceUselessPackets.java`.

One thing worth noting, not a limitation: **`dab.enabled` defaults to `true` out of the box** in
this version's Leaf source, unlike the newer tracks where it defaults to `false` and has to be
explicitly enabled. No config change was needed for it here - already on by default.

Everything else matches the other Leaf tracks' tuning exactly.
