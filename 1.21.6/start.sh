#!/bin/bash
# Aikar's flags: https://docs.papermc.io/paper/aikars-flags
# Tuned G1GC settings that consistently reduce GC pause times / stutter on
# Minecraft servers vs default JVM settings - this matters far more for
# "many players on limited RAM" than any raw heap size number does.
#
# -Xms == -Xmx on purpose: letting the heap resize at runtime causes extra
# GC pauses exactly when the server is under the most load (more players).
#
# NOTE: -XX:+AlwaysPreTouch is intentionally left OUT. It forces the OS to
# physically commit and zero the entire heap before the JVM does anything
# else - that's what was making startup take ~30s. Without it the server
# boots in a fraction of the time; the tradeoff is a few extra (usually
# unnoticeable) page faults during the first seconds of real load instead
# of upfront. Add it back if you'd rather trade startup time for that.

MEMORY="8G"

java -Xms${MEMORY} -Xmx${MEMORY} \
  -XX:+UseG1GC \
  -XX:+ParallelRefProcEnabled \
  -XX:MaxGCPauseMillis=200 \
  -XX:+UnlockExperimentalVMOptions \
  -XX:+DisableExplicitGC \
  -XX:G1NewSizePercent=30 \
  -XX:G1MaxNewSizePercent=40 \
  -XX:G1HeapRegionSize=8M \
  -XX:G1ReservePercent=20 \
  -XX:G1HeapWastePercent=5 \
  -XX:G1MixedGCCountTarget=4 \
  -XX:InitiatingHeapOccupancyPercent=15 \
  -XX:G1MixedGCLiveThresholdPercent=90 \
  -XX:G1RSetUpdatingPauseTimePercent=5 \
  -XX:SurvivorRatio=32 \
  -XX:MaxTenuringThreshold=1 \
  -Dusing.aikars.flags=https://mcflags.emc.gs \
  -Daikars.new.flags=true \
  -jar AtlasSpigot-1.21.6.jar nogui
