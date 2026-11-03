package com.politicalcampaigns;

import net.minecraft.ChatFormatting;

public enum Party {
    DEMOCRATIC("democratic", "Democratic", ChatFormatting.BLUE),
    REPUBLICAN("republican", "Republican (GOP)", ChatFormatting.RED),
    LIBERTARIAN("libertarian", "Libertarian", ChatFormatting.GOLD);

    public final String id;
    public final String displayName;
    public final ChatFormatting color;

    Party(String id, String displayName, ChatFormatting color) {
        this.id = id;
        this.displayName = displayName;
        this.color = color;
    }
}
