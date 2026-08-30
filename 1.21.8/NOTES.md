# 1.21.8-specific notes

This Leaf branch is missing two things present on the newer tracks (26.2, 26.1.2, 1.21.11) -
caught by checking the actual generated config, not assumed from another track:

- **No `region-format`/`B_LINEAR` support at all.** `RegionFormatConfig.java` doesn't exist in this
  branch's source. World storage stays on the vanilla `MCA` format here - not a missed setting,
  the feature itself doesn't exist yet in this version of Leaf.
- **`reduce-packets` only has `reduce-entity-move-packets`.** `reduce-entity-motion-packets` and
  `disable-useless-particles` aren't present in this branch's `ReduceUselessPackets.java` - only
  the one sub-setting that exists is enabled here.

Everything else matches the other Leaf tracks' tuning exactly.
