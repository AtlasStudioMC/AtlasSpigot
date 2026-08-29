# JVM flags for hosting panels (Pterodactyl/Spaceify/etc.)

If you're running on a panel, it generates its own `java` command and ignores
`start.sh` entirely — which means none of the G1GC tuning in `start.sh` was ever
applied on that deployment. Panels typically let you override the flags in the
startup command / environment variable (often called something like
`JAVA_ARGS` or similar in the panel's egg/config).

Replace the flags with this (keeps the panel's dynamic RAM-percentage sizing,
which is the right call in a container where you don't know the exact memory
limit ahead of time, and adds the same Aikar's-flags G1GC tuning from
`start.sh`):

```
-Xms128M -XX:MaxRAMPercentage=95.0 -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:MaxTenuringThreshold=1 -jar {{SERVER_JARFILE}} nogui
```

(`{{SERVER_JARFILE}}` is Pterodactyl-style templating for whatever the jar is
named on that panel - replace with the literal filename, e.g.
`AtlasSpigot-26.2.jar`, if your panel doesn't support that placeholder.)

Left out on purpose: `-XX:+AlwaysPreTouch` (roughly doubles startup time to
pre-commit the whole heap upfront - not worth it, same reasoning as `start.sh`).

Why `-Xms128M` and not a fixed `-Xms`/`-Xmx` pair like `start.sh` uses: on a
panel you don't know the container's memory limit at the time you write the
config, so `MaxRAMPercentage` sizing to whatever the panel actually allocates
is more correct than guessing a fixed number - a low starting heap plus a
percentage-based ceiling is the standard pattern for this exact deployment
style. If you know the fixed amount of RAM the container always gets, `start.sh`'s
approach (equal `-Xms`/`-Xmx`) avoids runtime heap-resize pauses entirely and
is the better choice.
