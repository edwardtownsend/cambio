import random

def create_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    
    point_values = {str(i): i for i in range(2, 11)}
    point_values.update({'J': 10, 'Q': 10, 'A': 1})
    point_values.update({'K Hearts': -2, 'K Diamonds': -2, 'K Clubs': 10, 'K Spades': 10})
    
    deck = [f'{rank} of {suit}' for suit in suits for rank in ranks]
    
    card_points = {}
    for suit in suits:
        for rank in ranks:
            if rank == 'K':
                card_points[f'{rank} of {suit}'] = point_values[f'K {suit}']
            else:
                card_points[f'{rank} of {suit}'] = point_values[rank]
    
    return deck, card_points

def deal_cards(deck, num_players=4, cards_per_player=4):
    random.shuffle(deck)
    hands = {f'Player {i+1}': [deck.pop() for _ in range(cards_per_player)] for i in range(num_players)}
    return hands, deck

def player_turn(player, hands, pile, deck, card_points):
    print(f'\n{player}\'s turn:')
    hand = hands[player]
    
    if input(f'{player}, do you want to call Cambio? (yes/no): ').lower() == 'yes':
        return True
    
    draw_from_pile = False
    if len(pile) > 0:
        draw_from_pile = input(f'{player}, do you want to draw from the pile? (yes/no): ').lower() == 'yes'
    
    if draw_from_pile:
        picked_card = pile.pop()
        print(f'{player} picks up {picked_card} from the pile')
    else:
        picked_card = deck.pop()
        print(f'{player} picks up {picked_card} from the deck')
    
    action = input(f'{player}, do you want to (1) place {picked_card} on the pile or (2) swap it with one of your cards? Enter 1 or 2: ')
    
    if action == '1':
        pile.append(picked_card)
        if picked_card.split(' ')[0] in ['7', '8', '9', '10', 'J', 'Q', 'K']:
            handle_special_card(picked_card, player, hands)

    elif action == '2':
        swap_index = int(input('Enter the number of the card to swap: ')) - 1
        if 0 <= swap_index < len(hand):
            swapped_card = hand[swap_index]
            hand[swap_index] = picked_card
            pile.append(swapped_card)
        else:
            print('Invalid selection. The drawn card goes back to the deck.')
            deck.append(picked_card)
            return

    return False

def handle_special_card(card, player, hands):
    card_rank = card.split(' ')[0]

    if card_rank in ['7', '8']:
        card_number = input(f'Enter the card you want to look at from Player {target_player}\'s hand: ') - 1
        if card_number < len(hands[player]):
            print(hands[player][card_number])
        else:
            print('Invalid card number!')

    elif card_rank in ['9', '10']:
        target_player = input('Enter the player whose hand you want to look at: ')
        if target_player in hands:
            card_number = input(f'Enter the card you want to look at from Player {target_player}\'s hand: ') - 1
            if card_number < len(hands[target_player]):
                print(hands[target_player][card_number])
            else:
                print('Invalid card number!')
        else:
            print('Invalid player number!')

    elif card_rank in ['J', 'Q']:
        target_player = input('Enter the player you want to swap with: ')
        if target_player in hands:
            swap_from_hand = int(input(f'Enter the number of the card from your hand to swap: ')) - 1
            swap_from_target = int(input(f'Enter the number of the card from {target_player}\'s hand to swap: ')) - 1
            if 0 <= swap_from_hand < len(hands[player]) and 0 <= swap_from_target < len(hands[target_player]):
                hand_card = hands[player][swap_from_hand]
                target_card = hands[target_player][swap_from_target]
                hands[player][swap_from_hand] = target_card
                hands[target_player][swap_from_target] = hand_card
            else:
                print('Invalid selection.')
        else:
            print('Invalid player.')

    elif card_rank == 'K':
        if 'Hearts' in card or 'Diamonds' in card:
            print('Red King does not have a special effect, game carries on.')
        else:
            target_player = input('Enter the player whose hand you want to look at: ')
            if target_player in hands:
                card_number = input(f'Enter the card you want to look at from Player {target_player}\'s hand: ') - 1
                if card_number < len(hands[target_player]):
                    print(hands[target_player][card_number])
                else:
                    print('Invalid card number!')
            else:
                print('Invalid player number!')
            
            target_player = input('Enter the player you want to swap with: ')
            if target_player in hands:
                swap_from_hand = int(input(f'Enter the number of the card from your hand to swap: ')) - 1
                swap_from_target = int(input(f'Enter the number of the card from {target_player}\'s hand to swap: ')) - 1
                if 0 <= swap_from_hand < len(hands[player]) and 0 <= swap_from_target < len(hands[target_player]):
                    hand_card = hands[player][swap_from_hand]
                    target_card = hands[target_player][swap_from_target]
                    hands[player][swap_from_hand] = target_card
                    hands[target_player][swap_from_target] = hand_card
                else:
                    print('Invalid selection.')
            else:
                print('Invalid player.')
            
def check_winner(hands, card_points):
    scores = {player: sum(card_points[card] for card in hand) for player, hand in hands.items()}
    winner = min(scores, key=scores.get)
    return winner, scores[winner]

def main():
    num_players = 4
    deck, card_points = create_deck()
    hands, remaining_deck = deal_cards(deck, num_players)
    pile = []
    
    for player, hand in hands.items():
        print(f'First two cards in {player}\'s hand: {hand[:2]}')
    
    cambio_called = None
    
    while True:
        for i in range(num_players):
            player = f'Player {i+1}'
            if cambio_called is None:
                cambio_called = player_turn(player, hands, pile, remaining_deck, card_points)
                if cambio_called:
                    break
        
        if cambio_called:
            print(f'\n{cambio_called} called Cambio!')
            print('\nCompleting round...')
            for j in range(num_players):
                if f'Player {j+1}' != cambio_called:
                    player = f'Player {j+1}'
                    player_turn(player, hands, pile, remaining_deck, card_points)
            break
        
    print('\nRound Ended')
    for player, hand in hands.items():
        print(f'{player}\'s hand: {hand}')
    
    winner, winner_score = check_winner(hands, card_points)
    print(f'\nWinner: {winner} with {winner_score} points')

if __name__ == '__main__':
    main()