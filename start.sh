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

# -XX:+PerfDisableSharedMem keeps the JVM from writing perf data to the filesystem. It is
# part of Aikar's flags and was missing here. On a busy disk those writes stall at a
# safepoint and surface as GC latency. Cost: jps/jstat can no longer see this JVM via its
# shared-memory file, so attach by PID if you profile.

# The jar name has changed across releases: AtlasSpigot-26.2.jar, then Atlas-26.2.jar, and from
# the next build Astra-26.2.jar. Resolve whichever one is actually here instead of hardcoding a
# single name and breaking the other two. Override with JAR=/path/to/server.jar if you renamed it.
if [ -z "${JAR:-}" ]; then
  for candidate in Astra-26.2.jar Atlas-26.2.jar AtlasSpigot-26.2.jar; do
    if [ -f "$candidate" ]; then JAR="$candidate"; break; fi
  done
fi
if [ -z "${JAR:-}" ]; then
  echo "No server jar found in $(pwd)." >&2
  echo "Expected Astra-26.2.jar, Atlas-26.2.jar or AtlasSpigot-26.2.jar, or set JAR=/path/to/server.jar" >&2
  exit 1
fi
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
  -XX:+PerfDisableSharedMem \
  -XX:MaxTenuringThreshold=1 \
  -Dusing.aikars.flags=https://mcflags.emc.gs \
  -Daikars.new.flags=true \
  -jar "$JAR" nogui
