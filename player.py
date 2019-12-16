
class Player:
    VERSION = "1.0"

    def betRequest(self, game_state):
        player_index = game_state['in_action']
        players = game_state['players']
        player = players[player_index]
        card1, card2 = player['hole_cards']

        community_cards = game_state['community_cards']
        min_raise = game_state['minimum_raise']

        current_buy_in = game_state['current_buy_in']
        our_bet = players[player_index]['bet']

        pair_in_hand = card1['rank'] == card2['rank']
        match_count = 1 if pair_in_hand else 0
        if community_cards:
            for card in community_cards:
                if card['rank'] in (card1['rank'], card2['rank']):
                    match_count += 1

        if not community_cards:
            if (
                    card1['rank'] in ('J', 'K', 'Q', 'A') and card2['rank'] in ('J', 'K', 'Q', 'A')
            ) or (
                    match_count and card1['rank'] not in (str(i) for i in range(1, 7))
            ):
                return current_buy_in - our_bet + min_raise

            else:
                return 0

        else:
            return current_buy_in - our_bet

    def showdown(self, game_state):
        pass

