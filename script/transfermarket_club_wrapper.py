from bs4 import BeautifulSoup
import re
import codecs
import sys
import json

f = codecs.open(sys.argv[1])
output = codecs.open(sys.argv[2], "w")
# f = codecs.open("test.jl")
ii=0
url_lst = []

for line in f:
    profile = dict()

    data = json.loads(line)
    print ii
    ii += 1

    url = data["url"]
    print url
    html_doc = data["raw_content"]
    soup = BeautifulSoup(html_doc, 'html.parser')
    if url not in url_lst and soup(text=re.compile(r'Official club name:')):
        url_lst.append(url)

        if soup.find("div", {"class": "dataErfolge hide-for-small"}):
            profile["honors"] = dict()
            club_wins = soup.find("div", {"class": "dataErfolge hide-for-small"})
            for a in club_wins.find_all('a'):
                profile["honors"][a.get("title").strip().lower()] = int(a.find("span", {"class": "dataErfolgAnzahl"}).text) if a.find("span", {"class": "dataErfolgAnzahl"}) else "none"

        if soup.find("div", {"class": "dataZusatzDaten"}):
            league_name = soup.find("div", {"class": "dataZusatzDaten"}).span.a.text
            profile["league name"] = league_name.strip()

        if soup(text=re.compile(r'League level:')):
            if soup(text=re.compile(r'League level'))[0].parent.a:
                league_level = soup(text=re.compile(r'League level'))[0].parent.a
                profile["country"] = league_level.img.get("title").strip()
                profile["league level"] = league_level.text.strip()

        if soup(text=re.compile(r'Squad size:')):
            squad_size = soup(text=re.compile(r'Squad size'))[0].parent.next_sibling.next_sibling
            profile["squad size"] = squad_size.text.strip()

        if soup(text=re.compile(r'Average age:')):
            average_age = soup(text=re.compile(r'Average age'))[0].parent.next_sibling.next_sibling
            profile["average age"] = average_age.text.strip().replace(",", ".")

        if soup(text=re.compile(r'Current international players:')):
            current_international_players = soup(text=re.compile(r'Current international players'))[0].parent.next_sibling.next_sibling
            profile["current international players"] = current_international_players.text.strip()

        if soup(text=re.compile(r'Foreign players:')):
            foreign_players = soup(text=re.compile(r'Foreign players'))[0].parent.next_sibling.next_sibling
            profile["foreign players"] = {}
            ll = [d.strip() for d in foreign_players.text.split()]
            if len(ll) >=3:
                profile["foreign players"]["count"] = ll[0]
                profile["foreign players"]["percentage"] = ll[1].replace(",", ".") + ll[2]

        if soup(text=re.compile(r'Stadium:')):
            stadium = soup(text=re.compile(r'Stadium'))[0].parent.next_sibling.next_sibling
            ll = [d.strip() for d in stadium.text.split()]
            if len(ll) >= 2:
                profile["stadium"] = {}
                profile["stadium"]["name"] = ll[0]
                profile["stadium"]["seats"] = ll[1]

        if soup(text=re.compile(r'Current transfer record:')):
            current_transfer_record = soup(text=re.compile(r'Current transfer record'))[0].parent.next_sibling.next_sibling
            if len(current_transfer_record.text.split()) >= 2:
                profile["current transfer record"] = current_transfer_record.text.split()[0].strip()+ " " + current_transfer_record.text.split()[1].strip()
            else:
                profile["current transfer record"] = current_transfer_record.text.split()[0].strip()

        if soup.find("div", {"class": "dataMarktwert"}):
            total_value = soup.find("div", {"class": "dataMarktwert"}).text.split()
            profile["total market value"] = total_value[0].strip() + " " + total_value[1].strip()


        if soup.find("div", {"class": "grid-view"}):
            if soup.find("div", {"class": "grid-view"}).table:
                profile["players"] = []
                player_lst = soup.find("div", {"class": "grid-view"}).table.tbody.findChildren(recursive=False)
                for each_player in player_lst:
                    this_player = {}
                    tds = each_player.find_all('td')
                    if len(tds) >=0:
                        this_player["number"] = tds[0].text if tds[0].text else "unknown"
                    if len(tds) >=5:
                        this_player["name"] = tds[5].text.strip() if tds[5].text.strip() else "unknown"
                    if len(tds) >=4:
                        this_player["position"] = tds[4].text.strip() if tds[4].text.strip() else "unknown"
                    if len(tds) >=6:
                        this_player["birth day"] = tds[6].text.replace(")", "").split("(")[0].strip() if tds[6].text.replace(")", "").split("(")[0].strip() else "unknown"
                        this_player["age"] = tds[6].text.replace(")", "").split("(")[1].strip() if tds[6].text.replace(")", "").split("(")[1].strip() else "unknown"
                    if len(tds) >=7:
                        this_player["nationality"] = []
                        if tds[7].find_all('img'):
                            for a_img in tds[7].find_all('img'):
                                this_player["nationality"].append(a_img.get("title").strip())
                    if len(tds[8].text.split()) >= 2:
                        this_player["market value"] = tds[8].text.split()[0].strip() + " " + tds[8].text.split()[1].strip()
                    profile["players"].append(this_player)

        # if soup(text=re.compile(r'Official club name:')):
        club_inf = soup(text=re.compile(r'Official club name'))[0].parent.parent.parent
        club_inf_lst = club_inf.find_all('tr')
        profile['club address'] = ""
        for an_inf in club_inf_lst:
            if an_inf.th.text == u'Official club name:':
                profile['Official club name'] = an_inf.td.text.strip()
            if an_inf.th.text == u'Address:' or an_inf.th.text == '':
                profile['club address'] = (profile['club address'] + " " + an_inf.td.text.strip()).strip()
            if an_inf.th.text == u'Tel:':
                profile['Tel'] = an_inf.td.text.strip()
            if an_inf.th.text == u'Fax:':
                profile['Fax'] = an_inf.td.text.strip()
            if an_inf.th.text == u'Foundation:':
                profile['Foundation'] = an_inf.td.text.strip()



              
        # data["knowledge_graph"] = profile
        json.dump(profile, output)
        output.write("\n")

f.close()
output.close()



