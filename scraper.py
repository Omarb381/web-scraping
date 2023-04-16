from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv

date = input("Enter date in format mm/dd/YYY :")
page = requests.get(f"https://www.yallakora.com/match-center/?date={date}")

def main(page):
    src = page.content
    soup = BeautifulSoup(src, 'lxml')
    match_details = []
    championships = soup.find_all("div", {'class': 'matchCard'})

    def get_info(championship):
        championship_title = championship.contents[1].find('h2').text.strip()
        all_matches = championship.contents[3].find_all('li')
        number_match = len(all_matches)
        for i in range(number_match):
            team_A = all_matches[i].find("div", {'class': 'teams teamA'}).text.strip()
            team_B = all_matches[i].find("div", {'class': 'teams teamB'}).text.strip()
            match_result = all_matches[i].find("div", {'class': 'MResult'}).find_all("span", {'class': 'score'})
            score = f"{match_result[0].text.strip()} - {match_result[1].text.strip()}"
            match_time = all_matches[i].find("div", {'class': 'MResult'}).find("span", {'class': 'time'}).text.strip()
            match_details.append({'نوع البطولة': championship_title, 'الفريق الأول': team_A, 'الفريق الثاني': team_B, 'موعد المبارة': match_time, 'النتيجة': score})

    for i in range(len(championships)):
        get_info(championships[i])

    keys = match_details[0].keys()
    with open("D:\\Alex ferberg\\scrap.csv", 'w',) as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(match_details)
        print("file created")


main(page)
