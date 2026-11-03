package com.politicalcampaigns;

import net.fabricmc.fabric.api.event.player.UseEntityCallback;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;

public final class VillagerVoting {
    private VillagerVoting() {
    }

    public static void register() {
        UseEntityCallback.EVENT.register((player, level, hand, entity, hitResult) -> {
            // The callback runs once per hand; only handle the main hand so a vote is never counted twice.
            if (hand != InteractionHand.MAIN_HAND || player.isSpectator()) {
                return InteractionResult.PASS;
            }
            if (entity.getType() != EntityType.VILLAGER) {
                return InteractionResult.PASS;
            }
            // Sneak + right-click skips voting so you can still trade while wearing a hat.
            if (player.isShiftKeyDown()) {
                return InteractionResult.PASS;
            }
            Party party = partyOf(player);
            if (party == null) {
                return InteractionResult.PASS;
            }
            if (level instanceof ServerLevel serverLevel) {
                VoteManager.addVote(party);
                entity.playSound(SoundEvents.VILLAGER_YES, 1.0F, 1.0F);
                serverLevel.sendParticles(ParticleTypes.HAPPY_VILLAGER,
                        entity.getX(), entity.getY() + entity.getBbHeight() * 0.8, entity.getZ(),
                        8, 0.4, 0.4, 0.4, 0.0);
            }
            return InteractionResult.SUCCESS;
        });
    }

    /** A held slogan wins over a worn hat. Main hand is checked before the off hand. */
    private static Party partyOf(Player player) {
        ItemStack main = player.getMainHandItem();
        if (main.getItem() instanceof SloganItem slogan) {
            return slogan.party();
        }
        ItemStack off = player.getOffhandItem();
        if (off.getItem() instanceof SloganItem slogan) {
            return slogan.party();
        }
        ItemStack head = player.getItemBySlot(EquipmentSlot.HEAD);
        if (head.getItem() instanceof HatItem hat) {
            return hat.party();
        }
        return null;
    }
}
