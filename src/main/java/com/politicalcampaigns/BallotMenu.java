package com.politicalcampaigns;

import net.minecraft.ChatFormatting;
import net.minecraft.core.component.DataComponents;
import net.minecraft.network.chat.Component;
import net.minecraft.world.Container;
import net.minecraft.world.SimpleContainer;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.MenuType;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;

/**
 * Read-only server-side menu shown as a one-row chest GUI. The vanilla client already knows how to draw
 * GENERIC_9x1, so the mod needs no client code. Slot order matches ChestMenu (9 container, 27 inventory, 9 hotbar).
 */
public class BallotMenu extends AbstractContainerMenu {
    private final SimpleContainer display = new SimpleContainer(9);

    public BallotMenu(int containerId, Inventory playerInventory) {
        super(MenuType.GENERIC_9x1, containerId);
        refresh();

        for (int c = 0; c < 9; c++) {
            this.addSlot(new DisplaySlot(display, c, 8 + c * 18, 18));
        }
        for (int r = 0; r < 3; r++) {
            for (int c = 0; c < 9; c++) {
                this.addSlot(new Slot(playerInventory, c + r * 9 + 9, 8 + c * 18, 50 + r * 18));
            }
        }
        for (int c = 0; c < 9; c++) {
            this.addSlot(new Slot(playerInventory, c, 8 + c * 18, 108));
        }
    }

    private void refresh() {
        display.setItem(1, entry(ModItems.DEM_HAT, Party.DEMOCRATIC));
        display.setItem(3, entry(ModItems.GOP_HAT, Party.REPUBLICAN));
        display.setItem(5, entry(ModItems.LIB_HAT, Party.LIBERTARIAN));

        int total = VoteManager.total();
        ItemStack sum = new ItemStack(Items.PAPER);
        sum.set(DataComponents.ITEM_NAME,
                Component.literal("Total: " + total + (total == 1 ? " vote" : " votes")).withStyle(ChatFormatting.WHITE));
        display.setItem(7, sum);
    }

    private static ItemStack entry(Item icon, Party party) {
        int votes = VoteManager.get(party);
        ItemStack stack = new ItemStack(icon);
        stack.set(DataComponents.ITEM_NAME,
                Component.literal(party.displayName + ": " + votes + (votes == 1 ? " vote" : " votes")).withStyle(party.color));
        return stack;
    }

    @Override
    public void broadcastChanges() {
        refresh(); // keeps the numbers live while the box is open
        super.broadcastChanges();
    }

    @Override
    public ItemStack quickMoveStack(Player player, int index) {
        return ItemStack.EMPTY;
    }

    @Override
    public boolean stillValid(Player player) {
        return true;
    }

    private static final class DisplaySlot extends Slot {
        DisplaySlot(Container container, int index, int x, int y) {
            super(container, index, x, y);
        }

        @Override
        public boolean mayPlace(ItemStack stack) {
            return false;
        }

        @Override
        public boolean mayPickup(Player player) {
            return false;
        }
    }
}
