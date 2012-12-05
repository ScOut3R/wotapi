import urllib2
import simplejson
from wotapi.statistics import player
from wotapi.cache import cache


class Clan(object):
    
    def __init__(self, clan_id, region, use_cache=False, cache_host="127.0.0.1", cache_port='11211'):
        self.clan_id = clan_id
        self.use_cache = use_cache
        if region == 'eu':
            self.region = '.eu'
        elif region == 'us':
            self.region = '.com'
        elif region == 'ru':
            self.region = '.ru'
        elif region == 'asia':
            self.region = '-sea.com'
        
        if self.use_cache == True:
            self.cache = cache.Memcache(cache_host, cache_port)
        
    def memberlist(self):
        if self.use_cache:
            cached_data = self.cache.get('wotapi.clan_memberlist')
            if cached_data != None:
                return cached_data
        request = urllib2.Request('http://worldoftanks%s/community/clans/%s/members/?type=table&offset=0&limit=100&order_by=role&search=&echo=1&id=clan_members_index' % ( self.region, self.clan_id ))
        opener = urllib2.build_opener()
        opener.addheaders = [ ('X-CSRFToken', 'MIu7a4WxPinfs9sdf694z6K64wbYPdAP'), ('X-Requested-With', 'XMLHttpRequest')]
        f = opener.open(request)
        clan_data = simplejson.load(f)
        if self.use_cache:
            self.cache.set('wotapi.clan_memberlist', clan_data['request_data']['items'])
        return clan_data['request_data']['items']
    
    def stat(self):
        members = self.memberlist()
        if self.use_cache:
            cached_data = self.cache.get('wotapi.clan_stats')
            if cached_data != None:
                return cached_data
        battles = 0
        for member in members:
            battles = battles + int(player.Player(account_id=member['account_id'], name=member['name'], region='eu').single_stat('Battles Participated').replace(u'\xa0', u''))
        if self.use_cache:
            self.cache.set('wotapi.clan_stats', { 'members': len(members), 'battles': battles })
        return { 'members': len(members), 'battles': battles }
