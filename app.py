from http.client import responses
import os
import requests
import numpy
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from datetime import datetime
from bs4 import BeautifulSoup
from helpers import *

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# API Key - might use pset 9's way of hiding API key (os.environ.get("API_KEY"))
key = "5a0827f1-cf40-4ea6-9891-5a5a323b5f35"

# Get Bingo Card API Data from Hypixel - id, name, lore, required amount
response = (requests.get("https://api.hypixel.net/resources/skyblock/bingo")).json()
bingo_id = response["id"]

armor_list = [{"name":'Leather Armor', "id":'LEATHER'}, {"name":'Golden Armor', "id":'GOLD'}, {"name": 'Chainmail Armor', "id":"CHAINMAIL"}, {"name":'Iron Armor', "id":"IRON"}, {"name":'Diamond Armor', "id":"DIAMOND"}, {"name":'Farm Suit', "id":"FARM"}, {"name":'Mushroom Armor', "id":"MUSHROOM"}, {"name":'Pumpkin Armor', "id":"PUMPKIN"}, {"name":'Cactus Armor', "id":"CACTUS"}, {"name":'Leaflet Armor',"id":"LEAFLET"}, {"name":'Miner Armor',"id":"TANK"}, {"name":'Lapis Armor',"id":"LAPIS"}, {"name":'Angler Armor',"id":"ANGLER"}, {"name":"Rosetta's Armor","id":"ROSETTA"}, {"name":'Squire Armor',"id":"SQUIRE"}, {"name":'Celeste Armor', "id":"CELESTE"}, {"name":'Mercenary Armor',"id":"MERCENARY"}, {"name":'Starlight Armor', "id":"STARLIGHT"}]
accessory_list = ['Zombie Talisman', 'Skeleton Talisman', 'Village Affinity Talisman', 'Mine Affinity Talisman', 'Intimidation Talisman', 'Scavenger Talisman', 'Wolf Paw', "Pig's Foot", "Melody's Hair", 'Shiny Yellow Rock', 'Campfire Initiate Badge', 'Cat Talisman', 'King Talisman', 'Red Claw Talisman', 'Spider Talisman', 'Vaccine Talisman', 'Farming Talisman', 'Talisman of Coins', 'Magnetic Talisman', 'Gravity Talisman', 'Speed Talisman', 'Potion Affinity Talisman']
pet_list = ['Bingo', 'Grandma Wolf', 'Bee', 'Rock', 'Dolphin', 'Jerry', 'Rabbit', 'Pig', 'Silverfish', 'Armadillo', 'Enderman', 'An Oringo Pet']

health_steps = [("Mushroom Armor", 165), ("Growth V", 900), ("Titanic (Armor Reforge, Uncommon)", 120), ("Crab-Colored Century Cake", 10)]
scc_steps = [("Angler V", 5), ("Beacon V (Friend's)", 5), ("Angler Armor", 4), ("Sea Emperor Century Cake", 1)]
strength_steps = [("Bingo Pet (Lv. 50+)", 15), ("Strength VIII Potion (Friend's)", 75), ("Overflux Power Orb (Friend's)", 25), ("Raider Axe (Base, Reforged to Epic)", 105), ("Fierce (Armor Reforge, Rare+)", 24)]
ferocity_steps = [("Dirty (Reforge, Uncommon+)", 3), ("Latest Update Century Cake", 2)]
crit_damage_steps = [("Critical (Enchantment)", 50), ("Spicy (Meelee Reforge, Rare+)", 45), ("Fierce (Armor Reforge, Rare+)", 40), ("Critical IV Potion (Friend's)", 40), ("Beacon V (Friend's)", 10)]
crit_chance_steps = [("Odd (Meelee Reforge, Rare+)", 15), ("Clean (Armor Reforge, Rare+)", 24), ("Critical IV Potion (Friend's)", 25), ("Beacon V (Friend's)", 5), ("Fortuitous Power (Accessory)", 3)]
speed_steps = [("Godsplash (#BongoBrewers)", 220), ("Farm Suit", 20), ("Rogue Sword", 30), ("Hunter Knife", 40), ("Haste Block (Friend's)", 100), ("Potato-Style Century Cake (Friend's", 10)]

money_steps = [("Spider Relics", 310000), ("Kill Goblins/Farm Wheat/Other Money Making Method", 100000000)]

dchest_prices = [("Wood", 0), ("Gold", 25000), ("Diamond", 50000), ("Emerald", 100000), ("Obsidian", 250000)]

unique_minions = ["Cobblestone", "Sand", "Coal", "Iron", "Gold", "Diamond", "Lapis Lazuli", "Redstone", "Emerald", "Oak", "Spruce", "Birch", "Dark Oak", "Acacia", "Jungle", "Wheat", "Melon", "Pumpkin", "Carrot", "Potato", "Mushroom", "Cactus", "Cocoa Beans", "Sugar Cane", "Cow", "Pig", "Chicken", "Sheep", "Rabbit"]

# Loads data into database
db = SQL("sqlite:///bingo.db")

# TODO: ALTER DATABASE WHEN NECESSARY
db.execute("DELETE FROM bingo")
for dict in response["goals"]:
    unloads = ""
    eta = 0
    minion = ""
    strategy = ""

    id = dict["id"].lower()
    name = dict["name"]
    if "lore" in dict:
        lore = dict["lore"]
        lore = color(lore)
    else:
        lore = "Community Goal!"
    
    if "requiredAmount" in dict:
        requiredAmount = dict["requiredAmount"]
    else:
        requiredAmount = ""

    # TODO: Collection Goal, use minion.
    if "collection" in id:
        method = "MINION"
        # Parse item to query
        try:
            item = id.replace('collection_', '')

            # Select minion from item (sometimes minion name is different from item)
            minion = (db.execute("SELECT type FROM miniondata WHERE tier=1 AND ugMaterial LIKE ?", item))[0]["type"]

        except:
            # In case weird name (Eg. 'ender stone' entered as opposed to 'end stone')
            item = name.replace(' Collector', '')

            minion = db.execute("SELECT type FROM miniondata WHERE tier=1 AND ugMaterial LIKE ?", item)[0]["type"]
        
            

        # Find tier 4 stats
        info = db.execute("SELECT delay, storage FROM miniondata WHERE tier=4 AND type=?", minion)
        timePerItem = ((info[0]["delay"]) * 2) / 3600
        storage = (info[0]["storage"]) + 576 # Medium Storages (TODO: Calculate if user has more minion slots, use small storages)
        # Find time (in HOURS) WITH 5 MINIONS to get collection
        eta = round((requiredAmount * timePerItem) / 5)
        unloads = int(numpy.ceil(eta / (timePerItem * storage)))
        timePerUnload = eta / unloads

        strategy = "One second..."

    # TODO: Craft Goal, determine if worth minion, and how much minion.
    # TODO: For crafting: take into account 
    # Couldn't do "craft" in id b/c craft_minions is a goal but it's crafting 40 unique minions
    elif "Craft a" in lore:
        method = "CRAFT"
        strategy = "WIP"

    elif lore == "Community Goal!":
        method = "COMMUNITY GOAL"
        strategy = "I'm not sure! The Hypixel API doesn't provide lore for Community Goals..."
        eta = "---"

    else:
        method = "MISCELLANEOUS"

        # IF KILLING A MOB
        if "kill" in id and "skill" not in id:
            mob = search_term(id.replace('kill_', ''))
            strategy = find_text(mob, "Location")

        # IF WEARING SOMETHING
        elif "unique_armor" in id:
            strategy = "armor_list"
            #strategy = f"Obtain {requiredAmount} of these: \n"
            #for armor in armor_list:
            #    strategy += f"- {armor}\n"
        elif "accessories" in id:
            strategy = "accessory_list"
            #strategy = f"Obtain {requiredAmount} of these: \n"
            #for accessory in accessory_list:
            #    strategy += f"- {accessory}\n"

        # IF OBTAINING SOMETHING
        elif "obtain_item" in id:
            item = item.replace('Obtain an ', '')
            item = lore.replace('Obtain a ', '')
            item = item.replace(' ', '_')
            item = item.replace('.', '')
            strategy = str(find_text(item, "Obtaining"))
        
        elif "obtain_pets" in id:
            strategy = "pet_list"
            #strategy = f"Obtain {requiredAmount} of these: \n"
            #for pet in pet_list:
            #    strategy += f"- {pet}\n"
        elif "obtain_t1" in id:
            number = ""
            for char in lore:
                if char.isnumeric():
                    number = number + char
            if number == "11":
                strategy = "Upgrade a Wheat Minion to Tier 11. Use the hub to farm wheat."
            elif number == "12":
                strategy = "Upgrade a Wheat Minion to Tier 12. Use the hub to farm wheat, and upgrade to Tier 12 using Tony's Shop in the Mushroom Desert."
        
        # Edge cases :( - no (useful) wiki page...
        elif "obtain_ultimate_enchanted_book" in id:
            strategy = "Play Floor 1 of Dungeons. You'll likely get Bank I from the Free Chest."
        
        elif "Esteemed Enchanter" == name:
            strategy = "Play Floor 1 of Dungeons. You'll likely get Feather Falling VI or Infinite Quiver VI from the Free Chest."

        # IF STAT TASK
        elif "stat" in id:
            if "health" in id:
                strategy = stat_strat(100, requiredAmount, health_steps)
            elif "sea_creature_chance" in id:
                strategy = stat_strat(20, requiredAmount, scc_steps)
            elif "strength" in id:
                strategy = stat_strat(0, requiredAmount, strength_steps)
            elif "ferocity" in id:
                strategy = stat_strat(0, requiredAmount, ferocity_steps)
            elif "critical_damage" in id:
                strategy = stat_strat(50, requiredAmount, crit_damage_steps)
            elif "critical_chance" in id:
                strategy = stat_strat(30, requiredAmount, crit_chance_steps)
            elif "speed" in id:
                strategy = stat_strat(100, requiredAmount, speed_steps)
            else:
                strategy = "Oops I didn't plan for this"
            
        # IF SKILL TASK
        elif "get_skill" in id:
            skill = id.replace("get_skill_", "")
            skill = list(skill)
            for count, char in enumerate(skill): 
                if not char.isalpha():
                    skill[count] = ""
            skill = ("".join(skill)).strip()
            skill = skill.title()
            strategy = get_skill_info(skill)
                    
        # IF REFORGE TASK
        elif "reforge" in id:
            reforge = (id.replace("reforge_", "")).title()
            strategy = attempt_search(reforge)
            if strategy == "I sure hope this task is self-explanatory because I didn't program for this to happen":
                strategy = f"Basic reforges (like {reforge}) can be applied to an item at the Blacksmith."

        # IF BANK TASK
        elif "bank" in id:
            strategy = stat_strat(0, requiredAmount, money_steps)

        # IF DUNGEON CHEST TASK
        elif "dungeon_chest" in id:
            tier = id.replace("unlock_dungeon_chest_", "")
            try:
                for chest in dchest_prices:
                    if chest[0] == tier:
                        amount = chest[1]
                strategy = f"Play Floor 1. A {tier} chest costs {amount} coins."
            except:
                strategy = "Error..."

        # IF SKILL AVERAGE
        elif "skill_average" in id:
            strategy = "Play the game. If neccessary, Farming tends to be the easiest skill to level up."

        # IF POTION
        elif "brew_potion" in id:
            if requiredAmount == 4:
                strategy = "Speed IV: Enchanted Sugar + Glowstone Dust"
            if requiredAmount == 6:
                strategy = "Speed VI: Enchanted Sugar + Enchanted Redstone Lamp"

        # IF MINION COLLECTION
        elif "craft_minions" in id:
            strategy = find_next_minions(requiredAmount, unique_minions)
        
        # IF SLAYER LEVEL
        elif "slayer_level" in id:
            strategy = "Level up Spider Slayer."


        # IF NOTHING ELSE
        else:
            key_words = []
            key_words = find_key_words(dict["lore"])
            strategy = attempt_search(key_words)
                
    db.execute("INSERT INTO bingo VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", id, name, lore, requiredAmount, method, eta, unloads, minion, strategy)



@app.route("/")
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/bingo", methods=["POST"])
def bingo():
    error=""
    ign = (request.form.get("ign")).strip()
    # Get UUID from Mojang API
    try:
        response = (requests.get(f"https://api.mojang.com/users/profiles/minecraft/{ign}")).json()
        ign = response['name']
        uuid = response['id']
        profile_data = []
        profile_id = ""
    except:
        error = "Not a username!"
    else:
        # If valid username, check Bingo Stats
        # Completed Bingo Tasks:
        response = (requests.get(f"https://api.hypixel.net/skyblock/bingo?key={key}&uuid={uuid}")).json()
        try:
            if response["cause"] == "Key throttle" or response["cause"] == "Invalid API key":
                error = "Something's wrong with my API key?!?!?"
            else:
                error = "Can't find BINGO data!"
        except:
            # Completed Tasks of Latest Bingo Event
            # Find correct bingo with key (must be equal to bingo_id)

            latest = (response["events"][(len(response["events"]) - 1)])["key"]
            if latest == bingo_id:
                completed_tasks = (response["events"][(len(response["events"]) - 1)])["completed_goals"]
                for count, task in enumerate(completed_tasks):
                    completed_tasks[count] = task.lower()
                print(completed_tasks)

                # Profile data for personalized stuff
                response = (requests.get(f"https://api.hypixel.net/skyblock/profiles?key={key}&uuid={uuid}")).json()
                for profile in response["profiles"]:
                    try:
                        if profile["game_mode"] == "bingo":
                            profile_data = profile
                            profile_id = profile_data["profile_id"]
                    except:
                        continue
    
                
            else:
                completed_tasks = []

            bingo_tasks = db.execute("SELECT * FROM bingo")
            # Adds personalized completion data, keeps proper order of tasks - used for bingo board
            ordered_tasks = completion(ign, uuid, profile_data, profile_id, bingo_tasks, completed_tasks, latest, bingo_id, armor_list, accessory_list, pet_list)
            # Calculates and sorts by ETA - used for list of tasks
            eta_tasks = sortbyeta(ordered_tasks)

            return render_template('bingo.html', eta_tasks=eta_tasks, ordered_tasks=ordered_tasks, ign=ign, armor_list=armor_list, pet_list=pet_list, accessory_list=accessory_list)
    return redirect("/")
    

# TODO: bingo_tasks: Send list of dictionaries, each a task containing keys: name, lore (?), method, eta, completion (percentage)

# TODO: Query per user, add percentage bars (?) for each task, https://api.hypixel.net/skyblock/bingo?key=5a0827f1-cf40-4ea6-9891-5a5a323b5f35&uuid=5e22209b-e586-4a08-8761-aa6bde56a090
# TODO: Make tasks change color based on completion % (?) - g l o w
# TODO: Add interactable to-do list
