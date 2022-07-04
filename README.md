# cs50fp
#### Video Demo: https://www.youtube.com/watch?v=6jFvN45Hw1M
#### Description:

Here's my CS50 Final Project, months in the making! I've created a essentially a helper for a game in a game in a game in a game -- that is, a "solver" (I'll get to those quotation marks later) for the Minecraft server Hypixel's game mode Skyblock's monthly event of Bingo, in which a player must complete certain tasks ranging in difficulty within a week. At a broad level, this website reads data from Hypixel's Public API, finds certain keywords & phrases, and gives some solution or relevant information for each Bingo task.

Let's go through each of the files!

## app.py:
How about we start with the backbone of this entire project: app.py! First, I'd request the newest list of Bingo tasks from the Hypixel Public API and run something based on the nature of each task (filtered with one gargantuan if-elif-elif-...-else statement using each task's id or title). For general tasks, I'd get a list of keywords or phrases from the task's lore (a.k.a. description) and run these through a web scraper (see helpers.py) -- the first successful result would be returned, and I'd call that the "strategy" (Here's where the quotations from earlier come in: I'm not sure general information counts as a "solver", and a design choice I debated was taking information to others' posted guides online. That might've been a bit too difficult, though, since each website would have differing formatting, and sifting through one uniform website was enough trouble...). For tasks I figured my program could automate and personalize, I ran specific sets of code to determine what the player should do. Most of the work was done in helpers.py, so I'll go over the ones I'm most proud of there!

## helpers.py:
Helpers.py - If app.py is the backbone of this project, helpers.py is the backbone to that backbone. I figured that I'd copy pset9's use of a helper functions folder, and it definitely helped limit the clutter in the main file. Here are the main functions:
- find_text(), get_skill_info(), attempt_search(): Each of these functions use the library BeautifulSoup to scrape information from the Official Hypixel Skyblock Wiki, looking through header id's for key words (notably "Obtaining" & "Location"). It reports a specific blurb of information, and bingo.html displays that as the strategy. (Looking back, I might've been able to condense find_text() and attempt_search() into one function, but here we are)
- completion(): This is the big one! Here, I personalized the results for each player based on their progress, data which was obtained through the use of Hypixel's Public API and a community sourced API, SkyCrypt. Unfortunately, for some reason the latter takes literal ages to load per request, elongating the buffer time from, like, two to five-and-a-half-ish seconds. It's sad, but there's nothing I can do since it does a bunch of decodings and calculations necessary for this personalization. Here's some highlights of helpers.py!
- Overall Progress: I had an "eta" and "percent_complete": the former a fraction (550 / 10K), the latter a percentage (0.06%). Unique to each task, I took data from either API to determine both of these values.
- Stat Tasks (elif "stat" in task["id"]): Each player has a set of stats: health, defense, strength, and so on. A common task in Bingo is to reach a certain milestone for some stat - another problem that I found to be easily (borderline quotation marks there) automatable. For each stat that had the possibility to appear in Bingo, I created a list of tuples, each consisting of both a step and how much that step offered to the stat. Then, using the function stat_strat(), I determined the progress of the player in regards to the list of steps provided (so, so many if-else statments, unique to each step... there might have been a better way to do it, but I'm not sure how!). This one took a while to iron out, since I was going back and forth on whether to put in the work of analyzing every single step possible -- I'm glad I ended up doing so, though.
- Pets, Armor, and Accessories: Similar to Stat Tasks, I debated on adding personalized progress for each but ultimately ended up doing so. Similar to Stat Tasks, these dug through APIs for the progress of the player based on lists defined in app.py. 
- Collection Tasks (if task["method"] == "MINION"): In every Bingo, there's at least one collection task where the player must collected a certain amount of a specific item. The obvious solution to this was minions, bots that automatically generate materials regardless of player status. To implement this strategy, I gathered minion data (namely delays between creating/collecting an item) from existing CSVs online and stored it in a database. I wrote some code to calculate how long it would take using minions alone to reach a certain collection goal, and with that, how many unloads would be necessary (minions have limited storage). Furthermore, I scraped and added some basic information of the item being collected, just for the well-rounded strategy.

## bingo.db:
- This database holds Bingo information (task name, id, strategy, eta, ...) as well as minion data (of course accessed through SQLite3).

## layout.html:
- I'm pretty proud of my website's overall asthetic! If you're an avid Skyblocker, you might notice the heavy inspiration from SkyCrypt.

## index.html:
- It's a little plain, but it gets the job done. A feature that could possibly be added would be a list of recently searched players (or favorited players)

## bingo.html:
- This took literal months to build, and you'll notice in the video showcase the many iterations bingo.html underwent. However, something that remained constant throughout was the heavy use of grids: the elements were organized by grid, and most had grids themselves, too. There might've been a better way to do it, but that I don't know! Here's a run-down of each element:
  - Username input box (grid-input): Allows new username input.
    - This is where the user can input a new username and search. On a side note, I used the POST method as I figured the url looked cleaner (.../bingo?ign="bleh" -> .../bingo). That was a pretty bad oversight, though, as attempting to refresh via browser always results in a confirmation screen. It definitely can be tedious to refresh, but it's not world-ending enough for me to figure out how to redo it with GET.
  - Bingo board (grid-board): Displays Bingo board. 
    - Here's a downside to using a grid based on viewport height - the longer the screen, the slender-er the Bingo board. It admittedly looks... less than perfect on some screens, but, again, it doesn't render my website unusable, so it stays. An extra feature that could have been added would have been the ability for each square to act as a button that would function similar to those in the list of tasks.
  - Strategy box (grid-strat): Displays strategy per task. 
This was initially a to-do list consisting of uncompleted tasks, but I redesigned it to make better use of the space.
  - Task filtering (grid-select): Filters tasks. 
    - I'm pretty proud of the javascript used to make this filtering function. Clicking on one of the words reveals only the tasks pertaining to the category and hides all others. Looking back, there might have been more useful categories, though (eg. CRAFT -> STAT)
  - List of tasks (grid-tasks): Displays list of tasks. 
    - Each item contains the task's title, description, and progress of the user.
This element underwent the most drastic changes. I initially planned to display the strategy of each task within its little box along with the task's description and the player's progress, but that would have never worked due to the size limitation. As mentioned above, I moved the strategies to the bottom-left box. Additionally, I debated whether to add a progress bar but ultimately decided against it for a cleaner look.

## about.html:
- I'll either copy & paste this there or remove the page entirely and replace it with a github link.

# THANK YOU CS50!
