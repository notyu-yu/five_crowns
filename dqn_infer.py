import torch
import numpy as np

from deck import Card


def card_to_idx(suit, rank):
    """
    Returns the corresponding index of the card in the encoded state

    Args:
        suit (str): Suit of the card
        rank (int): Rank of the card

    Returns:
        int: Index of the card
    """
    # Dictionary to map suit to index
    suit_dict = {
        "Clubs": 0,
        "Diamonds": 1,
        "Hearts": 2,
        "Spades": 3,
        "Stars": 4,
        "J": 5,
    }

    return 11 * suit_dict[suit] + (rank if suit != "J" else 0) - 3


def idx_to_card(idx):
    """
    Returns the corresponding card of the index in the encoded state

    Args:
        idx (int): Index of the card

    Returns:
        Card: Card corresponding to the index
    """
    # Dictionary to map index to suit
    suit_dict = {
        0: "Clubs",
        1: "Diamonds",
        2: "Hearts",
        3: "Spades",
        4: "Stars",
        5: "J",
    }

    # Calculate rank and suit
    suit = suit_dict[idx // 11]
    if suit == "J":
        rank = 50
    else:
        rank = (idx % 11) + 3

    return Card(rank, suit)


def encode_state(num_players, full_deck, player_deck, discard_card, gone_out_status):
    """
    Encodes the state of the game into a numpy array

    Args:
        num_players (int): Number of players in the game
        full_deck (list): List of all cards in the deck
        player_deck (list): List of cards in the player's hand
        discard_card (Card): Card in the discard pile
        gone_out_status (bool): Whether the player has gone out

    Returns:
        np.array: Encoded state of the game
    """
    # Get the unique set of cards in the deck
    deck = set(full_deck)

    # Encode player's hand
    encoded_deck = np.zeros(len(deck))
    for card in player_deck:
        card_idx = card_to_idx(card.suit(), card.rank())
        encoded_deck[card_idx] += 1

    # Encode discard card
    discard_card_encoded = np.zeros(len(deck))
    if discard_card is not None:
        discard_idx = card_to_idx(discard_card.suit(), discard_card.rank())
        discard_card_encoded[discard_idx] = 1

    # Encode gone out status
    gone_out_status_encoded = int(gone_out_status)

    return np.concatenate(
        [encoded_deck, discard_card_encoded, [gone_out_status_encoded]]
    )


def inference(game, hand, discard_card, policy_net):
    """
    Inference function for the DQN player

    Args:
        game (Game): Game object
        hand (list): List of cards in the player's hand
        discard_card (Card): Card in the discard pile
        policy_net (nn.Module): Policy network for the DQN player

    Returns:
        Card: Card to be discarded
    """
    # Encode the state of the game
    encoded_state = encode_state(
        game.num_players(),
        game.get_full_deck()._cards,
        hand,
        discard_card,
        game._go_out,
    )

    # Perform inference
    with torch.no_grad():
        output = policy_net(torch.Tensor(encoded_state).to("cuda")).to("cpu").numpy()

        # Sort the output by probability
        sorted_list = [(output[i], idx_to_card(i)) for i in range(len(output))]
        sorted_list.sort(key=lambda x: x[0], reverse=True)

        # Choose the card with the highest probability that is not the discard card
        for _, card in sorted_list:
            if card in hand and card != discard_card:
                return card
