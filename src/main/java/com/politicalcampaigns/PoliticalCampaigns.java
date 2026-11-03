package com.politicalcampaigns;

import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class PoliticalCampaigns implements ModInitializer {
    public static final String MOD_ID = "political_campaigns";
    public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

    @Override
    public void onInitialize() {
        ModBlocks.init();
        ModItems.init();
        VillagerVoting.register();

        ServerLifecycleEvents.SERVER_STARTED.register(VoteManager::load);
        ServerLifecycleEvents.SERVER_STOPPING.register(server -> VoteManager.save());
        ServerLifecycleEvents.SERVER_STOPPED.register(server -> VoteManager.unload());
    }
}
