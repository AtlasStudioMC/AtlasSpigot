# Roadmap

AtlasSpigot currently covers current versions down through 1.20, using whichever real upstream
project actually has buildable source for that version.

- **Leaf** - current versions. AtlasSpigot's primary base; most tuning here is Leaf's own config
  modules directly.
- **Purpur** - 1.21.3 down through 1.20, where Leaf's own branches stop. Purpur's branches go
  back further still ([verified live](https://github.com/PurpurMC/Purpur/branches) to 1.15), but
  that range is out of scope for now.

Status key: **released** = a real tagged GitHub release exists right now. **planned** = on this
list, not built yet - never claimed as available before it actually ships.

| Minecraft | Fork | Status |
|---|---|---|
| 26.2 | Leaf | released |
| 26.1.2 | Leaf | released |
| 1.21.11 | Leaf | released |
| 1.21.8 | Leaf | released |
| 1.21.7 | Leaf | released |
| 1.21.6 | Leaf | released |
| 1.21.5 | Leaf | released |
| 1.21.4 | Leaf | released |
| 1.21.3 | Purpur | released |
| 1.21.1 | Purpur | released |
| 1.21 | Purpur | released |
| 1.20.6 | Purpur | released |
| 1.20.4 | Purpur | released |
| 1.20.2 | Purpur | planned |
| 1.20.1 | Purpur | planned |
| 1.20 | Purpur | planned |

This table and the website's version grid ([`src/data/versions.ts`](https://github.com/AtlasStudioMC/Atlas-Website/blob/main/src/data/versions.ts)
in the Atlas-Website repo) are kept in sync by hand as each version ships.
