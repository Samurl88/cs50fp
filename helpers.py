from bs4 import BeautifulSoup
import requests
import re
import math

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

def stat_strat(base_stat, requiredAmount, steps):
    strategy = f"- Base → {base_stat}\n"
    i = 0
    while base_stat < requiredAmount:
        try:
            
            strategy += f"- {steps[i][0]} → {steps[i][1]}\n"
            base_stat += steps[i][1]
            i += 1
        except:
            # TODO: Add fairy soul suppport?
            break
    return strategy

def get_skill_info(skill):
    para = ""
    r = requests.get(f'https://wiki.hypixel.net/index.php?title={skill}&redirect=yes')
    soup = BeautifulSoup(r.content, 'html.parser')
    for header in soup.find_all(id=f"{skill}_XP_Gain"):
        para = header.find_next('p').get_text()
    return(str(para).strip())

def find_next_minions(requiredAmount, minion_list):
    #15, 25, 40, 60, 100
    return(str(minion_list))

def find_key_words(lore):
    #print(lore)

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
        para = ""
        r = requests.get(f'https://wiki.hypixel.net/index.php?title={phrase}&redirect=yes')
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')

            # If not Obtaining, try first para of page
            if not soup.find_all(id="Obtaining"):
                i = 0
                for para in soup.find_all('p'):
                    text = para.get_text()
                    if text != "\n" and text != "Content\n":
                        return(text.strip())

            # Try Obtaining
            for header in soup.find_all(id='Obtaining'):
                para = str(header.find_next('p').get_text())
                return(para.strip())

    return("I sure hope this task is self-explanatory because I didn't program for this to happen")

    

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
def completion(ign, uuid, profile_data, profile_id, tasks, completed_tasks, latest, bingo_id):
# TODO: Personalized Completion Data Here
    try: # In case API's down
        shiiyu_data = requests.get(f"https://sky.shiiyu.moe/api/v2/profile/{ign}").json() #NOTE: THIS IS SO SLOW!!!
        talisman_data = requests.get(f"https://sky.shiiyu.moe/api/v2/talismans/{ign}").json()
    except:
        shiiyu_data = []
        talisman_data = []

    for task in tasks:
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
                    task["eta"] = f"0 / {shorten_number(required_amount)}"
                    task["percent_complete"] = 0.0
            except:
                task["eta"] = "Turn on Collection API!"
                task["percent_complete"] = 0.0
                
        elif task["method"] == "COMMUNITY GOAL":
            task["eta"] = "---"
            task["percent_complete"] = 100

        elif "stat" in task["id"]:
            try:
                required_amount = task["required_amount"]
                task_stat = task["id"].replace("stat_", "")

                progress = shiiyu_data["profiles"][profile_id]["data"]["stats"][task_stat]

                task["eta"] = f"{str(progress)} / {str(required_amount)}"
                task["percent_complete"] = round(((progress / required_amount) * 100), 1)
            except:
                task["eta"] = "API too slow..."
                task["percent_complete"] = 0.0
            
        elif "fairy_souls" in task["id"]:
            try:
                required_amount = task["required_amount"]
                progress = profile_data["members"][uuid]["fairy_souls_collected"]
            except:
                progress = 0
            task["eta"] = f"{str(progress)} / {str(required_amount)}"
            task["percent_complete"] = round(((progress / required_amount) * 100), 1)
        
        elif "pets" in task["id"]:
            try:
                required_amount = task["required_amount"]
                progress = len(profile_data["members"][uuid]["pets"])
            except:
                progress = 0
            task["eta"] = f"{str(progress)} / {str(required_amount)}"
            task["percent_complete"] = round(((progress / required_amount) * 100), 1)

        elif "accessories" in task["id"]:
            try:
                required_amount = task["required_amount"]
                progress = len(talisman_data["profiles"][profile_id]["accessories"])
            except:
                progress = 0
            task["eta"] = f"{str(progress)} / {str(required_amount)}"
            task["percent_complete"] = round(((progress / required_amount) * 100), 1)
                
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
            except:
                progress = 0
            task["eta"] = f"{str(progress)} / {str(required_amount)}"
            task["percent_complete"] = round(((progress / required_amount) * 100), 1)
        
        # NOTE: Only checks equipped armor and armor stored in wardrobe
        elif "armor" in task["id"]:
            required_amount = task["required_amount"]
            armor_count = 0
            # Armor currently equipped
            try:
                equipped_armor = shiiyu_data["profiles"][profile_id]["items"]["armor"]
                armor_check = equipped_armor[0]["armor_name"]
                c = 0 # I don't know how to do this better
                for piece in equipped_armor:
                    if piece["armor_name"] == armor_check:
                        c += 1
                if c == 4:
                    armor_count += 1
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
            except:
                armor_count += 0
            task["eta"] = f"{str(armor_count)} / {str(required_amount)}"
            task["percent_complete"] = round(((armor_count / required_amount) * 100), 1)

        elif "bank" in task["id"]:
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
            required_amount = task["required_amount"]
            xp_list = {1:5, 2:25, 3:200, 4:1000, 5:5000, 6:20000, 7:100000, 8:400000, 9:1000000}
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
# TODO: Order: BY ETA
    #sorted_tasks = sorted(init_tasks, key = lambda item: item["percent_complete"])
    sorted_tasks = init_tasks
    return(sorted_tasks)
    