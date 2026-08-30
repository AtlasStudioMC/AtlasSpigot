# Roadmap

AtlasSpigot's goal is full coverage across Minecraft's history, using whichever real upstream
project actually has buildable source for that version - not one fork stretched further back than
its own maintainers take it.

- **Leaf** - current versions. AtlasSpigot's primary base; most tuning here is Leaf's own config
  modules directly.
- **Purpur** - versions back to 1.15, where Leaf's own branches stop but
  [Purpur's still have live source](https://github.com/PurpurMC/Purpur/branches) (verified against
  their actual branch list, not assumed).
- **Paper/Spigot** - the oldest versions, back to 1.8.8. Paper's GitHub repo no longer keeps live
  source branches this old (they get pruned once EOL - verified: their own branch list has nothing
  before ~1.21.4, though their downloads API confirms these versions were real, official releases
  once). This tier builds via Spigot/CraftBukkit's BuildTools instead, which is what TacoSpigot
  (this project's own starting point) already is.

Status key: **released** = a real tagged GitHub release exists right now. **planned** = on this
list, not built yet - never claimed as available before it actually ships.

| Minecraft | Fork | Status |
|---|---|---|
| 26.2 | Leaf | released |
| 26.1.2 | Leaf | released |
| 1.21.11 | Leaf | released |
| 1.21.8 | Leaf | released |
| 1.21.7 | Leaf | planned |
| 1.21.6 | Leaf | planned |
| 1.21.5 | Leaf | planned |
| 1.21.4 | Leaf | planned |
| 1.21.3 | Purpur | planned |
| 1.21.1 | Purpur | planned |
| 1.21 | Purpur | planned |
| 1.20.6 | Purpur | planned |
| 1.20.4 | Purpur | planned |
| 1.20.2 | Purpur | planned |
| 1.20.1 | Purpur | planned |
| 1.20 | Purpur | planned |
| 1.19.4 | Purpur | planned |
| 1.19.3 | Purpur | planned |
| 1.19.2 | Purpur | planned |
| 1.19.1 | Purpur | planned |
| 1.19 | Purpur | planned |
| 1.18.2 | Purpur | planned |
| 1.18.1 | Purpur | planned |
| 1.18 | Purpur | planned |
| 1.17.1 | Purpur | planned |
| 1.16.5 | Purpur | planned |
| 1.16.4 | Purpur | planned |
| 1.16.3 | Purpur | planned |
| 1.16.2 | Purpur | planned |
| 1.15 | Purpur | planned |
| 1.14.4 | Paper/Spigot | planned |
| 1.13.2 | Paper/Spigot | planned |
| 1.12.2 | Paper/Spigot | planned |
| 1.11.2 | Paper/Spigot | planned |
| 1.10.2 | Paper/Spigot | planned |
| 1.9.4 | Paper/Spigot | planned |
| 1.8.8 | Paper/Spigot | planned |

This table and the website's version grid ([`src/data/versions.ts`](https://github.com/AtlasStudioMC/Atlas-Website/blob/main/src/data/versions.ts)
in the Atlas-Website repo) are kept in sync by hand as each version ships.
