import urllib2
import simplejson


class Clan(object):
    
    def __init__(self, clan_id, region):
        self.clan_id = clan_id
        if region == 'eu':
            self.region = '.eu'
        elif region == 'us':
            self.region = '.com'
        elif region == 'ru':
            self.region = '.ru'
        elif region == 'asia':
            self.region = '-sea.com'
        
    def memberlist(self):
        request = urllib2.Request('http://worldoftanks%s/community/clans/%s/members/?type=table&offset=0&limit=100&order_by=role&search=&echo=1&id=clan_members_index' % ( self.region, self.clan_id ))
        opener = urllib2.build_opener()
        opener.addheaders = [ ('X-CSRFToken', 'MIu7a4WxPinfs9sdf694z6K64wbYPdAP'), ('X-Requested-With', 'XMLHttpRequest')]
        f = opener.open(request)
        clan_data = simplejson.load(f)
        return clan_data['request_data']['items']
