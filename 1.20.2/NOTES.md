# 1.20.2-specific notes

Same profile as 1.20.4: no `ServerBuildInfoImpl.java`/`Brand-Name` manifest attribute in this era,
branding comes from `CraftServer.java`'s hardcoded `serverName` field and
`PurpurConfig.serverModName`, both renamed. Pufferfish's `dab`/`inactive-goal-selector-throttle`
both default `false`, both enabled. Same paper-global/world-defaults tuning as every track. Same
harmless spark `ClassNotFoundException` on the network-monitoring thread observed on boot as
1.20.4 - spark's own issue, server shuts down clean regardless.
