package com.politicalcampaigns;

import net.minecraft.server.MinecraftServer;
import net.minecraft.world.level.storage.LevelResource;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.EnumMap;
import java.util.Map;
import java.util.Properties;

/** Stores the vote totals per world in a small properties file next to level.dat. */
public final class VoteManager {
    private static final Map<Party, Integer> VOTES = new EnumMap<>(Party.class);
    private static Path file;

    static {
        reset();
    }

    private VoteManager() {
    }

    private static void reset() {
        for (Party party : Party.values()) {
            VOTES.put(party, 0);
        }
    }

    public static synchronized void load(MinecraftServer server) {
        file = server.getWorldPath(LevelResource.ROOT).resolve("political_campaigns_votes.properties");
        reset();
        if (!Files.exists(file)) {
            return;
        }
        Properties props = new Properties();
        try (InputStream in = Files.newInputStream(file)) {
            props.load(in);
        } catch (IOException e) {
            PoliticalCampaigns.LOGGER.error("Could not read votes file", e);
            return;
        }
        for (Party party : Party.values()) {
            try {
                VOTES.put(party, Math.max(0, Integer.parseInt(props.getProperty(party.id, "0").trim())));
            } catch (NumberFormatException ignored) {
                VOTES.put(party, 0);
            }
        }
    }

    public static synchronized void save() {
        if (file == null) {
            return;
        }
        Properties props = new Properties();
        for (Party party : Party.values()) {
            props.setProperty(party.id, Integer.toString(VOTES.get(party)));
        }
        try (OutputStream out = Files.newOutputStream(file)) {
            props.store(out, "Political Campaigns vote totals");
        } catch (IOException e) {
            PoliticalCampaigns.LOGGER.error("Could not write votes file", e);
        }
    }

    public static synchronized void unload() {
        save();
        file = null;
        reset();
    }

    public static synchronized int get(Party party) {
        return VOTES.get(party);
    }

    public static synchronized int total() {
        int sum = 0;
        for (int v : VOTES.values()) {
            sum += v;
        }
        return sum;
    }

    public static synchronized int addVote(Party party) {
        int now = VOTES.get(party) + 1;
        VOTES.put(party, now);
        save();
        return now;
    }
}
