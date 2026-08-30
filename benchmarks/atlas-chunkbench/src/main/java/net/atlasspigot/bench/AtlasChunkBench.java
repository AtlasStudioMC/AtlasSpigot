package net.atlasspigot.bench;

import org.bukkit.Bukkit;
import org.bukkit.World;
import org.bukkit.plugin.java.JavaPlugin;

import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.atomic.AtomicInteger;

public class AtlasChunkBench extends JavaPlugin {

    @Override
    public void onEnable() {
        String label = System.getProperty("atlas.chunkbench.label", "unlabeled");
        int radius = Integer.parseInt(System.getProperty("atlas.chunkbench.radius", "40"));

        Bukkit.getScheduler().runTaskLater(this, () -> runBenchmark(label, radius), 100L);
    }

    private void runBenchmark(String label, int radius) {
        World world = Bukkit.getWorlds().get(0);
        int cx = 183 >> 4;
        int cz = -201 >> 4;

        int side = radius * 2 + 1;
        int total = side * side;
        AtomicInteger remaining = new AtomicInteger(total);

        getLogger().info("[AtlasChunkBench] Generating " + total + " chunks (radius " + radius + ")...");
        long start = System.nanoTime();

        for (int dx = -radius; dx <= radius; dx++) {
            for (int dz = -radius; dz <= radius; dz++) {
                CompletableFuture<org.bukkit.Chunk> future = world.getChunkAtAsync(cx + dx, cz + dz, true);
                future.thenRun(() -> {
                    if (remaining.decrementAndGet() == 0) {
                        long elapsedNanos = System.nanoTime() - start;
                        finish(label, total, elapsedNanos);
                    }
                });
            }
        }
    }

    private void finish(String label, int total, long elapsedNanos) {
        double elapsedSeconds = elapsedNanos / 1_000_000_000.0;
        String line = String.format("label=%s chunks=%d elapsed_seconds=%.3f", label, total, elapsedSeconds);
        getLogger().info("[AtlasChunkBench] RESULT " + line);

        // Bukkit.getScheduler() calls must happen on main thread; the future callback may fire
        // off-thread, so hop back before touching plugin/file APIs and scheduling shutdown.
        Bukkit.getScheduler().runTask(this, () -> {
            try (PrintWriter pw = new PrintWriter(new FileWriter("atlas-chunkbench-result.txt", true))) {
                pw.println(line);
            } catch (Exception ex) {
                getLogger().severe("Failed to write result file: " + ex.getMessage());
            }
            Bukkit.getScheduler().runTaskLater(this, Bukkit::shutdown, 20L);
        });
    }
}
