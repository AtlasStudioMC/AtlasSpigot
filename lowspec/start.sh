#!/bin/bash
# Atlas 26.2 - low-spec profile
#
# Sized for roughly 3GB total RAM, an older CPU that is already near 100% thread usage,
# and ~10GB of disk.
#
# HEAP SIZING - the important part.
#
# 1600M is not the whole 3GB on purpose. A Java server needs a good deal of memory
# *outside* the heap: metaspace (which grows with plugin count - 45 plugins is a lot),
# thread stacks, Netty's direct byte buffers, and the JIT code cache. Budget roughly
# 1.0-1.4GB for that plus the operating system.
#
# Setting -Xmx to 3G on a 3GB box does not give you a bigger server. It gives you a
# server the kernel kills, or one that swaps and runs far worse than a smaller heap
# would have. If you have headroom after watching it run, raise this in 256M steps.
#
# -Xms == -Xmx deliberately: a heap that resizes does so by pausing, and it will choose
# to do that exactly when the server is busiest.
MEMORY="1600M"

# G1HeapRegionSize is 4M rather than the usual 8M. G1 wants somewhere near 2048 regions
# to balance well; at a 1600M heap, 8M regions would give it only ~200 to work with.
java -Xms${MEMORY} -Xmx${MEMORY} \
  -XX:+UseG1GC \
  -XX:+ParallelRefProcEnabled \
  -XX:MaxGCPauseMillis=200 \
  -XX:+UnlockExperimentalVMOptions \
  -XX:+DisableExplicitGC \
  -XX:G1NewSizePercent=30 \
  -XX:G1MaxNewSizePercent=40 \
  -XX:G1HeapRegionSize=4M \
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
  -jar Atlas-26.2.jar nogui
