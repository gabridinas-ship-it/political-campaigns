package com.politicalcampaigns;

import net.minecraft.world.item.Item;

public class SloganItem extends Item implements PartyItem {
    private final Party party;

    public SloganItem(Item.Properties properties, Party party) {
        super(properties);
        this.party = party;
    }

    @Override
    public Party party() {
        return party;
    }
}
