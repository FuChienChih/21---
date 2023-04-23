import random

# 定義卡牌類別
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.values = {
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5,
            "Six": 6,
            "Seven": 7,
            "Eight": 8,
            "Nine": 9,
            "Ten": 10,
            "Jack": 10,
            "Queen": 10,
            "King": 10,
            "Ace": 11,
        }
        self.value = self.values[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"


# 定義卡牌組類別
class Deck:
    def __init__(self):
        self.cards = []
        self.suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        self.ranks = [
            "Two",
            "Three",
            "Four",
            "Five",
            "Six",
            "Seven",
            "Eight",
            "Nine",
            "Ten",
            "Jack",
            "Queen",
            "King",
            "Ace",
        ]
        for suit in self.suits:
            for rank in self.ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()


# 定義手牌類別
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.value
        if card.rank == "Ace":
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


# 定義玩家類別
class Player:
    def __init__(self, name):
        self.name = name
        self.chips = 100
        self.hand = Hand()

    def bet(self):
        while True:
            try:
                bet = int(input("您想要下注多少籌碼? "))
            except ValueError:
                print("抱歉，請輸入大於零的正整數")
            else:
                if bet > self.chips:
                    print(f"抱歉，您沒有足夠的籌碼，您得籌碼數為：{self.chips}.")
                if bet < 0:
                    print("抱歉，請輸入大於零的正整數")
                else:
                    self.chips -= bet
                    return bet

    def hit(self, deck):
        self.hand.add_card(deck.deal())
        self.hand.adjust_for_ace()

    def hit_or_stand(self, deck, basic_strategy):
        print(f"{self.name}的手牌: ")
        for card in self.hand.cards:
            print(card)
        print(f"點數: {self.hand.value}")

        print("hit or stand? Enter 'h' or 's':")
        print(basic_strategy)
        choice = basic_strategy

        if choice == "h":
            self.hit(deck)
            print('翻到',self.hand.cards[-1].value)
            print('總點數',self.hand.value)
        elif choice == "s":
            print(f"{self.name} 停牌.")
        else:
            print("Please enter 'h' or 's'.")


# 定義莊家類別
class Dealer:
    def __init__(self):
        self.name = "Dealer"
        self.hand = Hand()

    def play(self, deck):
        while self.hand.value < 17:
            self.hit(deck)
        print("莊家停牌.")

    def hit(self, deck):
        self.hand.add_card(deck.deal())
        self.hand.adjust_for_ace()
        print("莊家翻到",self.hand.cards[-1].value)
        print("莊家點數",self.hand.value)


# 定義玩家勝利函數
def player_wins(player, bet):
    player.chips += bet * 2
    print(f"{player.name} wins {bet} 籌碼!")


# 定義玩家失敗函數
def player_loses(player, bet):
    print(f"{player.name} loses {bet} 籌碼.")


# 定義平局函數
def tie(player, bet):
    player.chips += bet
    print("It's a tie!")


# 基本策略表
def basic_strategy(player_hand, dealer_card):
    if player_hand <= 8:
        return "h"
    elif player_hand >= 9 and player_hand <= 11:
        if dealer_card >= 2 and dealer_card <= 9:
            return "h"
        else:
            return "s"
    elif player_hand == 12:
        if dealer_card >= 2 and dealer_card <= 6:
            return "s"
        else:
            return "h"
    elif player_hand >= 13 and player_hand <= 16:
        if dealer_card >= 2 and dealer_card <= 6:
            return "s"
        else:
            return "h"
    else:
        return "s"


# 定義遊戲函數
def blackjack():
    print("Welcome to Blackjack!\n")
    # 創建新牌組並洗牌
    deck = Deck()
    deck.shuffle()
    # 創建玩家與莊家
    player = Player("Player")
    dealer = Dealer()

    # 遊戲迴圈
    while True:
        # 玩家下注
        bet = player.bet()
        if bet == 0:
            break
        # 發牌
        player.hand.add_card(deck.deal())
        dealer.hand.add_card(deck.deal())
        player.hand.add_card(deck.deal())
        dealer.hand.add_card(deck.deal())

        # 顯示牌面
        print("莊家明牌", dealer.hand.cards[1])

        # 玩家回合 使用基本策略，根據手牌與莊家名牌決定s or h
        while True:
            advisor = basic_strategy(
                player.hand.value, dealer.hand.cards[1].value
            )
            player.hit_or_stand(deck, advisor)
            if advisor == "s" or player.hand.value >= 21:
                break

        # 莊家回合
        if player.hand.value <= 21:
            dealer.play(deck)

            # 判斷勝負
            if dealer.hand.value > 21:
                player_wins(player, bet)
            elif dealer.hand.value < player.hand.value:
                player_wins(player, bet)
            elif dealer.hand.value > player.hand.value:
                player_loses(player, bet)
            else:
                tie(player, bet)
        # else:

        # 顯示結果
        print("莊家手牌:")
        for card in dealer.hand.cards:
            print(card)
        print(f"總點數: {dealer.hand.value}\n")

        # 顯示最終結果
        # print(f"{player.name} 贏的籌碼: {player.chips}")
        print(f"{player.name} 剩餘的籌碼: {player.chips}")
        player.hand = Hand()
        dealer.hand = Hand()


if __name__ == "__main__":
    blackjack()
