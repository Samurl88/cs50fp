import os
import requests
import numpy

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

armor_list = ['Leather Armor', 'Golden Armor', 'Chainmail Armor', 'Iron Armor', 'Diamond Armor', 'Farm Suit', 'Mushroom Armor', 'Pumpkin Armor', 'Cactus Armor', 'Leaflet Armor', 'Miner Armor', 'Lapis Armor', 'Angler Armor', "Rosetta's Armor", 'Squire Armor', 'Celeste Armor', 'Mercenary Armor', 'Starlight Armor']
accessory_list = ['Zombie Talisman', 'Skeleton Talisman', 'Village Affinity Talisman', 'Mine Affinity Talisman', 'Intimidation Talisman', 'Scavenger Talisman', 'Wolf Paw', "Pig's Foot", "Melody's Hair", 'Shiny Yellow Rock', 'Campfire Initiate Badge', 'Cat Talisman', 'King Talisman', 'Red Claw Talisman', 'Spider Talisman', 'Vaccine Talisman', 'Farming Talisman', 'Talisman of Coins', 'Magnetic Talisman', 'Gravity Talisman', 'Speed Talisman', 'Potion Affinity Talisman']
health_steps = [("Growth V", 900), ("Titanic", 120)]
scc_steps = [("Sea Emperor Century Cake", 1), ("Angler V", 5), ("Beacon V", 5), ("Angler Armor", 4)]
strength_steps = [("Strength VIII Potion", 75)]

# Loads data into database
db = SQL("sqlite:///bingo.db")

# TODO: ALTER DATABASE WHEN NECESSARY
db.execute("DELETE FROM bingo")
for dict in response["goals"]:
    unloads = ""
    eta = 0
    minion = ""
    strategy = ""

    id = dict["id"]
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

    # TODO: Craft Goal, determine if worth minion, and how much minion.
    # TODO: For crafting: take into account 
    # Couldn't do "craft" in id b/c craft_minions is a goal but it's crafting 40 unique minions
    elif "Craft a" in lore:
        method = "CRAFT"

    elif lore == "Community Goal!":
        method = "COMMUNITY GOAL"

    else:
        method = "MISCELLANEOUS"

        # IF KILLING A MOB
        if "kill" in id:
            mob = search_term(id.replace('kill_', ''))
            strategy = find_text(mob, "Location")

        # IF WEARING SOMETHING
        elif "wear" in id:
            if "unique_armor" in id:
                strategy = f"Obtain {requiredAmount} of these armors: "
                for armor in armor_list:
                    strategy += f"{armor}\n"
            elif "accessories" in id:
                strategy = f"Obtain {requiredAmount} of these acessories: "
                for accessory in accessory_list:
                    strategy += f"{accessory}\n"

        # IF OBTAINING SOMETHING
        elif "obtain" in id:
            if "obtain_item" in id:
                item = item.replace('Obtain an ', '')
                item = lore.replace('Obtain a ', '')
                item = item.replace(' ', '_')
                item = item.replace('.', '')
                print(item)
                strategy = str(find_text(item, "Obtaining"))

        # IF STAT TASK
        elif "stat" in id:
            strategy = ""
            i = 0
            if "health" in id:
                health = 265 #(Base Health + Mushroom Armor)
                strategy += "Mushroom Armor\n"
                while health < requiredAmount:
                    try:
                        strategy += health_steps[i][0]
                        health += health_steps[i][1]
                        i += 1
                    except:
                        # TODO: Add fairy soul suppport?
                        break
                
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
            else:
                completed_tasks = []

            bingo_tasks = db.execute("SELECT * FROM bingo")
            # Adds completion %, keeps proper order of tasks - used for bingo board
            ordered_tasks = completion(bingo_tasks, completed_tasks, latest, bingo_id)
            # Calculates and sorts by ETA - used for list of tasks
            eta_tasks = sortbyeta(ordered_tasks)

            return render_template('bingo.html', eta_tasks=eta_tasks, ordered_tasks=ordered_tasks, ign=ign)
    return redirect("/")
    

# TODO: bingo_tasks: Send list of dictionaries, each a task containing keys: name, lore (?), method, eta, completion (percentage)

# TODO: Query per user, add percentage bars (?) for each task, https://api.hypixel.net/skyblock/bingo?key=5a0827f1-cf40-4ea6-9891-5a5a323b5f35&uuid=5e22209b-e586-4a08-8761-aa6bde56a090
# TODO: Make tasks change color based on completion % (?) - g l o w
# TODO: Add interactable to-do list
