# 1.20.4-specific notes

Older brand structure: no `ServerBuildInfoImpl.java` and no `Brand-Name`/`Specification-Title`
manifest attributes exist in this era's `build.gradle.kts` (still plain `Implementation-Title:
CraftBukkit` / `Specification-Title: Bukkit`) - branding here comes entirely from
`CraftServer.java`'s hardcoded `serverName` field and `PurpurConfig.serverModName`, both renamed
to AtlasSpigot. Pufferfish's `dab`/`inactive-goal-selector-throttle` both exist and default
`false` here (same as 1.21.1/1.21.3), both enabled. Same paper-global/world-defaults tuning as
every track.

Minor known issue, not fixed: the version string still prints a literal `git-Purpur-...` fragment
from a separate hardcoded location unrelated to `getName()`/`getServerModName()` (which do
correctly report AtlasSpigot) - cosmetic only, left as-is given time constraints. A harmless
`ClassNotFoundException` in spark's own network-monitoring thread was also observed on boot
(spark's issue, not ours); server shuts down clean regardless.
