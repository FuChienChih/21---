import random
import pandas as pd
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
        for suit in self.suits*8:
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
        self.chips = 10000
        self.hand = Hand()

    def mat(self,len_cards,count ):
        truth = count / (len_cards / 52)
        return truth

    def bet(self, len_cards, count):
        truth = self.mat(len_cards,count)
        if truth > 2:
            bet = 10
        else:
            bet = 10
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
        return choice


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
        print("莊家翻到", self.hand.cards[-1].value)
        print("莊家點數", self.hand.value)


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
    desktop_path = '/Users/fuqianzhi/Desktop/21點專案'  # 桌面路径
    file_name = '1000data.csv'    # 文件名
    file_path = desktop_path + file_name  # 文件路径
    print("--------------------遊戲開始--------------------")
    print("Welcome to Blackjack!\n")
    # 創建新牌組並洗牌
    deck = Deck()
    deck.shuffle()
    # 創建玩家與莊家
    player1 = Player("Player1")
    player2 = Player("Player2")
    player3 = Player("Player3")
    player4 = Player("Player4")
    player5 = Player("Player5")
    dealer = Dealer()
    count = 0
    win,loss,tie_,sum_ = 0,0,0,0
    # 遊戲迴圈
    truth = []
    win_loss = []
    for i in range(10000):
        # 如果牌組卡數低於一定值，重新洗牌
        if len(deck.cards) < 52 * 3:
            print("\n\n\n\n=================重新洗牌=================")
            deck = Deck()
            deck.shuffle()
            count = 0
        # 真數
        truth.append(count / (len(deck.cards) / 52))
        # 玩家下注
        players = [player1, player2, player3, player4, player5]
        for player in players:
            bet = player.bet(len(deck.cards), count)
        
        # 發牌
        for i in range(2):
            for player in players:
                card = deck.deal()
                player.hand.add_card(card)
                count += check_count(card.value)
            card = deck.deal()
            dealer.hand.add_card(card)
            count += check_count(card.value)
        # if bet == 0:
        #     continue
        else :
            sum_ += 1
        # 顯示牌面
        print("莊家明牌", dealer.hand.cards[1])
        print("player1點數", player1.hand.value)
        # 玩家回合 使用基本策略，根據手牌與莊家名牌決定s or h
        for player in players:
            while True:
                advisor = basic_strategy(
                    player.hand.value, dealer.hand.cards[1].value
                )   
                if advisor == "s" or player.hand.value >= 21:
                    break
                else :
                    card = deck.deal()
                    player.hand.add_card(card)
                    count += check_count(card.value)
                    if player.name == 'Player1':
                        print('Player1翻到',card.value)

        # 莊家回合
        if  dealer.hand.value < 17  :
            card = deck.deal()
            dealer.hand.add_card(card)
            count += check_count(card.value)

        # 判斷勝負
        if player1.hand.value <= 21:
            if dealer.hand.value > 21:
                player_wins(player1, bet)
                win+=1
                win_loss.append('win')
            elif dealer.hand.value < player1.hand.value:
                player_wins(player1, bet)
                win+=1
                win_loss.append('win')
            elif dealer.hand.value > player1.hand.value:
                player_loses(player1, bet)
                loss+=1
                win_loss.append('loss')
            else:
                tie(player1, bet)
                tie_+=1
                win_loss.append('tie_')
        else:
            player_loses(player1, bet)
            loss+=1
            win_loss.append('loss')
        # 顯示結果
        print("莊家手牌:")
        for card in dealer.hand.cards:
            print(card)
        print(f"總點數: {dealer.hand.value}\n")

        # 顯示最終結果
        print(f"{player1.name} 剩餘的籌碼: {player1.chips}")
        player1.hand = Hand()
        dealer.hand = Hand()
        print("-----------------------------------------")
        print("牌值:", count)
    
    print('籌碼量:',player1.chips)
    print('總遊戲次數:',sum_)
    print('win:',win)
    print('loss:',loss)
    print('tie',tie_)
    df = pd.DataFrame({'真數': truth,
                        '輸贏':win_loss,
                        })
    df.to_csv(file_path, index=False)
    return player1.chips,sum_,win,loss,tie_


def check_count(card_value):
    if card_value in [2, 3, 4, 5, 6]:
        return 1
    elif card_value in [7, 8, 9]:
        return 0
    else:
        return -1

if __name__ == "__main__":
    chips,win,loss,tie_,playtime = [],[],[],[],[]
    blackjack()
    # for i in range(10):
    #     chips.append(blackjack()[0])
    #     win.append(blackjack()[1])
    #     loss.append(blackjack()[2])
    #     tie_.append(blackjack()[3])
    #     playtime.append(blackjack()[4])
    # df = pd.DataFrame({'chips': chips,
    #                     'win':win,
    #                     'loss':loss,
    #                     'tie':tie_,
    #                     'playtime':playtime})
    # desktop_path = '/Users/fuqianzhi/Desktop/21點專案'  # 桌面路径
    # file_name = '1000data.csv'    # 文件名
    # file_path = desktop_path + file_name  # 文件路径
    # df.to_csv(file_path, index=False)
