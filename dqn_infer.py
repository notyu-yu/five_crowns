import torch
import numpy as np
from deck import Card
from dqn import DQN


def card_to_idx(suit, rank):
    suit_dict = {
        'Clubs': 0,
        'Diamonds': 1,
        'Hearts': 2,
        'Spades': 3,
        'Stars': 4,
        'J': 5
    }

    return 11 * suit_dict[suit] + (rank if suit != "J" else 0) - 3


def idx_to_card(idx):
    suit_dict = {
        0: 'Clubs',
        1: 'Diamonds',
        2: 'Hearts',
        3: 'Spades',
        4: 'Stars',
        5: 'J'
    }

    suit = suit_dict[idx // 11]
    if suit == "J":
        rank = 50
    else:
        rank = (idx % 11) + 3

    return Card(rank, suit)


def encode_state(num_players, full_deck, player_deck, discard_card, gone_out_status):
    num_players = num_players

    deck = set(full_deck)

    encoded_deck = np.zeros(len(deck))
    for idx, card in enumerate(player_deck):
        card_idx = card_to_idx(card.suit(), card.rank())
        encoded_deck[card_idx] += 1

    # Encode discard card as (rank, suit)
    discard_card_encoded = np.zeros(len(deck))
    if discard_card is not None:
        discard_idx = card_to_idx(discard_card.suit(), discard_card.rank())
        discard_card_encoded[discard_idx] = 1

    # Gone out status
    gone_out_status_encoded = int(gone_out_status)

    return np.concatenate([
        encoded_deck,
        discard_card_encoded,
        [gone_out_status_encoded]
    ])


def inference(game, hand, discard_card, policy_net):
    encoded_state = encode_state(game.num_players(
    ), game.get_full_deck()._cards, hand, discard_card, game._go_out)

    with torch.no_grad():
        device = torch.device("mps" if torch.backends.mps.is_available(
        ) else "cuda" if torch.cuda.is_available() else "cpu")
        output = policy_net(torch.Tensor(
            encoded_state).to(device)).to("cpu").numpy()

        sorted_list = [(output[i], idx_to_card(i)) for i in range(len(output))]
        sorted_list.sort(key=lambda x: x[0], reverse=True)

        for _, card in sorted_list:
            if card in hand and card != discard_card:
                return card
