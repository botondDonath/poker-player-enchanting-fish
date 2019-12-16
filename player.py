
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

    def is_hand_relatively_good(self, card1, card2):
        return self.is_higher_than(card1, '6') and self.is_higher_than(card2, '6')

    def betRequest(self, game_state):
        player_index = game_state['in_action']
        players = game_state['players']
        player_count = len(players)
        active_players = [plyr['name'] if plyr['status'] == 'active' else None for plyr in players]
        player = players[player_index]
        card1, card2 = player['hole_cards']

        community_cards = game_state['community_cards']
        min_raise = game_state['minimum_raise']

        current_buy_in = game_state['current_buy_in']
        our_bet = players[player_index]['bet']

        CALL = current_buy_in - our_bet
        MIN_RAISE = current_buy_in - our_bet + min_raise
        round_status = self.get_round_status(community_cards)
        same_suits_nr = self.check_suit(card1, card2, community_cards)

        high_cards = card1['rank'] in ('J', 'K', 'Q', 'A') and card2['rank'] in ('J', 'K', 'Q', 'A')

        pair_in_hand = card1['rank'] == card2['rank']
        match_count = 1 if pair_in_hand else 0
        for card in community_cards:
            if card['rank'] in (card1['rank'], card2['rank']):
                match_count += 1

        if round_status == 'preflop':
            if match_count and card1['rank'] == 'A':
                return player['stack']
            elif all(player_['id'] < player_index for player_ in players if player_['status'] == 'active') and CALL == 0:
                return MIN_RAISE
            for player_ in players:
                if player_['name'] == 'TwoSeven' and player_['bet'] > 500 and (pair_in_hand or (card1['rank'] in ('J', 'K', 'Q', 'A') or card2['rank'] in ('J', 'K', 'Q', 'A'))):
                    return CALL
            if high_cards or (match_count and self.is_higher_than(card1, '6')):  # if cards are high or high pair
                return MIN_RAISE
            elif self.is_hand_relatively_good(card1, card2):
                return CALL
            else:
                return 0

        else:
            if len(active_players) == 2:
                for player_ in active_players:
                    if player_['name'] == 'TwoSeven' and (
                            pair_in_hand or (card1['rank'] in ('J', 'K', 'Q', 'A') or card2['rank'] in ('J', 'K', 'Q', 'A'))):
                        return CALL
            if game_state['dealer'] == player_index and CALL == 0:
                return MIN_RAISE
            elif all(player_['id'] < player_index for player_ in players if player_['status'] == 'active') and CALL == 0:
                return MIN_RAISE
            elif same_suits_nr == 5:
                return player['stack']
            elif match_count > 1:
                return MIN_RAISE
            elif match_count == 1:
                return CALL
            elif same_suits_nr == 4 and round_status != 'river':
                return CALL
            elif self.check_if_straight(community_cards, card1, card2):
                return MIN_RAISE * 2
            return 0

    def check_suit(self, card1, card2, community_cards):
        same_suite = card1['suit'] if card1['suit'] == card2['suit'] else None

        same_suite_nr = 2 if same_suite else 0

        for card in community_cards:
            if card['suit'] == same_suite:
                same_suite_nr += 1

        return same_suite_nr

    # if "get_round_status" > 0
    def check_if_straight(self, community_cards, card1, card2):
        card_rank_letters_to_numbers = {'J': '11', 'Q': '12', 'K': '13', 'A': '14'}

        # if card['rank'] is a letter, then convert it to number
        card1 = (card_rank_letters_to_numbers[card1['rank']]
                 if card1['rank'] in card_rank_letters_to_numbers
                 else card1['rank'])

        card2 = (card_rank_letters_to_numbers[card2['rank']]
                 if card2['rank'] in card_rank_letters_to_numbers
                 else card2['rank'])
        # add your hand into a card rank list
        cards_rank_list = [int(card1), int(card2)]
        straight = 0

        for card in community_cards:
            # if card['rank'] is a letter, then convert it to number
            card['rank'] = (card_rank_letters_to_numbers[card['rank']]
                            if card['rank'] in card_rank_letters_to_numbers
                            else card['rank'])
            cards_rank_list.append(int(card['rank']))

        cards_rank_list.sort()

        for index, card_rank in enumerate(cards_rank_list):
            if (index + 1) <= len(cards_rank_list) and (cards_rank_list[index + 1] - card_rank) == 1:
                straight += 1
                #if straight is 4 then we have a minimum straight of ranks
                #(because minimum 5 cards is the requirement for the straight)
                if straight == 4:
                    return True
            else:
                return False

    def showdown(self, game_state):
        pass
