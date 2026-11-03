package com.politicalcampaigns;

import net.fabricmc.fabric.api.creativetab.v1.CreativeModeTabEvents;
import net.minecraft.core.Registry;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.tags.TagKey;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.item.equipment.EquipmentAsset;
import net.minecraft.world.item.equipment.EquipmentAssets;
import net.minecraft.world.item.equipment.Equippable;
import net.minecraft.world.level.block.entity.BannerPattern;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;

public final class ModItems {
    // Keep these ids in sync with SLOGANS in tools/generate_assets.py
    public static final List<Item> SLOGAN_SIGNS = new ArrayList<>();

    public static final Item DEM_HAT = hat("dem_hat", Party.DEMOCRATIC);
    public static final Item GOP_HAT = hat("gop_hat", Party.REPUBLICAN);
    public static final Item LIB_HAT = hat("lib_hat", Party.LIBERTARIAN);

    public static final Item DEMOCRATIC_BANNER_PATTERN = patternItem(Party.DEMOCRATIC);
    public static final Item REPUBLICAN_BANNER_PATTERN = patternItem(Party.REPUBLICAN);
    public static final Item LIBERTARIAN_BANNER_PATTERN = patternItem(Party.LIBERTARIAN);

    static {
        slogan("obama_yes_we_can", Party.DEMOCRATIC);
        slogan("clinton_stronger_together", Party.DEMOCRATIC);
        slogan("clinton_im_with_her", Party.DEMOCRATIC);
        slogan("jfk_time_for_greatness", Party.DEMOCRATIC);

        slogan("trump_maga", Party.REPUBLICAN);
        slogan("trump_promises_kept", Party.REPUBLICAN);
        slogan("reagan_morning_again", Party.REPUBLICAN);
        slogan("eisenhower_i_like_ike", Party.REPUBLICAN);
        slogan("nixon_the_one", Party.REPUBLICAN);

        slogan("mcmullin_stand_for_principles", Party.LIBERTARIAN);
        slogan("paul_end_the_fed", Party.LIBERTARIAN);
        slogan("oliver_chasing_freedom", Party.LIBERTARIAN);
    }

    private ModItems() {
    }

    private static Identifier id(String name) {
        return Identifier.fromNamespaceAndPath(PoliticalCampaigns.MOD_ID, name);
    }

    private static <T extends Item> T register(String name, Function<Item.Properties, T> factory, Item.Properties properties) {
        ResourceKey<Item> key = ResourceKey.create(Registries.ITEM, id(name));
        T item = factory.apply(properties.setId(key));
        return Registry.register(BuiltInRegistries.ITEM, key, item);
    }

    private static Item hat(String name, Party party) {
        ResourceKey<EquipmentAsset> asset = ResourceKey.create(EquipmentAssets.ROOT_ID, id(name));
        Item.Properties props = new Item.Properties()
                .stacksTo(1)
                .component(DataComponents.EQUIPPABLE, Equippable.builder(EquipmentSlot.HEAD).setAsset(asset).build());
        return register(name, p -> new HatItem(p, party), props);
    }

    private static void slogan(String name, Party party) {
        SLOGAN_SIGNS.add(register(name, p -> new SloganItem(p, party), new Item.Properties().stacksTo(16)));
    }

    private static Item patternItem(Party party) {
        TagKey<BannerPattern> tag = TagKey.create(Registries.BANNER_PATTERN, id("pattern_item/" + party.id));
        Item.Properties props = new Item.Properties()
                .stacksTo(1)
                .rarity(Rarity.UNCOMMON)
                .component(DataComponents.PROVIDES_BANNER_PATTERNS, tag);
        return register(party.id + "_banner_pattern", Item::new, props);
    }

    public static void init() {
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.COMBAT).register(tab -> {
            tab.accept(DEM_HAT);
            tab.accept(GOP_HAT);
            tab.accept(LIB_HAT);
        });
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.INGREDIENTS).register(tab -> {
            tab.accept(DEMOCRATIC_BANNER_PATTERN);
            tab.accept(REPUBLICAN_BANNER_PATTERN);
            tab.accept(LIBERTARIAN_BANNER_PATTERN);
        });
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.TOOLS_AND_UTILITIES).register(tab -> {
            for (Item sign : SLOGAN_SIGNS) {
                tab.accept(sign);
            }
        });
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.FUNCTIONAL_BLOCKS).register(tab ->
                tab.accept(ModBlocks.BALLOT_BOX));
    }
}
