from bs4 import BeautifulSoup
import requests
import re
import math
import time
import numpy

def color(lore):
    lore = lore.replace("§1", "")
    lore = lore.replace("§2", "")
    lore = lore.replace("§3", "")
    lore = lore.replace("§4", "")
    lore = lore.replace("§5", "")
    lore = lore.replace("§6", "")
    lore = lore.replace("§7", "")
    lore = lore.replace("§9", "")
    lore = lore.replace("§0", "")
    lore = lore.replace("§a", "")
    lore = lore.replace("§b", "")
    lore = lore.replace("§c", "")
    lore = lore.replace("§d", "")
    lore = lore.replace("§e", "")
    lore = lore.replace("§f", "")
    return lore

def search_term(query):
    query = query.replace(" ", "_")
    query = list(query)
    for count, char in enumerate(query):
        if char == '_':
            query[count + 1] = query[count + 1].upper()
        if char.isnumeric():
            query[count] = ''
    query = ''.join(query)
    return(query)

def find_text(thing, word):
    para = ""
    r = requests.get(f'https://wiki.hypixel.net/index.php?title={thing}&redirect=yes')
    soup = BeautifulSoup(r.content, 'html.parser')
    for header in soup.find_all(id=word):
        para = header.find_next('p').get_text()
    return(str(para).strip())

# Gets required steps for task.
def stat_strat(steps, required_amount):
    steps_req = []
    stat_count = 0
    i = 0
    while stat_count < required_amount:
        try:
            tmpdict = {}
            tmpdict["name"] = f"{steps[i][0]} → {steps[i][1]}"
            if "Base" in tmpdict["name"]:
                tmpdict["has"] = "true"
            else:
                tmpdict["has"] = "false"
            stat_count += steps[i][1]
            i += 1
            steps_req.append(tmpdict)
        except:
            break
    return(steps_req)

def get_skill_info(skill):
    para = ""
    r = requests.get(f'https://wiki.hypixel.net/index.php?title={skill}&redirect=yes')
    soup = BeautifulSoup(r.content, 'html.parser')
    if not soup.find_all(id=f"{skill}_XP_Gain"):
        for header in soup.find_all(id=f"Levelling"):
            para = header.find_next('p').get_text()
            return(str(para).strip())
    for header in soup.find_all(id=f"{skill}_XP_Gain"):
        para = header.find_next('p').get_text()
    return(str(para).strip())

def find_next_minions(requiredAmount, minion_list):
    #15, 25, 40, 60, 100
    return(str(minion_list))

def find_key_words(lore):
    # Remove useless coloring and periods
    lore = (lore).replace(".", "")
    lore = (lore).replace("§7", "", 1)
    lore = list(lore)

    # Removes character following § (so §8 -> §)
    for count,char in enumerate(lore):
        if char == '§':
            lore[count + 1] = ""
    lore = "".join(lore)

    key_words = []
    read = False
    key = []

    # Get key words
    for count, char in enumerate(lore):
        if read:
            if char == "§":
                key = ("".join(key)).strip()
                key_words.append(key)
                read = False
                key = []
            else:
                key.append(char)
        if char == "§":
            read = True
        if count == len(lore) - 1:
            if key:
                key = ("".join(key)).strip()
                key_words.append(key)

    # Filter useless key words
    for count, word in enumerate(key_words):
        # Important numbers already in requiredAmount
        # Remove starting numbers
        replacement = re.sub(r'[0-9]', '', word)
        replacement = re.sub(r'[^\w]', ' ', replacement)
        #print(replacement)
        if replacement != word:
            key_words[count] = replacement

        if key_words[count] == '':
            key_words.remove('')
    #print(key_words)
    return(key_words)

def attempt_search(key_words):
    for phrase in key_words:
        phrase = search_term(phrase)
        para = ""
        r = requests.get(f'https://wiki.hypixel.net/index.php?title={phrase}&redirect=yes')
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')

            # If not Obtaining, try first para of page
            if not soup.find_all(id="Obtaining"):
                for para in soup.find_all('p'):
                    text = para.get_text()
                    if text != "\n" and text != "Content\n":
                        return(text.strip(), phrase)

            # Try Obtaining
            for header in soup.find_all(id='Obtaining'):
                para = str(header.find_next('p').get_text())
                return(para.strip(), phrase)

    return("I sure hope this task is self-explanatory because I didn't program for this to happen", "ERROR")

    

#[{'name': 'Skilled', 'lore': '', 'method': '', 'eta': 0}, {'name': 'Diamond Collector', 'lore': '§7Reach §a5,000 §7Diamond Collection.', 'method': 'MINION', 'eta': 15}

# Returns a string from a long number (ex. 390000 -> 390K)
def shorten_number(number):
    try:
        number = int(number)
        if number >= 1000000000:
            number_string = str(round((number / 1000000000), 1)) + "B"
        elif number >= 1000000:
            number_string = str(round((number / 1000000), 1)) + "M"
        elif number >= 1000:
            number_string = str(round((number / 1000), 1)) + "K"
        else:
            number_string = number
        return(number_string)
    except:
        return(0)



# TODO: Add completion % for each task
def completion(ign, uuid, profile_data, profile_id, tasks, completed_tasks, latest, bingo_id, armor_list, accessory_list, pet_list, minion_info, health_steps_req, scc_steps_req, strength_steps_req, ferocity_steps_req, crit_damage_steps_req, crit_chance_steps_req, speed_steps_req, unique_minions, money_steps_req):
# TODO: Personalized Completion Data Here
    try: # In case API's down
        load_shiiyu_page = requests.get(f"https://sky.shiiyu.moe/stats/{uuid}/{profile_id}") #API doesn't update otherwise...
        shiiyu_data = requests.get(f"https://sky.shiiyu.moe/api/v2/profile/{ign}").json() #NOTE: THIS IS SO SLOW!!!
        talisman_data = requests.get(f"https://sky.shiiyu.moe/api/v2/talismans/{ign}").json()
        sloth_data = requests.get("https://api.slothpixel.me/api/skyblock/profile/logicalresponse/kiwi").json()
    except:
        shiiyu_data = []
        talisman_data = []

    def cake_check(key):
        current_time = time.time() * 1000
        try:
            cake_buffs = profile_data["members"][uuid]["temp_stat_buffs"]
            for buff in cake_buffs:
                if buff["key"] == key:
                    if buff["expire_at"] > current_time:
                        step["has"] = "true"
                        return("true")
                    else:
                        return("false")
            return("false")
        except:
            return("false")

    def reforge_check(items, reforge, rarity=[""], count=1):
        c = 0 
        try:
            for item in items:
                try:
                    if item["extra"]["reforge"] == reforge and item["rarity"] not in rarity:
                        c += 1
                        if c == count:
                            return("true")
                except:
                    c += 0
            return("false")
        except:
            return("false")

    def enchant_check(items, enchantment, level, count=1):
        c = 0
        try:
            for item in items:
                try:
                    if item["tag"]["ExtraAttributes"]["enchantments"][enchantment] >= level:
                        c += 1
                        if c == count:
                            return("true")
                except:
                    c += 0
            return("false")
        except:
            return("false")

    def effect_check(potion, level):
        try:
            effects = profile_data["members"][uuid]["active_effects"]
            for effect in effects:
                if effect["effect"] == potion:
                    if int(effect["level"]) == level:
                        return("true")
                    else:
                        return("false")
            return("false")
        except:
            return("false")

    def item_check(item):
        try:
            items = shiiyu_data["profiles"][profile_id]["items"]
            if item in str(items):
                return("true")
            else:
                return("false")
        except:
            return("false") 
        """
            NOTE: not sure if above is inefficient. If so, here's what would go instead:
            weapons = shiiyu_data["profiles"][profile_id]["items"]["weapons"]
            for weapon in weapons:
                if item in weapon["display_name"]:
        """



    for task in tasks:
        task["has_list"] = "false"
        if task["method"] == "MINION":
            required_amount = task["required_amount"]
            item = (task["id"].replace("collection_", "")).upper()
            try:
                collection = profile_data["members"][uuid]["collection"]
                try:
                    progress = collection[item]
                    task["eta"] = f"{shorten_number(progress)} / {shorten_number(required_amount)}"
                    task["percent_complete"] = round(((progress / required_amount) * 100), 1)
                except:
                    progress = 0
                    task["eta"] = f"0 / {shorten_number(required_amount)}"
                    task["percent_complete"] = 0.0
            except:
                task["eta"] = "Turn on Collection API!"
                task["percent_complete"] = 0.0

            if minion_info[item] != "none":
                try:
                    required_amount -= progress
                    if required_amount > 0:
                        timePerItem = ((minion_info[item][0]["delay"]) * 2) / 3600
                        storage = (minion_info[item][0]["storage"]) + 576 # Medium Storages (TODO: Calculate if user has more minion slots, use small storages)
                        # Find time (in HOURS) WITH 5 MINIONS to get collection
                        eta = round((required_amount * timePerItem) / 5)
                        unloads = int(numpy.ceil(eta / (timePerItem * storage)))

                        task["minion_hours_left"] = eta
                        task["unloads"] = unloads
                    else:
                        task["minion_hours_left"] = "--"
                        task["unloads"] = "--"
                except:
                    task["minion_hours_left"] = "--"
                    task["unloads"] = "--"
            else:
                task["minion_hours_left"] = "none"
                task["unloads"] = "none"
                
        elif task["method"] == "COMMUNITY GOAL":
            task["eta"] = "---"
            task["percent_complete"] = 100
            
        elif "fairy_souls" in task["id"]:
            try:
                required_amount = task["required_amount"]
                progress = profile_data["members"][uuid]["fairy_souls_collected"]
            except:
                progress = 0
            task["eta"] = f"{str(progress)} / {str(required_amount)}"
            task["percent_complete"] = round(((progress / required_amount) * 100), 1)
        
        elif "pets" in task["id"]:
            task["has_list"] = "true"
            progress_pets = []
            try:
                required_amount = task["required_amount"]
                pets = profile_data["members"][uuid]["pets"]
                progress = len(pets)

                for pet in pets:
                    progress_pets.append(pet["type"])

            except:
                progress = 0
            task["eta"] = f"{str(progress)} / {str(required_amount)}"
            task["percent_complete"] = round(((progress / required_amount) * 100), 1)

            task["completion_list"] = []
            for pet in pet_list:
                tmpdict = {}
                tmpdict["name"] = pet
                if pet.replace(" ", "_").upper() in progress_pets:
                    tmpdict["has"] = "true"
                else:
                    tmpdict["has"] = "false"
                task["completion_list"].append(tmpdict)

        elif "accessories" in task["id"]:
            task["has_list"] = "true"
            progress_accessories = []
            required_amount = task["required_amount"]
            try:
                accessories = talisman_data["profiles"][profile_id]["accessories"]
                progress = len(accessories)

                for accessory in accessories:
                    progress_accessories.append(accessory["display_name"])
            except:
                progress = 0
            # Get list of accessories that player has

            task["eta"] = f"{str(progress)} / {str(required_amount)}"
            task["percent_complete"] = round(((progress / required_amount) * 100), 1)

            # Compare player's accessories to full list; create dict showing whether has or doesn't have
            task["completion_list"] = []
            for accessory in accessory_list:
                tmpdict = {}
                tmpdict["name"] = accessory
                if accessory in progress_accessories:
                    tmpdict["has"] = "true"
                else:
                    tmpdict["has"] = "false"
                task["completion_list"].append(tmpdict)
            
        elif "relic" in task["id"]:
            try:
                required_amount = task["required_amount"]
                progress = profile_data["members"][uuid]["objectives"]["find_relics"]["progress"]
            except:
                progress = 0
            task["eta"] = f"{str(progress)} / {str(required_amount)}"
            task["percent_complete"] = round(((progress / required_amount) * 100), 1)
        
        elif "get_skill" in task["id"]:
            skill = list(task["id"].replace("get_skill_", ""))
            for count, char in enumerate(skill): 
                if not char.isalpha():
                    skill[count] = ""
            skill = ("".join(skill)).strip()
            required_amount = int((re.sub('[^0-9]','', task["id"])).strip())
            try:
                progress = shiiyu_data["profiles"][profile_id]["data"]["levels"][skill]["level"]
                print(progress)
            except:
                progress = 0
            task["eta"] = f"{str(progress)} / {str(required_amount)}"
            task["percent_complete"] = round(((progress / required_amount) * 100), 1)
        
        # NOTE: Only checks equipped armor and armor stored in wardrobe
        elif "armor" in task["id"]:
            task["has_list"] = "true"
            required_amount = task["required_amount"]
            armor_count = 0
            progress_armors = []
            # Armor currently equipped
            try:
                equipped_armor = shiiyu_data["profiles"][profile_id]["items"]["armor"]
                armor_check = equipped_armor[0]["tag"]["ExtraAttributes"]["id"].split('_')[0]
                c = 0 # I don't know how to do this better
                for piece in equipped_armor:
                    if armor_check in piece["tag"]["ExtraAttributes"]["id"]:
                        c += 1
                if c == 4:
                    armor_count += 1
                    armor_check = armor_check.split(' ')[0].upper()
                    progress_armors.append(armor_check)

            except:
                armor_count += 0
            
            # Armor stored in wardrobe
            try:
                wardrobe = shiiyu_data["profiles"][profile_id]["items"]["wardrobe"]
                for armor_set in wardrobe:
                    armor_check = armor_set[0]["tag"]["ExtraAttributes"]["id"].split('_')[0] # Gets id to compare to other armor pieces
                    c = 0
                    for piece in armor_set:
                        try:
                            if armor_check in piece["tag"]["ExtraAttributes"]["id"]:
                                c += 1
                        except:
                            break
                    if c == 4:
                        armor_count += 1
                        progress_armors.append(armor_check)
            except:
                armor_count += 0

            task["eta"] = f"{str(armor_count)} / {str(required_amount)}"
            task["percent_complete"] = round(((armor_count / required_amount) * 100), 1)

            armor_completion = []
            for armor in armor_list:
                tmpdict = {}
                tmpdict["name"] = armor["name"]

                armor_check = armor["id"]
                if armor_check in progress_armors:
                    tmpdict["has"] = "true"
                else:
                    tmpdict["has"] = "false"
                armor_completion.append(tmpdict)
                
            task["completion_list"] = armor_completion

        elif "bank" in task["id"]:
            task["has_list"] = "true"
            required_amount = task["required_amount"]
            try:
                str_required_amount = shorten_number(required_amount)
                coins = round(profile_data["banking"]["balance"])
                str_coins = shorten_number(coins)

                task["eta"] = f"{str_coins} / {str_required_amount}"
                task["percent_complete"] = round(((coins / required_amount) * 100), 1)
            except:
                task["eta"] = "Turn on Banking API!"
                task["percent_complete"] = 0.0

            for step in money_steps_req:
                try:
                    if "Spider" in step["name"]:
                        if profile_data["members"][uuid]["objectives"]["find_relics"]["progress"] == 28:
                            step["has"] == "true"
                except:
                    step["has"] = "false"
            task["completion_list"] = money_steps_req

        elif "powder_mithril" in task["id"]:
            required_amount = task["required_amount"]
            str_required_amount = shorten_number(required_amount)
            try:
                progress = shiiyu_data["profiles"][profile_id]["data"]["mining"]["core"]["powder"]["mithril"]["total"]
                str_progress = shorten_number(progress)
            except:
                progress = 0
                str_progress = 0
            task["eta"] = f"{str_progress} / {str_required_amount}"
            task["percent_complete"] = round(((progress / required_amount) * 100), 1)

        elif "powder_gemstone" in task["id"]:
            required_amount = task["required_amount"]
            str_required_amount = shorten_number(required_amount)
            try:
                progress = shiiyu_data["profiles"][profile_id]["data"]["mining"]["core"]["powder"]["gemstone"]["total"]
                str_progress = shorten_number(progress)
            except:
                progress = 0
                str_progress = 0
            task["eta"] = f"{str_progress} / {str_required_amount}"
            task["percent_complete"] = round(((progress / required_amount) * 100), 1)
        
        elif "unique_collections" in task["id"]:
            required_amount = task["required_amount"]
            try:
                progress = len(profile_data["members"][uuid]["collection"])
                task["eta"] = f"{str(progress)} / {str(required_amount)}"
            except:
                progress = 0
                task["eta"] = "Turn on Collection API!"
            task["percent_complete"] = round(((progress / required_amount) * 100), 1)

        elif "slayer_level" in task["id"]:
            task["unit"] = "XP"
            required_amount = task["required_amount"]
            xp_list = {0:1, 1:5, 2:25, 3:200, 4:1000, 5:5000, 6:20000, 7:100000, 8:400000, 9:1000000}
            xp_needed = xp_list[required_amount]
            try:
                # NOTE: possibly add code to determine highest slayer level and go off of that...
                slayers = profile_data["members"][uuid]["slayer_bosses"]
                progress = slayers["spider"]["xp"]
            except:
                progress = 0
            task["eta"] = f"{shorten_number(progress)} / {shorten_number(xp_needed)}"
            task["percent_complete"] = round(((progress / xp_needed) * 100), 1)
        
        elif "craft_minions" in task["id"]:
            required_amount = task["required_amount"]
            try:
                progress = len(profile_data["members"][uuid]["crafted_generators"])
            except:
                progress = 0
            task["eta"] = f"{progress} / {required_amount}"
            task["percent_complete"] = round(((progress / required_amount) * 100), 1)

            task["has_list"] = "true"
            task["completion_list"] = []
            try:
                generator_data = profile_data["members"][uuid]["crafted_generators"]
                t = 0
                for minion in unique_minions:
                    c = 0
                    for generator in generator_data:
                        if re.sub(r'[0-9]', '', generator).replace("_", "") == minion.replace(" ", "_").upper():
                            c += 1
                            t += 1
                    tmpdict = {"name":f"{minion} → {c}"}
                    if c >= 5:
                        tmpdict["has"] = "true"
                    elif c >= 1:
                        tmpdict["has"] = "maybe"
                    else:
                        tmpdict["has"] = "false"
                    task["completion_list"].append(tmpdict)
                task["completion_list"].insert(0, {"name": f"Other → {len(generator_data) - t}", "has": "true"})
            except:
                for minion in unique_minions:
                    tmpdict = {"name":f"{minion} → 0", "has": "false"}
                    task["completion_list"].append(tmpdict)

        elif "stat" in task["id"]:
            task["has_list"] = "true"
            required_amount = task["required_amount"]
            task_stat = task["id"].replace("stat_", "")
            if task_stat == "critical_damage":
                task_stat = "crit_damage"
            elif task_stat == "critical_chance":
                task_stat = "crit_chance"
            try:
                # Shiiyu API updated... now you need to manually calculate stats :(
                # Base Stat
                progress = sloth_data["members"][uuid]["attributes"][task_stat]

                # Pet
                for pet in shiiyu_data["profiles"][profile_id]["data"]["pets"]:
                    if pet["active"] == True:
                        try:
                            pet_stat = pet["stats"][task_stat]
                            progress += round(pet_stat)
                            break
                        except:
                            break

                task["eta"] = f"{str(progress)} / {str(required_amount)}"
                task["percent_complete"] = round(((progress / required_amount) * 100), 1)

            except:
                task["eta"] = "API Error"
                task["percent_complete"] = 0.0
                task["completion_list"] = [{'step': "Error :(", "has":"false"}]
            
            # For List Explanation in Taskbox
            if task_stat == "health":
                for step in health_steps_req:
                    try:
                        # Checking for growth v and titanic reforge, too!
                        if "Mushroom Armor" in step["name"]:
                            growth_v = "false"
                            titanic = "false"
                            try:
                                # First check equipped armor
                                equipped_armor = shiiyu_data["profiles"][profile_id]["items"]["armor"]

                                # Attempt to save time if player doesn't have set
                                if "MUSHROOM" in progress_armors:
                                    # Check for Mushroom Armor in equipped armor
                                    c = 0
                                    for piece in equipped_armor:
                                        try:
                                            if "MUSHROOM" in piece["tag"]["ExtraAttributes"]["id"]:
                                                c += 1
                                        except:
                                            break
                                    if c == 4: # that's a set, check growth enchant and titanic reforge with this set!
                                        step["has"] = "true"
                                        growth_v = enchant_check(equipped_armor, "growth", 5, 4)
                                        titanic = reforge_check(equipped_armor, "titanic", ["common"], 4)
                                    else:
                                        # If not equipped, try armor stored in wardrobe
                                        try:
                                            wardrobe = shiiyu_data["profiles"][profile_id]["items"]["wardrobe"]
                                            for armor_set in wardrobe:
                                                c = 0
                                                for piece in armor_set:
                                                    try:
                                                        if "MUSHROOM" in piece["tag"]["ExtraAttributes"]["id"]:
                                                            c += 1
                                                    except:
                                                        break
                                                if c == 4:
                                                    step["has"] = "true"
                                                    growth_v = enchant_check(equipped_armor, "growth", 5, 4)
                                                    titanic = reforge_check(equipped_armor, "titanic", ["common"], 4)
                                        except:
                                            step["has"] = "false"
                                            growth_v = "false"
                                            titanic = "false"
                            except:
                                step["has"] = "false"
                                growth_v = "false"
                                titanic = "false"
                                
                        elif "Growth V" in step["name"]:
                            if growth_v == "true":
                                step["has"] = "true"
                        
                        elif "Titanic" in step["name"]:
                            if titanic == "true":
                                step["has"] = "true"

                        elif "Century Cake" in step["name"]:
                            step["has"] = cake_check("cake_health")
                        
                    except:
                        step["has"] = "false"
                task["completion_list"] = health_steps_req

            elif task_stat == "sea_creature_chance":
                for step in scc_steps_req:
                    try:
                        if "Angler V" in step["name"]:
                            fishing_tools = shiiyu_data["profiles"][profile_id]["items"]["fishing_tools"]
                            step["has"] = enchant_check(fishing_tools, "angler", 5)

                        elif "Beacon V" in step["name"]:
                            step["has"] = "maybe"

                        elif "Angler Armor" in step["name"]:
                            if "ANGLER" in progress_armors:
                                step["has"] = "true"

                        elif "Century Cake" in step["name"]:
                            step["has"] = cake_check("cake_sea_creature_chance")
                    except:
                        step["has"] = "false"
                task["completion_list"] = scc_steps_req

            elif task_stat == "strength":
                for step in strength_steps_req:
                    try:
                        if "Bingo Pet" in step["name"]:
                            pets = shiiyu_data["profiles"][profile_id]["data"]["pets"]
                            for pet in pets:
                                if pet["type"] == "BINGO":
                                    if int(pet["level"]["level"]) >= 50: 
                                        step["has"] = "true"
                                    break

                        elif "Strength VIII" in step["name"]:
                            step["has"] = effect_check("strength", 8)

                        elif "Overflux" in step["name"]:
                            step["has"] = "maybe"

                        elif "Raider Axe" in step["name"]:
                            step["has"] = item_check("Raider Axe")

                        elif "Fierce" in step["name"]:
                            # First check equipped armor
                            equipped_armor = shiiyu_data["profiles"][profile_id]["items"]["armor"]
                            step["has"] = reforge_check(equipped_armor, "fierce", ["common", "uncommon"], 4)
                            if step["has"] == "false":
                                # Then check armor in wardrobe
                                try:
                                    wardrobe = shiiyu_data["profiles"][profile_id]["items"]["wardrobe"]
                                    for armor_set in wardrobe:
                                        step["has"] = reforge_check(armor_set, "fierce", ["common", "uncommon"], 4)
                                except:
                                    step["has"] = "false"

                    except:
                        step["has"] = "false"
                task["completion_list"] = strength_steps_req
                            
            elif task_stat == "ferocity":
                for step in ferocity_steps_req:
                    try:    
                        if "Dirty" in step["name"]:
                            weapons = shiiyu_data["profiles"][profile_id]["items"]["weapons"]
                            step["has"] = reforge_check(weapons, "dirty", ["common"])

                        elif "Century Cake" in step["name"]:
                            step["has"] = cake_check("cake_ferocity")
                    except:
                        step["has"] = "false"
                task["completion_list"] = ferocity_steps_req

            elif task_stat == "crit_damage":
                for step in crit_damage_steps_req:
                    try:
                        if "Critical V (Enchantment)" in step["name"]:
                            weapons = shiiyu_data["profiles"][profile_id]["items"]["weapons"]
                            step["has"] = enchant_check(weapons, "critical", 5)

                        elif "Spicy" in step["name"]:
                            weapons = shiiyu_data["profiles"][profile_id]["items"]["weapons"]
                            step["has"] = reforge_check(weapons, "spicy", ["common", "uncommon"])
                        
                        elif "Fierce" in step["name"]:
                            # First check equipped armor
                            equipped_armor = shiiyu_data["profiles"][profile_id]["items"]["armor"]
                            step["has"] = reforge_check(equipped_armor, "fierce", ["common", "uncommon"], 4)
                            if step["has"] == "false":
                                # Then check armor in wardrobe
                                try:
                                    wardrobe = shiiyu_data["profiles"][profile_id]["items"]["wardrobe"]
                                    for armor_set in wardrobe:
                                        step["has"] = reforge_check(armor_set, "fierce", ["common", "uncommon"], 4)
                                except:
                                    step["has"] = "false"

                        elif "Critical IV" in step["name"]:
                            step["has"] = effect_check("critical", 4)
                        
                        elif "Beacon V" in step["name"]:
                            step["has"] = "maybe"

                    except:
                        step["has"] = "false"
                task["completion_list"] = crit_damage_steps_req
                
            elif task_stat == "crit_chance":
                for step in crit_chance_steps_req:
                    try:
                        if "Odd" in step["name"]:
                            weapons = shiiyu_data["profiles"][profile_id]["items"]["weapons"]
                            step["has"] = reforge_check(weapons, "odd", ["common", "uncommon"])
                        
                        elif "Clean" in step["name"]:
                            # First check equipped armor
                            equipped_armor = shiiyu_data["profiles"][profile_id]["items"]["armor"]
                            step["has"] = reforge_check(equipped_armor, "clean", ["common", "uncommon"], 4)
                            if step["has"] == "false":
                                # Then check armor in wardrobe
                                try:
                                    wardrobe = shiiyu_data["profiles"][profile_id]["items"]["wardrobe"]
                                    for armor_set in wardrobe:
                                        step["has"] = reforge_check(armor_set, "clean", ["common", "uncommon"], 4)
                                except:
                                    step["has"] = "false"

                        elif "Critical IV Potion" in step["name"]:
                            step["has"] = effect_check("critical", 4)
                        
                        elif "Beacon V" in step["name"]:
                            step["has"] = "maybe"
                        
                        elif "Fortuitous" in step["name"]:
                            if profile_data["members"][uuid]["accessory_bag_storage"]["selected_power"] == "fortuitous":
                                step["has"] = "true"

                    except:
                        step["has"] = "false"
                task["completion_list"] = crit_chance_steps_req

            elif task_stat == "speed":
                for step in speed_steps_req:
                    try:
                        if "Godsplash" in step["name"]:
                            rabbit = effect_check("rabbit", 6)
                            agility = effect_check("agility", 4)
                            spirit = effect_check("spirit", 4)
                            speed = effect_check("speed", 8)
                            adrenaline = effect_check("adrenaline", 8)
                            if rabbit == "true" and agility == "true" and spirit == "true" and speed == "true" and adrenaline == "true":
                                step["has"] = "true"

                        elif "Farm Suit" in step["name"]:
                            if "FARM" in progress_armors:
                                step["has"] = "true"
                        
                        elif "Rogue Sword" in step["name"]:
                            step["has"] = item_check("Rogue Sword")
                        
                        elif "Hunter Knife" in step["name"]:
                            step["has"] = item_check("Hunter Knife")

                        elif "Haste Block" in step["name"]:
                            step["has"] = "maybe"

                        elif "Century Cake" in step["name"]:
                            step["has"] = cake_check("cake_walk_speed")

                    except:
                        step["has"] = "false"
                task["completion_list"] = speed_steps_req
            
            else:
                task["completion_list"] = [{'step': "Error :(", "has":"false"}]
            
        else:
            task["percent_complete"] = 0.0
            task["eta"] = "NOT DONE"


    if latest == bingo_id:
        for task in tasks:
            if task["id"] in completed_tasks:
                task["percent_complete"] = 100
                task["eta"] = "DONE"
            # If minion/craft, check collection
            # If stat, check stats
    else: 
        for task in tasks: 
            task["percent_complete"] = 0.0
    return(tasks)

def sortbyeta(init_tasks):
# NOTE: OK so when I initially began this project, I figured it might be useful to organize the tasks by ETA. 
# This could be a feature, but then I'd have to find a place on the website for another options bar...

    #sorted_tasks = sorted(init_tasks, key = lambda item: item["percent_complete"])
    sorted_tasks = init_tasks
    return(sorted_tasks)
    