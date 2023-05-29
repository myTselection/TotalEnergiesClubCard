
import logging
import requests
import urllib.parse
from bs4 import BeautifulSoup

_LOGGER = logging.getLogger(__name__)

class ComponentSession(object):
    def __init__(self):
        self.s = requests.Session()
        self.s.headers["User-Agent"] = "Python/3"
        self.s.headers["Accept-Language"] = "en-US,en;q=0.9"

    def login(self, cardnumber, password):
        response = self.s.get("https://services.totalenergies.be/nl/inloggen-op-uw-club-account",timeout=30,allow_redirects=True)
        print("post result status code: " + str(response.status_code))
        
        # response = self.s.post("https://services.totalenergies.be/cdn-cgi/rum?",data=data,timeout=30,allow_redirects=False)
        # print("post result status code: " + str(response.status_code))
        

        data = {
            "noCarte": cardnumber,
            "code": password,
            "p_LG": "NL",
            "p_PAYS": "BE",
            "menucourant": "adherent",
            "codeCategorie": ""
        }
        # response = self.s.post("https://club.totalenergies.be/authentification/authentification.php?PAYS=BE&LG=NL",data='{"noCarte": '+cardnumber+',"code": '+password+', "p_LG": "NL", "p_PAYS": "BE", "menucourant": "adherent", "codeCategorie":""}',timeout=30,allow_redirects=False)
        response = self.s.post("https://club.totalenergies.be/authentification/authentification.php?PAYS=BE&LG=NL",data=data,timeout=30,allow_redirects=False)
        print("post result status code: " + str(response.status_code))
        for cookie in self.s.cookies:
            print(cookie.name, cookie.value)
        clubCookie = self.s.cookies.get('club')
        clubCookie = urllib.parse.unquote(clubCookie)
        print(f"clubCookie: {clubCookie}")
        tab_valeurs = clubCookie.split(':')
        connect = tab_valeurs[0]
        if connect == '1':
            nom = tab_valeurs[1]
            prenom = tab_valeurs[2]
            email = tab_valeurs[3]
            noEmetteur = tab_valeurs[4]
            noCarte = tab_valeurs[5]
            dtFinAssistance = tab_valeurs[6]
            phraseAssistance = tab_valeurs[7]
            points = tab_valeurs[8]
        print(f"nom: {nom}, prenom: {prenom}, email {email}, noEmetteur {noEmetteur}, noCarte {noCarte}, dtFinAssistance {dtFinAssistance}, phraseAssistance {phraseAssistance}, points {points}")
        # print("post result response: " + str(response.text))
        # assert response.status_code == 200

    def userdetails(self):

        response = self.s.get("https://services.totalenergies.be/nl/promoties/total-club-uw-loyaliteit-wordt-beloond/log-bij-total-club/welkom-bij-total-club",timeout=30,allow_redirects=False)
        print("post result status code: " + str(response.status_code))
        print("post result response: " + str(response.text))
        response = self.s.get("https://services.totalenergies.be/nl/promoties/club-uw-loyaliteit-wordt-beloond/log-bij-club/welkom-bij-total-club",timeout=30,allow_redirects=True)
        print("post result status code: " + str(response.status_code))
        # print("post result response: " + str(response.text))
        print(f"header: {response.headers}")
        print(f"cookies: {self.s.cookies}")
        for cookie in self.s.cookies:
            print(cookie.name, cookie.value)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        div_assistance = soup.find('div', id= 'dtFinAssistance')

        print("Assistance: " + div_assistance.get_text(strip=True))

        all_text = soup.get_text(strip=True)
        # print(all_text)

        # assert response.status_code == 200

cs = ComponentSession()
cs.login("XXXXXXXXXX", "XXXX")
# cs.userdetails()