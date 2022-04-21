import pandas
from roman_arabic_numerals import conv
from cs50 import SQL

data = pandas.read_csv('miniondata.csv')
df = pandas.DataFrame(data)
print(df)

db = SQL("sqlite:///bingo.db")

db.execute("DROP TABLE miniondata")
db.execute("CREATE TABLE miniondata (type text, tier int, ugMaterial text, ugCost int, ugDisplay text, delay int, storage int)")


for row in df.itertuples():
    if row.tierA <= 5:
        db.execute("INSERT INTO miniondata VALUES (?, ?, ?, ?, ?, ?, ?)", row.type, row.tierA, row.ugMaterial, row.ugCost, row.ugDisplay, row.delay, row.storage)
        