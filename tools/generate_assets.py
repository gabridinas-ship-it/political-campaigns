#!/usr/bin/env python3
"""Generates every texture, model, lang, recipe and data file for the mod.

Run from the project root:   python3 tools/generate_assets.py     (needs Pillow)
Edit the textures/ASCII logos below or replace the PNGs by hand afterwards.
Keep SLOGANS in sync with ModItems.java.
"""
import json
import os
from PIL import Image, ImageDraw

MOD = "political_campaigns"
HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "src", "main", "resources")
ASSETS = os.path.join(RES, "assets", MOD)
DATA = os.path.join(RES, "data", MOD)

PARTIES = {
    "democratic": dict(name="Democratic", hat="dem_hat", hat_name="Democratic Cap",
                       main=(37, 99, 235), dark=(18, 45, 130), light=(200, 218, 255),
                       logo_fg=(255, 255, 255), logo_detail=(18, 45, 130),
                       dye="blue_dye", carpet="blue_carpet", wool="blue_wool", extra="leather", logo="donkey"),
    "republican": dict(name="Republican (GOP)", hat="gop_hat", hat_name="MAGA Cap",
                       main=(220, 38, 38), dark=(120, 15, 15), light=(255, 210, 210),
                       logo_fg=(255, 255, 255), logo_detail=(120, 15, 15),
                       dye="red_dye", carpet="red_carpet", wool="red_wool", extra="leather", logo="elephant"),
    "libertarian": dict(name="Libertarian", hat="lib_hat", hat_name="Libertarian Gold Cap",
                        main=(240, 190, 20), dark=(120, 85, 0), light=(255, 245, 180),
                        logo_fg=(70, 45, 0), logo_detail=(255, 245, 180),
                        dye="yellow_dye", carpet="yellow_carpet", wool="yellow_wool", extra="gold_nugget", logo="porcupine"),
}

# (id, party, candidate, slogan, initials, variant)
SLOGANS = [
    ("obama_yes_we_can", "democratic", "Obama", "Yes We Can", "OBA", 0),
    ("clinton_stronger_together", "democratic", "Clinton", "Stronger Together", "CLI", 0),
    ("clinton_im_with_her", "democratic", "Clinton", "I'm With Her", "CLI", 1),
    ("jfk_time_for_greatness", "democratic", "JFK", "A Time for Greatness", "JFK", 0),
    ("trump_maga", "republican", "Trump", "Make America Great Again", "TRU", 0),
    ("trump_promises_kept", "republican", "Trump", "Promises Made, Promises Kept", "TRU", 1),
    ("reagan_morning_again", "republican", "Reagan", "It's Morning Again in America", "REA", 0),
    ("eisenhower_i_like_ike", "republican", "Eisenhower", "I Like Ike", "IKE", 0),
    ("nixon_the_one", "republican", "Nixon", "Nixon's the One", "NIX", 0),
    ("mcmullin_stand_for_principles", "libertarian", "McMullin", "Stand for Principles", "MCM", 0),
    ("paul_end_the_fed", "libertarian", "Ron Paul", "End the Fed", "PAU", 0),
    ("oliver_chasing_freedom", "libertarian", "Chase Oliver", "Chase-ing Freedom", "OLI", 0),
]

# 16x16 logos. X = main colour, o = detail colour, . = empty
LOGOS = {
    "donkey": [
        "..XXX......XXX..",
        ".XXXXX....XXXXX.",
        ".XXXXX....XXXXX.",
        ".XXXXXX..XXXXXX.",
        "..XXXXXXXXXXXX..",
        "..XXXXXXXXXXXX..",
        "..XXooXXXXooXX..",
        "..XXXXXXXXXXXX..",
        "...XXXXXXXXXX...",
        "...XXXXXXXXXX...",
        "....XXXXXXXX....",
        "....XXXXXXXX....",
        "....XXoXXoXX....",
        "....XXXXXXXX....",
        ".....XXXXXX.....",
        "................",
    ],
    "elephant": [
        "................",
        "..XXXXXXXXXXXX..",
        ".XXXXXXXXXXXXXX.",
        "XXXXXXXXXXXXXXXX",
        "XXXXXXXXXXXXXXXX",
        "XXXXoXXXXXXoXXXX",
        "XXXXXXXXXXXXXXXX",
        "XXXXXXXXXXXXXXXX",
        ".XXXXXXooXXXXXX.",
        ".XXXXXXooXXXXXX.",
        "..XXXXXooXXXXX..",
        "...XXXXooXXXX...",
        "....XXXooXXX....",
        ".....XXooXX.....",
        "......XXXX......",
        "................",
    ],
    "porcupine": [
        "....X..X..X.....",
        "...XX.XX.XX.XX..",
        "..XXXXXXXXXXXXX.",
        ".XXXXXXXXXXXXXXX",
        ".XXXXXXXXXXXXXXX",
        ".XXXXXXXXXXXXXXX",
        ".XXXXXXXXXXXXoXX",
        "..XXXXXXXXXXXXXX",
        "..XXXXXXXXXXXXXo",
        "...XXXXXXXXXXXX.",
        "...XXXXXXXXXXXX.",
        "....XXXXXXXXXX..",
        "....XX.XX.XX.XX.",
        "................",
        "................",
        "................",
    ],
}

FONT = {
    "A": [".X.", "X.X", "XXX", "X.X", "X.X"], "B": ["XX.", "X.X", "XX.", "X.X", "XX."],
    "C": [".XX", "X..", "X..", "X..", ".XX"], "E": ["XXX", "X..", "XX.", "X..", "XXX"],
    "F": ["XXX", "X..", "XX.", "X..", "X.."], "I": ["XXX", ".X.", ".X.", ".X.", "XXX"],
    "J": ["..X", "..X", "..X", "X.X", ".X."], "K": ["X.X", "X.X", "XX.", "X.X", "X.X"],
    "L": ["X..", "X..", "X..", "X..", "XXX"], "M": ["X.X", "XXX", "XXX", "X.X", "X.X"],
    "N": ["XX.", "X.X", "X.X", "X.X", "X.X"], "O": [".X.", "X.X", "X.X", "X.X", ".X."],
    "P": ["XX.", "X.X", "XX.", "X..", "X.."], "R": ["XX.", "X.X", "XX.", "X.X", "X.X"],
    "T": ["XXX", ".X.", ".X.", ".X.", ".X."], "U": ["X.X", "X.X", "X.X", "X.X", "XXX"],
    "X": ["X.X", "X.X", ".X.", "X.X", "X.X"],
}

COLORS = ["white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray",
          "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black"]


def rgba(c, a=255):
    return (c[0], c[1], c[2], a)


def save_png(im, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path)


def save_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


def draw_logo(im, art, ox, oy, fg, detail, size=16):
    for dy in range(size):
        for dx in range(size):
            ch = art[dy * 16 // size][dx * 16 // size]
            if ch == "X":
                im.putpixel((ox + dx, oy + dy), rgba(fg))
            elif ch == "o":
                im.putpixel((ox + dx, oy + dy), rgba(detail))


def hat_icon(p):
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([6, 3, 9, 3], fill=rgba(p["dark"]))
    d.rectangle([5, 4, 10, 4], fill=rgba(p["main"]))
    d.rectangle([4, 5, 11, 5], fill=rgba(p["main"]))
    d.rectangle([3, 6, 12, 9], fill=rgba(p["main"]))
    d.rectangle([3, 9, 12, 9], fill=rgba(p["dark"]))
    d.rectangle([3, 10, 14, 11], fill=rgba(p["dark"]))
    d.rectangle([7, 6, 8, 7], fill=rgba(p["light"]))
    return im


def hat_layer(p):
    """64x32 humanoid armour layer: a cap sitting on the upper half of the head."""
    im = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([8, 0, 15, 7], fill=rgba(p["main"]))
    for x0 in (0, 8, 16, 24):
        d.rectangle([x0, 8, x0 + 7, 11], fill=rgba(p["main"]))
    d.rectangle([8, 12, 15, 13], fill=rgba(p["dark"]))
    d.rectangle([11, 9, 12, 10], fill=rgba(p["light"]))
    return im


def sign_icon(p):
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([7, 9, 8, 15], fill=(120, 85, 45, 255))
    d.rectangle([1, 1, 14, 9], fill=rgba(p["dark"]))
    d.rectangle([2, 2, 13, 8], fill=rgba(p["main"]))
    d.rectangle([4, 4, 11, 4], fill=rgba(p["light"]))
    d.rectangle([4, 6, 9, 6], fill=rgba(p["light"]))
    return im


def pattern_icon(p):
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([2, 1, 13, 14], fill=(235, 230, 215, 255))
    d.rectangle([2, 1, 13, 1], fill=(190, 185, 170, 255))
    d.rectangle([2, 14, 13, 14], fill=(190, 185, 170, 255))
    art = LOGOS[p["logo"]]
    detail = p["dark"]
    draw_logo(im, art, 2, 2, p["main"] if p["logo"] != "porcupine" else p["dark"], detail, size=12)
    return im


def ballot_box_texture():
    im = Image.new("RGBA", (16, 16), (150, 108, 60, 255))
    d = ImageDraw.Draw(im)
    for y in range(0, 16, 4):
        d.rectangle([0, y, 15, y], fill=(132, 94, 50, 255))
    d.rectangle([0, 0, 15, 15], outline=(90, 62, 30, 255))
    d.rectangle([4, 3, 11, 4], fill=(25, 18, 10, 255))
    d.rectangle([2, 10, 5, 13], fill=rgba(PARTIES["democratic"]["main"]))
    d.rectangle([6, 10, 9, 13], fill=rgba(PARTIES["republican"]["main"]))
    d.rectangle([10, 10, 13, 13], fill=rgba(PARTIES["libertarian"]["main"]))
    return im


def poster_texture(party, initials, variant):
    p = PARTIES[party]
    im = Image.new("RGBA", (16, 32), rgba(p["dark"]))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 15, 18], fill=rgba(p["main"]))
    draw_logo(im, LOGOS[p["logo"]], 0, 1, p["logo_fg"], p["logo_detail"])
    d.rectangle([0, 0, 15, 0], fill=rgba(p["light"]))
    d.rectangle([0, 19, 15, 19], fill=rgba(p["light"]))
    d.rectangle([0, 31, 15, 31], fill=rgba(p["light"]))
    x = 2
    for ch in initials:
        for gy, row in enumerate(FONT[ch]):
            for gx, cell in enumerate(row):
                if cell == "X":
                    im.putpixel((x + gx, 22 + gy), rgba(p["light"]))
        x += 4
    for i in range(variant + 1):
        d.rectangle([2 + i * 3, 29, 3 + i * 3, 29], fill=rgba(p["light"]))
    return im


def banner_mask(art, size, ox, oy, canvas=64):
    im = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    for dy in range(size):
        for dx in range(size):
            ch = art[dy * 16 // size][dx * 16 // size]
            if ch == "X":
                im.putpixel((ox + dx, oy + dy), (255, 255, 255, 255))
            elif ch == "o":
                im.putpixel((ox + dx, oy + dy), (120, 120, 120, 255))
    return im


def item_model(item_id, texture):
    save_json(os.path.join(ASSETS, "models", "item", item_id + ".json"),
              {"parent": "minecraft:item/generated", "textures": {"layer0": f"{MOD}:item/{texture}"}})
    save_json(os.path.join(ASSETS, "items", item_id + ".json"),
              {"model": {"type": "minecraft:model", "model": f"{MOD}:item/{item_id}"}})


def main():
    lang = {"container.political_campaigns.ballot_box": "Ballot Box",
            "block.political_campaigns.ballot_box": "Ballot Box"}

    # ---------- hats ----------
    for key, p in PARTIES.items():
        hid = p["hat"]
        save_png(hat_icon(p), f"{ASSETS}/textures/item/{hid}.png")
        save_png(hat_layer(p), f"{ASSETS}/textures/entity/equipment/humanoid/{hid}.png")
        save_json(f"{ASSETS}/equipment/{hid}.json", {"layers": {"humanoid": [{"texture": f"{MOD}:{hid}"}]}})
        item_model(hid, hid)
        lang[f"item.{MOD}.{hid}"] = p["hat_name"]
        save_json(f"{DATA}/recipe/{hid}.json", {
            "type": "minecraft:crafting_shapeless",
            "ingredients": [f"minecraft:{p['wool']}", f"minecraft:{p['wool']}", f"minecraft:{p['extra']}"],
            "result": {"id": f"{MOD}:{hid}", "count": 1}})

        # ---------- sign + banner pattern textures per party ----------
        save_png(sign_icon(p), f"{ASSETS}/textures/item/sign_{key}.png")
        save_png(pattern_icon(p), f"{ASSETS}/textures/item/{key}_banner_pattern.png")
        item_model(f"{key}_banner_pattern", f"{key}_banner_pattern")
        lang[f"item.{MOD}.{key}_banner_pattern"] = f"Banner Pattern ({p['name']} Logo)"
        save_json(f"{DATA}/recipe/{key}_banner_pattern.json", {
            "type": "minecraft:crafting_shapeless",
            "ingredients": ["minecraft:paper", f"minecraft:{p['dye']}"],
            "result": {"id": f"{MOD}:{key}_banner_pattern", "count": 1}})

        # banner pattern definition, its tag and textures
        save_json(f"{DATA}/banner_pattern/{key}.json",
                  {"asset_id": f"{MOD}:{key}", "translation_key": f"block.{MOD}.banner.{key}"})
        save_json(f"{DATA}/tags/banner_pattern/pattern_item/{key}.json", {"values": [f"{MOD}:{key}"]})
        art = LOGOS[p["logo"]]
        save_png(banner_mask(art, 16, 3, 13), f"{ASSETS}/textures/entity/banner/{key}.png")
        save_png(banner_mask(art, 10, 2, 7), f"{ASSETS}/textures/entity/shield/{key}.png")
        for color in COLORS:
            lang[f"block.{MOD}.banner.{key}.{color}"] = f"{color.replace('_', ' ').title()} {p['name']} Logo"

    # ---------- slogan signs + posters ----------
    for sid, party, cand, slogan, initials, variant in SLOGANS:
        p = PARTIES[party]
        item_model(sid, f"sign_{party}")
        lang[f"item.{MOD}.{sid}"] = f"{cand} Sign: {slogan}"

        save_png(poster_texture(party, initials, variant), f"{ASSETS}/textures/painting/{sid}.png")
        save_json(f"{DATA}/painting_variant/{sid}.json", {
            "asset_id": f"{MOD}:{sid}", "width": 1, "height": 2,
            "title": {"text": slogan, "color": "yellow"},
            "author": {"text": cand, "color": "gray"}})

        # carpet -> sign via stonecutter (one carpet colour per party)
        save_json(f"{DATA}/recipe/{sid}_sign.json", {
            "type": "minecraft:stonecutting",
            "ingredient": f"minecraft:{p['carpet']}",
            "result": {"id": f"{MOD}:{sid}", "count": 1}})
        # sign + stick -> poster (a painting with a fixed variant)
        save_json(f"{DATA}/recipe/{sid}_poster.json", {
            "type": "minecraft:crafting_shapeless",
            "ingredients": [f"{MOD}:{sid}", "minecraft:stick"],
            "result": {"id": "minecraft:painting", "count": 1,
                       "components": {"minecraft:painting/variant": f"{MOD}:{sid}"}}})

    # ---------- ballot box ----------
    save_png(ballot_box_texture(), f"{ASSETS}/textures/block/ballot_box.png")
    save_json(f"{ASSETS}/blockstates/ballot_box.json", {"variants": {"": {"model": f"{MOD}:block/ballot_box"}}})
    save_json(f"{ASSETS}/models/block/ballot_box.json",
              {"parent": "minecraft:block/cube_all", "textures": {"all": f"{MOD}:block/ballot_box"}})
    save_json(f"{ASSETS}/items/ballot_box.json",
              {"model": {"type": "minecraft:model", "model": f"{MOD}:block/ballot_box"}})
    save_json(f"{DATA}/loot_table/blocks/ballot_box.json", {
        "type": "minecraft:block",
        "pools": [{"rolls": 1, "entries": [{"type": "minecraft:item", "name": f"{MOD}:ballot_box"}],
                   "conditions": [{"condition": "minecraft:survives_explosion"}]}]})
    save_json(os.path.join(RES, "data", "minecraft", "tags", "block", "mineable", "axe.json"),
              {"values": [f"{MOD}:ballot_box"]})
    save_json(f"{DATA}/recipe/ballot_box.json", {
        "type": "minecraft:crafting_shaped",
        "pattern": ["#P#", "# #", "###"],
        "key": {"#": "minecraft:oak_planks", "P": "minecraft:paper"},
        "result": {"id": f"{MOD}:ballot_box", "count": 1}})

    save_json(f"{ASSETS}/lang/en_us.json", lang)
    print("generated", len(lang), "lang entries")


if __name__ == "__main__":
    main()
