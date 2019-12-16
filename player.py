
class Player:
    VERSION = "1.0"

    def betRequest(self, game_state):
        player_index = game_state['in_action']
        players = game_state['players']
        player = players[player_index]

        community_cards = game_state['community_cards']
        min_raise = game_state['minimum_raise']
        if not community_cards:
            return min_raise
        return 0

    def showdown(self, game_state):
        pass

