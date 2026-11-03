# Political Campaigns (Fabric, Minecraft Java 26.3)

Requires Java 25, Fabric Loader 0.19.5+, Fabric API 0.161.0+26.3.

## Build
1. Install JDK 25 and Gradle (or copy `gradlew`, `gradlew.bat` and `gradle/wrapper/` from the Fabric example mod).
2. If there is no wrapper yet, run `gradle wrapper --gradle-version latest` once.
3. `./gradlew build` -> jar in `build/libs/`. `./gradlew runClient` to test.
4. Open `fabricmc.net/develop` and update `loom_version`, `loader_version`, `fabric_api_version` in `gradle.properties` if they have moved.

## What you get
- Caps (worn on the head): Democratic Cap, MAGA Cap, Libertarian Gold Cap. Recipe: 2 wool + leather (gold nugget for the Libertarian cap).
- 12 slogan signs (stonecutter: blue/red/yellow carpet -> that party's signs).
- 12 posters: sign + stick in the crafting grid gives a painting (1x2) with that poster.
  Creative: `/give @s minecraft:painting[minecraft:painting/variant="political_campaigns:trump_maga"]`
- 3 logo banner patterns (paper + blue/red/yellow dye). Use them in a Loom with any banner.
- Ballot Box block (planks + paper). Right-click opens a read-only one-row chest GUI with live totals.
- Villager voting: right-click a villager holding a slogan sign or wearing a cap = +1 vote, happy sounds and particles.
  A held sign beats a worn cap. Sneak + right-click skips voting so you can still trade.
- Votes are saved per world in `political_campaigns_votes.properties` inside the world folder.

## Regenerating art
`python3 tools/generate_assets.py` (needs Pillow) rewrites all textures, models, lang, recipes and data.
The logos are crude 16x16 placeholders: replace the PNGs under `src/main/resources/assets/political_campaigns/textures/`
after generating (or edit the ASCII art in the script). Keep `SLOGANS` in the script in sync with `ModItems.java`.

## Most likely compile fixes (written without being able to compile)
- `ModItems`: creative tab import `net.fabricmc.fabric.api.creativetab.v1.CreativeModeTabEvents`, and the equipment classes
  `net.minecraft.world.item.equipment.{Equippable, EquipmentAssets, EquipmentAsset}`.
- `BallotMenu` / `BallotBoxBlock`: `MenuType.GENERIC_9x1`, `Slot.mayPlace/mayPickup`, `simpleCodec`.
- `VoteManager`: `MinecraftServer#getWorldPath(LevelResource.ROOT)`.
