import datetime
import requests
from bs4 import BeautifulSoup
from flask import abort
import re

def findReservation(date, category):
    # dict of res options
    categories = {"badminton": "https://services.rec.rutgers.edu/Program/GetProgramDetails?courseId=a651ec00-2ed3-4106-818e-fcabf7b9993d&semesterId=3302ba85-8b33-4145-b755-2d709e0ec9ef",
                    "olympic pool": "https://services.rec.rutgers.edu/Program/GetProgramDetails?courseId=0c0f9f29-eabf-4316-93a1-d0693b61e08f&semesterId=3302ba85-8b33-4145-b755-2d709e0ec9ef",
                    "basketball": "https://services.rec.rutgers.edu/Program/GetProgramDetails?courseId=792d01fe-2e71-4d94-97f5-964c25e1efab&semesterId=3302ba85-8b33-4145-b755-2d709e0ec9ef",
                    "patio pool": "https://services.rec.rutgers.edu/Program/GetProgramDetails?courseId=f5bca03e-2f13-4821-be05-0fcdff6d5e16&semesterId=3302ba85-8b33-4145-b755-2d709e0ec9ef",
                    "gym": "https://services.rec.rutgers.edu/Program/GetProgramDetails?courseId=694b3079-a4f9-4988-94d5-6374f9d3fe40&semesterId=3302ba85-8b33-4145-b755-2d709e0ec9ef",
                    "volleyball": "https://services.rec.rutgers.edu/Program/GetProgramDetails?courseId=d2f8f574-5526-4fb6-8014-42cd314f340c&semesterId=3302ba85-8b33-4145-b755-2d709e0ec9ef"}
    
    # fetch page
    res = requests.get(categories[category])
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
    
    return {"monitoring": False, "spots_remaining": remaining, "currently_availible": availible, "category": category}