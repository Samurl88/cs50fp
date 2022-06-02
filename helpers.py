from bs4 import BeautifulSoup
import requests

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
    return(str(para))

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

#[{'name': 'Skilled', 'lore': '', 'method': '', 'eta': 0}, {'name': 'Diamond Collector', 'lore': '§7Reach §a5,000 §7Diamond Collection.', 'method': 'MINION', 'eta': 15}

# TODO: Add completion % for each task
def completion(tasks, completed_tasks, latest, bingo_id):
# TODO: Add completion % for each task, THIS IS A PLACEHOLDER
# TODO: For minions, at least: acknowledge collection progress, count toward & recalculate ETA
    if latest == bingo_id:
        for task in tasks:
            if task["id"] in completed_tasks:
                task["completion"] = 100
            else:
                task["completion"] = 0
            # If minion/craft, check collection
            # If stat, check stats
    else: 
        for task in tasks: 
            task["completion"] = 0
    return(tasks)

def sortbyeta(init_tasks):
# TODO: Order: BY ETA
    sorted_tasks = init_tasks
    return(sorted_tasks)

