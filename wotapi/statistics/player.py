import urllib2
from bs4 import BeautifulSoup


class Player(object):
    
    def __init__(self, account_id, name):
        self.account_id = account_id
        self.name = name
        self.lookup_strings_basic = [ ' Defeats: ', ' Battles Survived: ', ' Hit Ratio: ', ' Maximum Experience per Battle: ' ]
        self.lookup_strings_rating = [ 'Global Rating', 'Victories/Battles', 'Average Experience per Battle', 'Victories', 'Battles Participated', 'Capture Points', 'Damage Caused', 'Defense Points', 'Targets Destroyed', 'Targets Detected', 'Total Experience' ]

    def stats(self):
        request = urllib2.urlopen('http://worldoftanks.eu/community/accounts/%s-%s/' % ( self.account_id, self.name))
        f = request.read()
        request.close()
        soup = BeautifulSoup(f)
        stats = []

        for lookup_string in sorted(self.lookup_strings_basic):
            temp = soup.find("td", text=lookup_string)
            stats.append([ lookup_string[1:-2], temp.find_next_sibling().string ] )

        for lookup_string in sorted(self.lookup_strings_rating):
            temp = soup.find("td", text=lookup_string)
            stats.append([ lookup_string, temp.find_next_sibling().string, temp.find_next_sibling().find_next_sibling().string ] )
    
        return stats
