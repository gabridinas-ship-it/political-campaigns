package com.politicalcampaigns;

import net.minecraft.world.item.Item;

public class HatItem extends Item implements PartyItem {
    private final Party party;

    public HatItem(Item.Properties properties, Party party) {
        super(properties);
        this.party = party;
    }

    @Override
    public Party party() {
        return party;
    }
}
