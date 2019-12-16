
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

        round_status = self.get_round_status(community_cards)

        high_cards = card1['rank'] in ('J', 'K', 'Q', 'A') and card2['rank'] in ('J', 'K', 'Q', 'A')

        if int(self.get_round_status(community_cards)) > 0:
            self.check_if_straight(community_cards, card1, card2)

        pair_in_hand = card1['rank'] == card2['rank']
        match_count = 1 if pair_in_hand else 0
        for card in community_cards:
            if card['rank'] in (card1['rank'], card2['rank']):
                match_count += 1
        if round_status == 'preflop':
            if high_cards or (match_count and card1['rank'] not in (str(i) for i in range(1, 7))):
                return current_buy_in - our_bet + min_raise
            else:
                return 0

        else:
            if match_count > 1:
                return current_buy_in - our_bet + min_raise
            elif match_count == 1:
                return current_buy_in - our_bet
            return 0

    # if "get_round_status" > 0
    def check_if_straight(self, min_raise, community_cards, card1, card2):
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
                    return min_raise * 2
            else:
                return False


    def showdown(self, game_state):
        pass

