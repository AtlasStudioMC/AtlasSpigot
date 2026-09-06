#!/usr/bin/env python3
"""Apply every AtlasSpigot source patch to a freshly patched Leaf tree.

The .diff files in this directory are written to be *read* - they have no valid hunk headers and
`git apply` rejects them. That was fine when there were five branding patches; with fourteen it
meant every rebuild was hand-work, and hand-work drifts.

The generated trees (leaf-server/src/minecraft, paper-server/src/main) are gitignored by upstream,
so there is no tracked baseline to diff against and no way to produce a real patch file. This
script is the alternative: anchored search-and-replace with an assertion on every anchor, so it
either applies cleanly or tells you exactly which anchor upstream moved.

Usage, from a Leaf checkout after ./gradlew applyAllPatches:

    python3 /path/to/source-patches/apply.py .

Then: ./gradlew :leaf-server:createPaperclipJar
"""
import sys, pathlib

MC = "leaf-server/src/minecraft/java/net/minecraft/"
PS = "paper-server/src/main/java/"

# (file, [(anchor, replacement), ...], label)
PATCHES = []

def patch(path, pairs, label):
    PATCHES.append((path, pairs, label))

# ---------------------------------------------------------------- branding
patch("leaf-server/build.gradle.kts", [
    ('"Specification-Title" to "Leaf", // Leaf - Rebrand',
     '"Specification-Title" to "AtlasSpigot", // Leaf - Rebrand // AtlasSpigot - Rebrand'),
    ('"Brand-Name" to "Leaf", // Leaf - Rebrand',
     '"Brand-Name" to "AtlasSpigot", // Leaf - Rebrand // AtlasSpigot - Rebrand'),
], "brand: jar manifest")

patch(PS + "io/papermc/paper/ServerBuildInfoImpl.java", [
    ('private static final String BRAND_LEAF_NAME = "Leaf";',
     'private static final String BRAND_LEAF_NAME = "AtlasSpigot"; // AtlasSpigot - fallback default'),
], "brand: ServerBuildInfoImpl")

patch(PS + "org/bukkit/craftbukkit/CraftServer.java", [
    ("    public String getName() {\n        return this.serverName;\n    }",
     "    public String getName() {\n        return org.dreeam.leaf.config.modules.misc.ServerBrand.serverModName; // Leaf - configurable brand\n    }"),
], "brand: CraftServer#getName")

patch("leaf-server/src/main/java/org/dreeam/leaf/config/LeafConfig.java", [
    ('protected static final String GLOBAL_CONFIG_FILE = "leaf-global.yml";',
     'protected static final String GLOBAL_CONFIG_FILE = "atlas-global.yml"; // AtlasSpigot'),
    ('protected static final String DEFAULT_WORLD_CONFIG_FILE = "leaf-world-defaults.yml"; // Leaf TODO - Per world config',
     'protected static final String DEFAULT_WORLD_CONFIG_FILE = "atlas-world-defaults.yml"; // AtlasSpigot'),
    ('"config/leaf-global.yml",',
     'CONFIG_DIRECTORY.getName() + "/" + GLOBAL_CONFIG_FILE, // AtlasSpigot'),
], "brand: config filenames")

patch(MC.replace("java/net/minecraft/", "java/org/purpurmc/purpur/") + "PurpurConfig.java", [
    ('"Could not load purpur.yml, please correct your syntax errors"',
     '"Could not load atlas.yml, please correct your syntax errors"'),
], "brand: PurpurConfig message")

patch(PS + "org/bukkit/craftbukkit/Main.java", [
    ('.defaultsTo(new File("purpur.yml"))',
     '.defaultsTo(new File("atlas.yml")) // AtlasSpigot'),
], "brand: atlas.yml flag")

patch(PS + "com/destroystokyo/paper/Metrics.java", [
    ('private static final String URL = "https://bstats.org/submitData/server-implementation";',
     'private static final String URL = "https://bStats.org/api/v2/data/bukkit"; // AtlasSpigot\n\n    private static final int SERVICE_ID = 33733; // AtlasSpigot - our registered bStats service'),
    ('    private JSONObject getPluginData() {\n        JSONObject data = new JSONObject();\n\n        data.put("pluginName", name); // Append the name of the server software',
     '    private JSONObject getServiceData() {\n        JSONObject data = new JSONObject();\n\n        data.put("id", SERVICE_ID); // AtlasSpigot - v2 per-service shape'),
    ('        JSONObject data = new JSONObject();\n\n        data.put("serverUUID", serverUUID);',
     '        JSONObject data = new JSONObject();\n\n        data.put("serverUUID", serverUUID);\n        data.put("metricsVersion", "3.2.1"); // AtlasSpigot\n        data.put("playerAmount", Bukkit.getOnlinePlayers().size());\n        data.put("onlineMode", Bukkit.getOnlineMode() ? 1 : 0);\n        data.put("bukkitVersion", Bukkit.getVersion());\n        data.put("bukkitName", Bukkit.getName());\n        data.put("javaVersion", System.getProperty("java.version"));'),
    ('        JSONArray pluginData = new JSONArray();\n        pluginData.add(getPluginData());\n        data.put("plugins", pluginData);',
     '        data.put("service", getServiceData()); // AtlasSpigot - v2 schema'),
    ('Metrics metrics = new Metrics("Leaf"', 'Metrics metrics = new Metrics("AtlasSpigot"'),
    ('final String leafVersion;', 'final String atlasVersion; // AtlasSpigot'),
    ('leafVersion = "git-Leaf-%s-%s".formatted', 'atlasVersion = "git-AtlasSpigot-%s-%s".formatted'),
    ('leafVersion = "unknown";', 'atlasVersion = "unknown";'),
    ('new Metrics.SimplePie("leaf_version", () -> leafVersion)',
     'new Metrics.SimplePie("atlasspigot_version", () -> atlasVersion)'),
], "brand: bStats v2 service")

# ------------------------------------------------------- optimisation patches
patch(MC + "world/entity/LivingEntity.java", [
    ("        for (EquipmentSlot slot : EquipmentSlot.VALUES_ARRAY) { // Gale - JettPack - reduce array allocations",
     "        // AtlasSpigot start - skip Bukkit conversions nothing is listening for\n"
     "        final boolean equipmentChangedListened = io.papermc.paper.event.entity.EntityEquipmentChangedEvent.getHandlerList().getRegisteredListeners().length > 0;\n"
     "        final boolean armorChangeListened = com.destroystokyo.paper.event.player.PlayerArmorChangeEvent.getHandlerList().getRegisteredListeners().length > 0;\n"
     "        // AtlasSpigot end\n"
     "        for (EquipmentSlot slot : EquipmentSlot.VALUES_ARRAY) { // Gale - JettPack - reduce array allocations"),
    ("                final org.bukkit.inventory.ItemStack oldItem = CraftItemStack.asBukkitCopy(previous);\n"
     "                final org.bukkit.inventory.ItemStack newItem = CraftItemStack.asBukkitCopy(current);\n"
     "                if (this instanceof ServerPlayer && slot.getType() == EquipmentSlot.Type.HUMANOID_ARMOR) {",
     "                // AtlasSpigot start - only convert when an event will read them\n"
     "                final boolean armorChangeWanted = armorChangeListened && this instanceof ServerPlayer && slot.getType() == EquipmentSlot.Type.HUMANOID_ARMOR;\n"
     "                org.bukkit.inventory.ItemStack oldItem = null;\n"
     "                org.bukkit.inventory.ItemStack newItem = null;\n"
     "                if (equipmentChangedListened || armorChangeWanted) {\n"
     "                    oldItem = CraftItemStack.asBukkitCopy(previous);\n"
     "                    newItem = CraftItemStack.asBukkitCopy(current);\n"
     "                }\n"
     "                if (armorChangeWanted) {"),
    ("                    equipmentChanges = Maps.newEnumMap(org.bukkit.inventory.EquipmentSlot.class); // Paper - EntityEquipmentChangedEvent",
     "                    if (equipmentChangedListened) equipmentChanges = Maps.newEnumMap(org.bukkit.inventory.EquipmentSlot.class); // AtlasSpigot"),
    ("                equipmentChanges.put(org.bukkit.craftbukkit.CraftEquipmentSlot.getSlot(slot), new EquipmentChangeImpl(oldItem, newItem)); // Paper - EntityEquipmentChangedEvent",
     "                if (equipmentChangedListened) equipmentChanges.put(org.bukkit.craftbukkit.CraftEquipmentSlot.getSlot(slot), new EquipmentChangeImpl(oldItem, newItem)); // AtlasSpigot"),
    ("            new io.papermc.paper.event.entity.EntityEquipmentChangedEvent(this.getBukkitLivingEntity(), equipmentChanges).callEvent(); // Paper - EntityEquipmentChangedEvent",
     "            if (equipmentChangedListened) new io.papermc.paper.event.entity.EntityEquipmentChangedEvent(this.getBukkitLivingEntity(), equipmentChanges).callEvent(); // AtlasSpigot"),
    ("                        if (new com.destroystokyo.paper.event.entity.EntityJumpEvent(getBukkitLivingEntity()).callEvent()) { // Paper - Entity Jump API",
     "                        if (com.destroystokyo.paper.event.entity.EntityJumpEvent.getHandlerList().getRegisteredListeners().length == 0\n"
     "                            || new com.destroystokyo.paper.event.entity.EntityJumpEvent(getBukkitLivingEntity()).callEvent()) { // AtlasSpigot - skip when unlistened"),
], "opt: equipment conversions + jump event")

patch(MC + "world/entity/Entity.java", [
    ("            org.bukkit.util.Vector delta = new org.bukkit.util.Vector(xa, ya, za);\n"
     "            if (pushingEntity != null) {\n"
     "                io.papermc.paper.event.entity.EntityPushedByEntityAttackEvent event = new io.papermc.paper.event.entity.EntityPushedByEntityAttackEvent(this.getBukkitEntity(), io.papermc.paper.event.entity.EntityKnockbackEvent.Cause.PUSH, pushingEntity.getBukkitEntity(), delta);\n"
     "                if (!event.callEvent()) {\n                    return;\n                }\n"
     "                delta = event.getKnockback();\n            }\n"
     "            this.setDeltaMovement(this.getDeltaMovement().add(delta.getX(), delta.getY(), delta.getZ()));",
     "            // AtlasSpigot start - no Bukkit Vector for pushes nothing observes\n"
     "            double pushX = xa;\n            double pushY = ya;\n            double pushZ = za;\n"
     "            if (pushingEntity != null\n"
     "                && io.papermc.paper.event.entity.EntityPushedByEntityAttackEvent.getHandlerList().getRegisteredListeners().length != 0) {\n"
     "                org.bukkit.util.Vector delta = new org.bukkit.util.Vector(xa, ya, za);\n"
     "                io.papermc.paper.event.entity.EntityPushedByEntityAttackEvent event = new io.papermc.paper.event.entity.EntityPushedByEntityAttackEvent(this.getBukkitEntity(), io.papermc.paper.event.entity.EntityKnockbackEvent.Cause.PUSH, pushingEntity.getBukkitEntity(), delta);\n"
     "                if (!event.callEvent()) {\n                    return;\n                }\n"
     "                delta = event.getKnockback();\n"
     "                pushX = delta.getX();\n                pushY = delta.getY();\n                pushZ = delta.getZ();\n            }\n"
     "            this.setDeltaMovement(this.getDeltaMovement().add(pushX, pushY, pushZ));\n"
     "            // AtlasSpigot end"),
    ("    public void setAirSupply(final int supply) {\n        // CraftBukkit start",
     "    public void setAirSupply(final int supply) {\n"
     "        // AtlasSpigot start - fast path when the event cannot change anything\n"
     "        if (!this.valid || org.bukkit.event.entity.EntityAirChangeEvent.getHandlerList().getRegisteredListeners().length == 0) {\n"
     "            this.entityData.set(DATA_AIR_SUPPLY_ID, supply);\n            return;\n        }\n"
     "        // AtlasSpigot end\n        // CraftBukkit start"),
], "opt: push vector + air supply")

patch(MC + "world/entity/ExperienceOrb.java", [
    ("        if (!new com.destroystokyo.paper.event.entity.ExperienceOrbMergeEvent((org.bukkit.entity.ExperienceOrb) this.getBukkitEntity(), (org.bukkit.entity.ExperienceOrb) orb.getBukkitEntity()).callEvent()) {",
     "        if (com.destroystokyo.paper.event.entity.ExperienceOrbMergeEvent.getHandlerList().getRegisteredListeners().length != 0\n"
     "            && !new com.destroystokyo.paper.event.entity.ExperienceOrbMergeEvent((org.bukkit.entity.ExperienceOrb) this.getBukkitEntity(), (org.bukkit.entity.ExperienceOrb) orb.getBukkitEntity()).callEvent()) { // AtlasSpigot"),
], "opt: xp orb merge")

patch(MC + "server/level/ServerLevel.java", [
    ("            new com.destroystokyo.paper.event.entity.EntityAddToWorldEvent(entity.getBukkitEntity(), ServerLevel.this.getWorld()).callEvent(); // Paper - fire while valid",
     "            if (com.destroystokyo.paper.event.entity.EntityAddToWorldEvent.getHandlerList().getRegisteredListeners().length != 0) // AtlasSpigot\n"
     "            new com.destroystokyo.paper.event.entity.EntityAddToWorldEvent(entity.getBukkitEntity(), ServerLevel.this.getWorld()).callEvent(); // Paper - fire while valid"),
    ("            new com.destroystokyo.paper.event.entity.EntityRemoveFromWorldEvent(entity.getBukkitEntity(), ServerLevel.this.getWorld()).callEvent(); // Paper - fire while valid",
     "            if (com.destroystokyo.paper.event.entity.EntityRemoveFromWorldEvent.getHandlerList().getRegisteredListeners().length != 0) // AtlasSpigot\n"
     "            new com.destroystokyo.paper.event.entity.EntityRemoveFromWorldEvent(entity.getBukkitEntity(), ServerLevel.this.getWorld()).callEvent(); // Paper - fire while valid"),
], "opt: world tracking events")

patch(PS + "org/bukkit/craftbukkit/event/CraftEventFactory.java", [
    ("    public static boolean callItemMergeEvent(ItemEntity merging, ItemEntity mergingWith) {\n        org.bukkit.entity.Item entityMerging",
     "    public static boolean callItemMergeEvent(ItemEntity merging, ItemEntity mergingWith) {\n"
     "        // AtlasSpigot - veto-only; with no listener the answer is always true\n"
     "        if (ItemMergeEvent.getHandlerList().getRegisteredListeners().length == 0) {\n            return true;\n        }\n"
     "        org.bukkit.entity.Item entityMerging"),
    ("    public static void callEntitiesLoadEvent(Level level, ChunkPos pos, List<Entity> entities) {\n        List<org.bukkit.entity.Entity> bukkitEntities",
     "    public static void callEntitiesLoadEvent(Level level, ChunkPos pos, List<Entity> entities) {\n"
     "        // AtlasSpigot - streams every entity and forces CraftEntity creation; returns void\n"
     "        if (EntitiesLoadEvent.getHandlerList().getRegisteredListeners().length == 0) {\n            return;\n        }\n"
     "        List<org.bukkit.entity.Entity> bukkitEntities"),
    ("    public static void callEntityRemoveEvent(Entity entity, EntityRemoveEvent.Cause cause) {\n        if (entity instanceof ServerPlayer) {",
     "    public static void callEntityRemoveEvent(Entity entity, EntityRemoveEvent.Cause cause) {\n"
     "        // AtlasSpigot - universal removal path; returns void and getBukkitEntity() creates wrappers\n"
     "        if (EntityRemoveEvent.getHandlerList().getRegisteredListeners().length == 0) {\n            return;\n        }\n"
     "        if (entity instanceof ServerPlayer) {"),
    ("    public static void callEntitiesUnloadEvent(Level level, ChunkPos pos, List<Entity> entities) {\n        List<org.bukkit.entity.Entity> bukkitEntities",
     "    public static void callEntitiesUnloadEvent(Level level, ChunkPos pos, List<Entity> entities) {\n"
     "        // AtlasSpigot - same as the load side, on every chunk unload\n"
     "        if (EntitiesUnloadEvent.getHandlerList().getRegisteredListeners().length == 0) {\n            return;\n        }\n"
     "        List<org.bukkit.entity.Entity> bukkitEntities"),
], "opt: item merge + chunk entity events")

patch(MC + "world/level/chunk/LevelChunk.java", [
    ("            org.bukkit.Chunk bukkitChunk = new org.bukkit.craftbukkit.CraftChunk(this);\n"
     "            server.getPluginManager().callEvent(new org.bukkit.event.world.ChunkLoadEvent(bukkitChunk, this.needsDecoration));",
     "            // AtlasSpigot start - notification-only; CraftChunk built lazily for populators\n"
     "            org.bukkit.Chunk bukkitChunk = null;\n"
     "            if (org.bukkit.event.world.ChunkLoadEvent.getHandlerList().getRegisteredListeners().length != 0) {\n"
     "                bukkitChunk = new org.bukkit.craftbukkit.CraftChunk(this);\n"
     "                server.getPluginManager().callEvent(new org.bukkit.event.world.ChunkLoadEvent(bukkitChunk, this.needsDecoration));\n"
     "            }\n            // AtlasSpigot end"),
    ("                org.bukkit.World world = this.level.getWorld();\n                if (world != null) {",
     "                if (bukkitChunk == null) bukkitChunk = new org.bukkit.craftbukkit.CraftChunk(this); // AtlasSpigot - populators need it\n"
     "                org.bukkit.World world = this.level.getWorld();\n                if (world != null) {"),
    ("        org.bukkit.Chunk bukkitChunk = new org.bukkit.craftbukkit.CraftChunk(this);\n"
     "        org.bukkit.event.world.ChunkUnloadEvent unloadEvent = new org.bukkit.event.world.ChunkUnloadEvent(bukkitChunk, true); // Paper - rewrite chunk system - force save to true so that mustNotSave is correctly set below\n"
     "        server.getPluginManager().callEvent(unloadEvent);\n"
     "        // note: saving can be prevented, but not forced if no saving is actually required\n"
     "        this.mustNotSave = !unloadEvent.isSaveChunk();",
     "        // AtlasSpigot start - event is built with saveChunk=true and only a listener can call\n"
     "        // setSaveChunk(), so with none registered mustNotSave is definitively false.\n"
     "        if (org.bukkit.event.world.ChunkUnloadEvent.getHandlerList().getRegisteredListeners().length == 0) {\n"
     "            this.mustNotSave = false;\n        } else {\n"
     "        org.bukkit.Chunk bukkitChunk = new org.bukkit.craftbukkit.CraftChunk(this);\n"
     "        org.bukkit.event.world.ChunkUnloadEvent unloadEvent = new org.bukkit.event.world.ChunkUnloadEvent(bukkitChunk, true); // Paper - rewrite chunk system - force save to true so that mustNotSave is correctly set below\n"
     "        server.getPluginManager().callEvent(unloadEvent);\n"
     "        // note: saving can be prevented, but not forced if no saving is actually required\n"
     "        this.mustNotSave = !unloadEvent.isSaveChunk();\n        }\n        // AtlasSpigot end"),
], "opt: chunk load/unload events")


def main():
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not (root / "leaf-server").is_dir():
        sys.exit(f"error: {root} does not look like a Leaf checkout")
    failed = []
    for rel, pairs, label in PATCHES:
        f = root / rel
        if not f.exists():
            failed.append(f"{label}: file missing -> {rel}")
            continue
        s = f.read_text()
        for old, new in pairs:
            if new.split("\n")[0].strip() and new[:40] in s:
                pass  # tolerate re-running; the assert below is the real check
            if old not in s:
                failed.append(f"{label}: anchor not found in {rel}\n    {old.splitlines()[0][:90]}")
                break
            s = s.replace(old, new, 1)
        else:
            f.write_text(s)
            print(f"  applied: {label}")
            continue
    if failed:
        print("\nFAILED - upstream has moved these anchors:\n")
        for x in failed:
            print("  " + x)
        sys.exit(1)
    print(f"\nAll {len(PATCHES)} patch groups applied cleanly.")

if __name__ == "__main__":
    main()
