import urllib2
from bs4 import BeautifulSoup


class Player(object):
    
    def __init__(self, account_id, name, region):
        self.account_id = account_id
        self.name = name
        if region == 'eu':
            self.region = '.eu'
        elif region == 'us':
            self.region = '.com'
        elif region == 'ru':
            self.region = '.ru'
        elif region == 'asia':
            self.region = '-sea.com'
        self.lookup_strings_basic = [ ' Defeats: ', ' Battles Survived: ', ' Hit Ratio: ', ' Maximum Experience per Battle: ' ]
        self.lookup_strings_rating = [ 'Global Rating', 'Victories/Battles', 'Average Experience per Battle', 'Victories', 'Battles Participated', 'Capture Points', 'Damage Caused', 'Defense Points', 'Targets Destroyed', 'Targets Detected', 'Total Experience' ]

    def stats(self):
        request = urllib2.urlopen('http://worldoftanks%s/community/accounts/%s-%s/' % ( self.region, self.account_id, self.name))
        f = request.read()
        request.close()
        soup = BeautifulSoup(f)

        for lookup_string in sorted(self.lookup_strings_basic):
            temp = soup.find("td", text=lookup_string)
            if lookup_string == ' Defeats: ':
                self.defeats = temp.find_next_sibling().string
            if lookup_string == ' Battles Survived: ':
                self.battles_survived = temp.find_next_sibling().string
            if lookup_string == ' Hit Ratio: ':
                self.hit_ratio = temp.find_next_sibling().string
            if lookup_string == ' Maximum Experience per Battle: ':
                self.maximum_xp_per_battle = temp.find_next_sibling().string

        for lookup_string in sorted(self.lookup_strings_rating):
            temp = soup.find("td", text=lookup_string)
            if lookup_string == 'Global Rating':
                self.global_rating = { 'value': temp.find_next_sibling().string, 'place': temp.find_next_sibling().find_next_sibling().string }
            if lookup_string == 'Victories/Battles':
                self.victories_battles = { 'value': temp.find_next_sibling().string, 'place': temp.find_next_sibling().find_next_sibling().string }
            if lookup_string == 'Average Experience per Battle':
                self.average_xp_per_battle = { 'value': temp.find_next_sibling().string, 'place': temp.find_next_sibling().find_next_sibling().string }
            if lookup_string == 'Victories':
                self.victories = { 'value': temp.find_next_sibling().string, 'place': temp.find_next_sibling().find_next_sibling().string }
            if lookup_string  == 'Battles Participated':
                self.battles = { 'value': temp.find_next_sibling().string, 'place': temp.find_next_sibling().find_next_sibling().string }
            if lookup_string == 'Capture Points':
                self.capture_points = { 'value': temp.find_next_sibling().string, 'place': temp.find_next_sibling().find_next_sibling().string }
            if lookup_string == 'Damage Caused':
                self.damage_caused = { 'value': temp.find_next_sibling().string, 'place': temp.find_next_sibling().find_next_sibling().string }
            if lookup_string == 'Defense Points':
                self.defense_points = { 'value': temp.find_next_sibling().string, 'place': temp.find_next_sibling().find_next_sibling().string }
            if lookup_string == 'Targets Destroyed':
                self.targets_destroyed = { 'value': temp.find_next_sibling().string, 'place': temp.find_next_sibling().find_next_sibling().string }
            if lookup_string == 'Targets Detected':
                self.targets_detected = { 'value': temp.find_next_sibling().string, 'place': temp.find_next_sibling().find_next_sibling().string }
            if lookup_string == 'Total Experience':
                self.total_xp = { 'value': temp.find_next_sibling().string, 'place': temp.find_next_sibling().find_next_sibling().string }
    
    def single_stat(self, stat_name):
        request = urllib2.urlopen('http://worldoftanks%s/community/accounts/%s-%s/' % ( self.region, self.account_id, self.name))
        f = request.read()
        request.close()
        soup = BeautifulSoup(f)
        temp = soup.find("td", text=stat_name)
        return temp.find_next_sibling().string
