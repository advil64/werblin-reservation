import datetime
import requests
from bs4 import BeautifulSoup
from flask import abort
import re

def findReservation(date):
    # currently only for swimming
    url = "https://services.rec.rutgers.edu/Program/GetProgramDetails?courseId=0c0f9f29-eabf-4316-93a1-d0693b61e08f&semesterId=3302ba85-8b33-4145-b755-2d709e0ec9ef"
    
    # fetch page
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    cards = soup.find_all(class_='program-schedule-card-caption')

    # indicates that the date is availible for reservation
    availible = False
    remaining = 0

    # loop through reservations
    for res in cards:
        # find if the date exists
        text = res.get_text().strip()
        res_date = res.find(class_='program-schedule-card-header').get_text().strip()
        spots = res.find('span', class_='pull-right').get_text().strip()
        if date.strftime("%A, %B %d, %Y") in res_date and date.strftime("%-I:%M %p -") in text:
            availible = True
            if "spot(s) available" in spots:
                remaining = int(spots.split(' ')[0])
            print(text)
    
    return {"monitoring": False, "spots_remaining": remaining, "currently_availible": availible}