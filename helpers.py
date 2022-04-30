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

#[{'name': 'Skilled', 'lore': '', 'method': '', 'eta': 0}, {'name': 'Diamond Collector', 'lore': '§7Reach §a5,000 §7Diamond Collection.', 'method': 'MINION', 'eta': 15}

# TODO: Add completion % for each task
def completion(tasks, completed_tasks):
# TODO: Add completion % for each task, THIS IS A PLACEHOLDER
# TODO: For minions, at least: acknowledge collection progress, count toward & recalculate ETA
    for task in tasks:
        if task["id"] in completed_tasks:
            task["completion"] = 100
            print(task)
        else:
            task["completion"] = 0
        # If minion/craft, check collection
        # If stat, check stats
    return(tasks)

def sortbyeta(init_tasks):
# TODO: Order: BY ETA
    sorted_tasks = init_tasks
    return(sorted_tasks)

