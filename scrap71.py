from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.page_load_strategy = 'eager' 
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=chrome_options)
driver.set_page_load_timeout(45)

base_url = "https://www.fotmob.com"
main_url = f"{base_url}/leagues/77/stats/season/24254/teams"

teams_perfect_data = {}

try:
    print("Opening main page and capturing 28 stat cards...")
    driver.get(main_url)
    time.sleep(5)
    
    main_html = driver.page_source
    main_soup = BeautifulSoup(main_html, 'html.parser')
    
    stat_cards = main_soup.find_all('a', href=re.compile(r'/leagues/77/stats/season/\d+/teams/.+'))
    
    stat_tasks = []
    seen_hrefs = set()
    
    for card in stat_cards:
        href = card['href']
        if href not in seen_hrefs:
            seen_hrefs.add(href)
            title_element = card.find(['h3', 'span', 'p', 'div'])
            stat_title = title_element.text.strip() if title_element else href.split('/')[-1].replace('_stat', '').replace('_', ' ').title()
            
            if len(stat_title) > 3 and not stat_title.isdigit():
                stat_tasks.append({'title': stat_title, 'href': href})

    print(f"Successfully collected {len(stat_tasks)} sub-stats.")

    for index, task in enumerate(stat_tasks, 1):
        stat_name = task['title']
        full_stat_url = task['href'] if task['href'].startswith('http') else base_url + task['href']
        
        print(f"[{index}/{len(stat_tasks)}] Scraping data for: {stat_name}...")
        
        try:
            driver.get(full_stat_url)
            time.sleep(3)
            
            stat_html = driver.page_source
            stat_soup = BeautifulSoup(stat_html, 'html.parser')
            
            team_links = stat_soup.find_all('a', href=re.compile(r'/teams/\d+/overview/'))
            
            if not team_links:
                team_links = stat_soup.find_all('a', href=re.compile(r'/teams/\d+/'))
            
            for link in team_links:
                name_element = link.select_one('[class*="TeamOrPlayerName"]')
                if not name_element:
                    continue
                team_name = name_element.text.strip()
                
                value_element = link.select_one('[class*="StatValue"]')
                if value_element:
                    stat_value = value_element.text.strip()
                    
                    if team_name not in teams_perfect_data:
                        teams_perfect_data[team_name] = {}
                    
                    teams_perfect_data[team_name][stat_name] = stat_value
                    
        except Exception as e:
            print(f"Error in page {stat_name}, skipping...")
            continue

finally:
    driver.quit()
    print("Browser closed. Formatting data...")

if teams_perfect_data:
    df_clean = pd.DataFrame.from_dict(teams_perfect_data, orient='index')
    df_clean = df_clean.reset_index().rename(columns={'index': 'Team Name'})
    
    black_list = ['Stats', 'Teams', 'Players', 'Overview', 'Table', 'Matches', 'News', 'Fixtures', 'Knockout', 'Seasons']
    df_clean = df_clean[~df_clean['Team Name'].isin(black_list)]
    df_clean = df_clean[df_clean['Team Name'].str.len() > 2]
    
    output_file = "World_Cup_2026_Perfect_Analysis_Grid_71_final.xlsx"
    df_clean.to_excel(output_file, index=False)
    
    print("\nProcess finished successfully!")
    print(f"File saved as: {output_file}")
    print(f"Dimensions: {df_clean.shape[0]} teams x {df_clean.shape[1] - 1} stats.")
else:
    print("\nNo data collected. Please check your internet connection and script configuration.")