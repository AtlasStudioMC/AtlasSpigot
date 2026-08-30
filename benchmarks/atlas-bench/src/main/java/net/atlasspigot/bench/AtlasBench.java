package net.atlasspigot.bench;

import com.destroystokyo.paper.event.server.ServerTickEndEvent;
import org.bukkit.Bukkit;
import org.bukkit.Location;
import org.bukkit.World;
import org.bukkit.entity.EntityType;
import org.bukkit.entity.LivingEntity;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.plugin.java.JavaPlugin;

import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class AtlasBench extends JavaPlugin implements Listener {

    private final List<Double> samples = new ArrayList<>();
    private boolean measuring = false;
    private int ticksLeft;
    private String label;
    private int mobCount;
    private int spawned = 0;

    @Override
    public void onEnable() {
        label = System.getProperty("atlas.bench.label", "unlabeled");
        mobCount = Integer.parseInt(System.getProperty("atlas.bench.mobcount", "300"));
        int warmupTicks = Integer.parseInt(System.getProperty("atlas.bench.warmup", "100"));
        int measureTicks = Integer.parseInt(System.getProperty("atlas.bench.measure", "400"));

        Bukkit.getPluginManager().registerEvents(this, this);

        // Wait for world to be fully up before touching chunks/entities.
        Bukkit.getScheduler().runTaskLater(this, () -> {
            World world = Bukkit.getWorlds().get(0);
            int cx = 183 >> 4;
            int cz = -201 >> 4;
            int radius = 10; // chunk radius, ~320 blocks across
            for (int dx = -radius; dx <= radius; dx++) {
                for (int dz = -radius; dz <= radius; dz++) {
                    world.getChunkAt(cx + dx, cz + dz).setForceLoaded(true);
                }
            }
            getLogger().info("[AtlasBench] Force-loaded " + ((radius * 2 + 1) * (radius * 2 + 1)) + " chunks, spawning " + mobCount + " entities...");

            Bukkit.getScheduler().runTaskLater(this, () -> spawnEntities(world, mobCount), 40L);

            Bukkit.getScheduler().runTaskLater(this, () -> {
                getLogger().info("[AtlasBench] Warmup done (" + spawned + " entities alive). Starting measurement window of " + measureTicks + " ticks...");
                measuring = true;
                ticksLeft = measureTicks;
            }, 40L + warmupTicks);

        }, 100L);
    }

    private void spawnEntities(World world, int count) {
        Random rng = new Random(12345L); // fixed seed - identical spawn layout across runs
        int baseX = 183;
        int baseY = 67;
        int baseZ = -201;
        EntityType[] types = {EntityType.ZOMBIE, EntityType.SKELETON, EntityType.SPIDER, EntityType.COW, EntityType.SHEEP};
        for (int i = 0; i < count; i++) {
            int x = baseX + rng.nextInt(200) - 100;
            int z = baseZ + rng.nextInt(200) - 100;
            int y = world.getHighestBlockYAt(x, z) + 1;
            Location loc = new Location(world, x + 0.5, y, z + 0.5);
            EntityType type = types[rng.nextInt(types.length)];
            LivingEntity e = (LivingEntity) world.spawnEntity(loc, type);
            e.setRemoveWhenFarAway(false);
            spawned++;
        }
    }

    @EventHandler
    public void onTickEnd(ServerTickEndEvent event) {
        if (!measuring) return;
        samples.add(event.getTickDuration());
        ticksLeft--;
        if (ticksLeft <= 0) {
            measuring = false;
            finish();
        }
    }

    private void finish() {
        double sum = 0;
        double max = Double.MIN_VALUE;
        double min = Double.MAX_VALUE;
        for (double d : samples) {
            sum += d;
            if (d > max) max = d;
            if (d < min) min = d;
        }
        double avg = samples.isEmpty() ? -1 : sum / samples.size();

        String line = String.format(
            "label=%s mobcount_target=%d entities_spawned=%d samples=%d avg_mspt=%.4f min_mspt=%.4f max_mspt=%.4f",
            label, mobCount, spawned, samples.size(), avg, min, max
        );
        getLogger().info("[AtlasBench] RESULT " + line);

        try (PrintWriter pw = new PrintWriter(new FileWriter("atlas-bench-result.txt", true))) {
            pw.println(line);
        } catch (Exception ex) {
            getLogger().severe("Failed to write result file: " + ex.getMessage());
        }

        Bukkit.getScheduler().runTaskLater(this, () -> Bukkit.shutdown(), 20L);
    }
}
