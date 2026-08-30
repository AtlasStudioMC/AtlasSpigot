# 1.20-specific notes

Same old-era branding as 1.20.1/1.20.2/1.20.4 (hardcoded `serverName` field +
`PurpurConfig.serverModName`). Real finding: unlike those three, this version's boot **does not
generate `pufferfish.yml` at all**, even though `PufferfishConfig.java` exists in the source tree
- it's simply not wired into the load path here. So the only applicable tuning surface for this
version is the standard `config/paper-global.yml` / `config/paper-world-defaults.yml` settings.
Clean boot both fresh and tuned, no crashes.

This is the last version in the Purpur tier - track stops at 1.20 per project scope; 1.19 and
below are out of scope for now.
