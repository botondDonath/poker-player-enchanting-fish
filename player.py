
class Player:
    VERSION = "1.0"

    def betRequest(self, game_state):
        player_index = game_state['in_action']
        players = game_state['players']
        player = players[player_index]

        community_cards = game_state['community_cards']
        min_raise = game_state['minimum_raise']

        current_buy_in = game_state['current_buy_in']
        our_bet = players[player_index]['bet']

        if not community_cards:
            return current_buy_in - our_bet + min_raise
        return 0

    def showdown(self, game_state):
        pass

