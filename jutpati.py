import sys

import numpy as np
from termcolor import colored


def create_card_deck():
    card_values = np.repeat(np.arange(1, 14), 4)
    card_suites = np.tile(np.arange(1, 5), 13)
    deck = np.column_stack([card_suites, card_values])
    return deck


def serve_cards(player=2, cards=5):
    global global_joker
    card_list = np.arange(0, cards)  # to remove number of cards after serving to player
    deck = create_card_deck()
    deck = deck.reshape((52, 2))
    np.random.shuffle(deck)
    players = {}
    served_deck = {}
    for p in range(player):
        players[p+1] = deck[:cards]
        deck = np.delete(deck, card_list, axis=0)
    served_deck['players'] = players
    served_deck['joker'] = deck[:1]
    global_joker = served_deck['joker']
    deck = np.delete(deck, 0, axis=0)
    served_deck['deck'] = deck
    return served_deck


def check_cards(cards, jokers):
    card = cards[:, 1]
    joker = jokers[:, 1]

    # card = np.array([1, 2, 4, 4, 3, 13])
    # joker = np.array([13])

    no_of_cards = len(card)  # 5 , 7 ?

    joker_count = len(np.where(card == joker)[0])  # How many joker you got?

    card = np.delete(card, np.where(card == joker)[0])  # Cards removing Joker.

    pairs = 0  # Lots of bullshit to find pair.
    thrice = 0
    for c in card:
        is_pair = np.where(card == c)[0]
        if len(is_pair) == 2:
            pairs += 1
        if len(is_pair) == 3:
            thrice += 1
        if len(is_pair) == 4:
            pairs += 1

    pair = int(pairs / 2 + thrice / 3)  # To here.
    if (joker_count + pair)*2 == no_of_cards:  # Game finished condition.
        return 0
    return 1


def pick_from_deck(deck, player_cards):
    picked = deck[:1]
    player_cards = np.append(player_cards, picked, axis=0)
    deck = np.delete(deck, 0, axis=0)
    print(colored(" Computer You picked from Deck ", 'cyan'))
    return deck, player_cards


def pick_card(player_cards, thrown_card, deck):
    cards = player_cards[:, 1]
    if len(thrown_card) > 0:
        if global_joker[:,1] == thrown_card[1]:
            player_cards = np.append(player_cards, [thrown_card], axis=0)
            print(colored('Computer Picked Joker', 'cyan'))
            return deck, player_cards

        thrown = thrown_card[1]
        if_exist = np.where(cards == [thrown])[0]

        if len(if_exist) == 1 or len(if_exist) == 3:
            player_cards = np.append(player_cards, [thrown_card], axis=0)
            print(colored('Computer Picked Thrown Card', 'cyan'))
        else:
            deck, player_cards = pick_from_deck(deck, player_cards)

    else:
        deck, player_cards = pick_from_deck(deck, player_cards)
    return deck, player_cards


def throw_card(player_cards, throw_cards):
    throw = 1

    for c in player_cards:
        is_pair = np.where(player_cards == c)[0]

    return throw - 1


def play_game():
    served = serve_cards()
    deck = served['deck']
    players = served['players']
    joker = served['joker']
    thrown_cards = [[0, 0]]
    thrown_cards = np.array(thrown_cards)
    thrown_card = []
    player_turn = 1
    finished = 1

    while finished:
        print('-------------------------------------------')
        print(colored('Player ' + str(player_turn) + ' Turn:\n', 'blue'))
        print(colored('Joker:' + str(joker), 'green'))
        print('-------------------------------------------')
        print('P' + str(player_turn) + ": You Have \n", players[player_turn])
        print('-------------------------------------------')

        if player_turn == 2:
            deck, players[player_turn] = pick_card(players[player_turn], thrown_card, deck)
        else:
            pick = input('P' + str(player_turn) + ': [Pick] Deck=>1, Thrown=>2 :- ')

            if int(pick) == 1:
                picked = deck[:1]
                players[player_turn] = np.append(players[player_turn], picked, axis=0)
                deck = np.delete(deck, 0, axis=0)
                print(colored('P' + str(player_turn) + ": !You picked from Deck " + str(picked), 'cyan'))
            else:
                if len(thrown_card) > 0:

                    print(players[player_turn])
                    players[player_turn] = np.append(players[player_turn], [thrown_card], axis=0)
                    print('Thron Card ==> ', players[player_turn])
                    print(colored('P' + str(player_turn) + ": !You picked Thrown Card " + str(thrown_card), 'cyan'))
                else:
                    picked = deck[:1]
                    players[player_turn] = np.append(players[player_turn], picked, axis=0)
                    deck = np.delete(deck, 0, axis=0)
                    print('P', str(player_turn), ":! No Thrown Card !\nYou picked from Deck:", picked)
                    print(colored('P' + str(player_turn) + ":! No Thrown Card !\n !You picked from Deck " + str(picked),
                                  'cyan'))

        finished = check_cards(players[player_turn], joker)

        if finished == 0:
            print('!! Player', str(player_turn), " Won !! \n", players[player_turn], '\n Joker: ', joker)
            exit()

        print('-------------------------------------------')
        print('P' + str(player_turn) + ": You Have \n", players[player_turn])
        print(colored('Joker:' + str(joker), 'green'))
        print('-------------------------------------------')

        if player_turn == 2:
            throw = throw_card(players[player_turn], thrown_cards)
        else:
            throw = int(input('P' + str(player_turn) + ': [Throw] :- ')) - 1
        thrown_card = players[player_turn][throw]

        thrown_cards = np.append(thrown_cards, [thrown_card], axis=0)
        thrown_cards = np.delete(thrown_cards, 0, axis=0)

        players[player_turn] = np.delete(players[player_turn], throw, axis=0)
        print(colored('Player' + str(player_turn) + ":! You Threw " + str(thrown_card), 'red'))

        if player_turn == len(players):
            player_turn = 1
            # finished = 0
        else:
            player_turn += 1


if __name__ == "__main__":
    play_game()
