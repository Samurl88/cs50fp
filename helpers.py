from bs4 import BeautifulSoup
import requests
import re

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
    strategy = f"Base - {base_stat}\n"
    i = 0
    while base_stat < requiredAmount:
        try:
            
            strategy += f"{steps[i][0]} - {steps[i][1]}\n"
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

# TODO: Add completion % for each task
def completion(ign, uuid, profile_data, tasks, completed_tasks, latest, bingo_id):
# TODO: Personalized Completion Data Here
    for task in tasks:
        if task["method"] == "MINION":
            required_amount = task["required_amount"]
            try:
                item = (task["id"].replace("collection_", "")).upper()
                progress = profile_data["members"][uuid]["collection"][item]
            except:
                progress = 0
            task["eta"] = f"{str(progress)} / {str(required_amount)}"
            task["percent_complete"] = progress / required_amount

        elif "stat" in task["id"]:
            profile_id = profile_data["profile_id"]
            required_amount = task["required_amount"]
            shiiyu_data = requests.get("https://sky.shiiyu.moe/api/v2/profile/{ign}").json()
            for profile in shiiyu_data:
                if profile["profile_id"] == profile_id:
                    bingo_profile = profile
            print(bingo_profile)
            
        
    if latest == bingo_id:
        for task in tasks:
            if task["id"] in completed_tasks:
                task["percent_complete"] = 100
                #task["eta"] = "DONE" NOTE ADD THIS IN
            else:
                task["percent_complete"] = 0
            # If minion/craft, check collection
            # If stat, check stats
    else: 
        for task in tasks: 
            task["percent_complete"] = 0
    return(tasks)

def sortbyeta(init_tasks):
# TODO: Order: BY ETA
    sorted_tasks = init_tasks
    return(sorted_tasks)
    
