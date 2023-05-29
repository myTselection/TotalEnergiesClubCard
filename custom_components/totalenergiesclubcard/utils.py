
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.parse

import voluptuous as vol

_LOGGER = logging.getLogger(__name__)

_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.0%z"


def check_settings(config, hass):
    if not any(config.get(i) for i in ["username"]):
        _LOGGER.error("cardnumber was not set")
    else:
        return True
    if not config.get("password"):
        _LOGGER.error("password was not set")
    else:
        return True
    raise vol.Invalid("Missing settings to setup the sensor.")
        

class ComponentSession(object):
    def __init__(self):
        self.s = requests.Session()
        self.s.headers["User-Agent"] = "Python/3"
        self.s.headers["Accept-Language"] = "en-US,en;q=0.9"

    def login(self, cardnumber, password):
        response = self.s.get("https://services.totalenergies.be/nl/inloggen-op-uw-club-account",timeout=30,allow_redirects=True)
        
        data = {
            "noCarte": cardnumber,
            "code": password,
            "p_LG": "NL",
            "p_PAYS": "BE",
            "menucourant": "adherent",
            "codeCategorie": ""
        }
        response = self.s.post("https://club.totalenergies.be/authentification/authentification.php?PAYS=BE&LG=NL",data=data,timeout=30,allow_redirects=False)
        _LOGGER.debug("post result status code: " + str(response.status_code))
        _LOGGER.debug("post result response: " + str(response.text))
        
        clubCookie = self.s.cookies.get('club')
        clubCookie = urllib.parse.unquote(clubCookie)
        print(f"clubCookie: {clubCookie}")
        tab_valeurs = clubCookie.split(':')
        # Example nom: NAME, prenom: FIRSTNALE, email name@gmail.com, noEmetteur , noCarte , dtFinAssistance dd/mm/yyyy, phraseAssistance 0, points 999
        details = {
            "connect" : tab_valeurs[0],
            "lastname":  tab_valeurs[1],
            "firstname": tab_valeurs[2],
            "email" :tab_valeurs[3],
            "noEmetteur" : tab_valeurs[4],
            "noCarte" : tab_valeurs[5],
            "dtFinAssistance" : tab_valeurs[6],
            "phraseAssistance" : tab_valeurs[7],
            "points" : tab_valeurs[8],
            "last_update": datetime.now()
        }
        return details
        

