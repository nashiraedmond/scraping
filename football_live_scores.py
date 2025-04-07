# SCRAPPING FOOTBALL STATS

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import time
import csv

ua = UserAgent()
user_agent = ua.random


options = Options()
options.add_argument(f"user-agent={user_agent}")
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")


driver = webdriver.Chrome(options=options)

url = "https://www.espn.com/soccer/scoreboard"

driver.get(url)
time.sleep(3)

matches = driver.find_elements(By.CSS_SELECTOR, ".ScoreboardScoreCell__Competitors")

store_data = []
print("== ESPN Football Scores ===\n")

for match in matches:
    try:
        teams = match.find_elements(By.CSS_SELECTOR, ".ScoreCell__TeamName")
        scores = match.find_elements(By.CSS_SELECTOR, ".ScoreCell__Score")

        if len(teams) == 2 and len(scores) == 2:
            team1 = teams[0].text.strip()
            team2 = teams[1].text.strip()
            score1 = scores[0].text.strip()
            score2 = scores[1].text.strip()

            print(f"{team1} {score1} - {score2} {team2}")
            store_data.append([team1, score1, team2, score2])
    
    except Exception as e:
        print("Error parsing a match:", e)

csv_filename = "espn_scores.csv"
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Team 1", "Score 1", "Team 2", "Score 2"])
    writer.writerows(store_data)

print(f"\n Saved scores to {csv_filename}")

driver.quit()
