"""
Scoring function for epochs 3 to 5
"""
import itertools as it


def get_best_discard(hand, game, excluded_discard=None):
    """
    Get best discard and its score

    Return card to discard and its score
    """
    best_score = float('inf')
    best_discard = None
    for i, card in enumerate(hand):
        if excluded_discard and card == excluded_discard:
            continue
        score = score_hand(hand[:i] + hand[i+1:], game,
                           keep_wild=(not game.is_going_out()))
        if score < best_score:
            best_score = score
            best_discard = card
    return best_discard, best_score


def scoring_set(hand, game):
    """
    Checks if a set does have 0 score
    """
    wild_card_count = 0
    cards_without_wild = []
    for card in hand:
        if card.suit() == 'J' or card.rank() == game.get_epoch():
            wild_card_count += 1
        else:
            cards_without_wild.append(card)

    # Check if hand is a book
    if len(set([c.rank() for c in cards_without_wild])) == 1:
        return True
    # Check if hand is a run
    if len(set([c.suit() for c in cards_without_wild])) == 1:
        ranks = [c.rank() for c in cards_without_wild]
        # Same suit: Check if max-min = hand size - 1
        if max(ranks) - min(ranks) == len(hand)-1:
            # Check if wild cards + non-wild cards form a run
            if len(set(ranks)) + wild_card_count == len(hand):
                return True
    return False


def score_hand(hand, game, keep_wild=False):
    """
    Get lowest score of a hand for epochs 3 to 5

    hand - set of cards in hand
    game - a five crowns game object

    Returns lowest score for hand
    """
    def score_card(card):
        if keep_wild:
            if card.suit() == 'J' or card.rank() == game.get_epoch():
                return 0
        return game.card_value(card)

    lowest_score = sum(score_card(c) for c in hand)
    # Try every possible scoring subset for best score
    for window_size in range(3, game.get_epoch()+1):
        subsets = it.combinations(hand, window_size)
        for subset in subsets:
            if scoring_set(subset, game):
                # Remove scoring subset
                score = sum(score_card(c) for c in hand if c not in subset)
                if score < lowest_score:
                    lowest_score = score

    return lowest_score
