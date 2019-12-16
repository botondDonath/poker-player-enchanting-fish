
class Player:
    VERSION = "1.0"

    def get_round_status(self, community_cards):
        round_status_dict = {
            0: 'preflop',
            3: 'flop',
            4: 'turn',
            5: 'river'
        }

        return round_status_dict[len(community_cards)]

    def is_higher_than(self, card, rank):
        ranks = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
        rank_dict = {}
        i = 1
        for rank_ in ranks:
            rank_dict[rank_] = i
            i += 1
        return rank_dict[card['rank']] > rank_dict[rank]

    def betRequest(self, game_state):
        player_index = game_state['in_action']
        players = game_state['players']
        player_count = len(players)
        player = players[player_index]
        card1, card2 = player['hole_cards']

        community_cards = game_state['community_cards']
        min_raise = game_state['minimum_raise']

        current_buy_in = game_state['current_buy_in']
        our_bet = players[player_index]['bet']





        CALL = current_buy_in - our_bet
        MIN_RAISE = current_buy_in - our_bet + min_raise
        round_status = self.get_round_status(community_cards)

        high_cards = card1['rank'] in ('J', 'K', 'Q', 'A') and card2['rank'] in ('J', 'K', 'Q', 'A')

        pair_in_hand = card1['rank'] == card2['rank']
        match_count = 1 if pair_in_hand else 0
        for card in community_cards:
            if card['rank'] in (card1['rank'], card2['rank']):
                match_count += 1
        if round_status == 'preflop':
            if high_cards or (match_count and self.is_higher_than(card1, '6')):
                return "MIN_RAISE"
            else:
                return 0

        else:
            if match_count > 1:
                return MIN_RAISE
            elif match_count == 1:
                return CALL
            elif self.check_suite(card1, card2, community_cards) > 4:
                return player['stack']
            return 0

    def check_suite(self, card1, card2, community_cards):
        same_suite = card1['suite'] if card1['suite'] == card2['suite'] else None

        same_suite_nr = 2 if same_suite else 0

        for card in community_cards:
            if card['suite'] == same_suite:
                same_suite_nr += 1

        return same_suite_nr

    def showdown(self, game_state):
        pass

