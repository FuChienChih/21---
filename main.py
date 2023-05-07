import random
import pandas as pd
import time


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
        self.is_split = False

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
        self.bet = 30
        self.double = False
        self.name = name
        self.chips = 10000
        self.hand = Hand()
    def mat(self,len_cards,count ):
        truth = count / (len_cards / 52)
        return truth

    def place＿bet(self, len_cards, count):
        truth = self.mat(len_cards,count)
        if truth > 2:
            bet = 20
        else:
            bet = 0
        return bet


    def hit(self, deck):
        self.hand.add_card(deck.deal())
        self.hand.adjust_for_ace()


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
        # print("莊家翻到", self.hand.cards[-1].value)
        # print("莊家點數", self.hand.value)



# 基本策略表
def basic_strategy(player_hand, dealer_card,truth):
    if len(player_hand.cards) == 1 :
        if player_hand.cards[0].rank == "Ace":
            return "HS"
        else:
            return "H"
    # 分牌區
    if player_hand.cards[0].rank == player_hand.cards[1].rank and  len(player_hand.cards)==2:
        if player_hand.cards[0].rank == "Ace" or player_hand.cards[0].rank == "Eight":
            return "SP"
        elif (player_hand.cards[0].rank == "Two" or player_hand.cards[0].rank == "Three") and dealer_card <= 7:
            return "SP"
        elif player_hand.cards[0].rank == "Six" and dealer_card >=5 and dealer_card<=6:
            return "SP"
        elif player_hand.cards[0].rank == "Four" and dealer_card <= 6:
            return "SP"
        elif player_hand.cards[0].rank == "Seven" and dealer_card <= 7:
            return "SP"
        elif player_hand.cards[0].rank == "Nine" and (dealer_card <= 6 or (dealer_card >=8 and dealer_card<=9)):
            return "SP"
    # 玩家手牌有A
    strategy = {
        (4, 2): "H",
        (4, 3): "H",
        (4, 4): "H",
        (4, 5): "H",
        (4, 6): "H",
        (4, 7): "H",
        (4, 8): "H",
        (4, 9): "H",
        (4, 10): "H",
        (4, 11): "H",
        (5, 2): "H",
        (5, 3): "H",
        (5, 4): "H",
        (5, 5): "H",
        (5, 6): "H",
        (5, 7): "H",
        (5, 8): "H",
        (5, 9): "H",
        (5, 10): "H",
        (5, 11): "H",
        (6, 2): "H",
        (6, 3): "H",
        (6, 4): "H",
        (6, 5): "H",
        (6, 6): "H",
        (6, 7): "H",
        (6, 8): "H",
        (6, 9): "H",
        (6, 10): "H",
        (6, 11): "H",
        (7, 2): "H",
        (7, 3): "H",
        (7, 4): "H",
        (7, 5): "H",
        (7, 6): "H",
        (7, 7): "H",
        (7, 8): "H",
        (7, 9): "H",
        (7, 10): "H",
        (7, 11): "H",
        (8, 2): "H",
        (8, 3): "H",
        (8, 4): "H",
        (8, 5): "D",
        (8, 6): "D",
        (8, 7): "H",
        (8, 8): "H",
        (8, 9): "H",
        (8, 10): "H",
        (8, 11): "H",
        (9, 2): "H",
        (9, 3): "D",
        (9, 4): "D",
        (9, 5): "D",
        (9, 6): "D",
        (9, 7): "H",
        (9, 8): "H",
        (9, 9): "H",
        (9, 10): "H",
        (9, 11): "H",
        (10, 2): "D",
        (10, 3): "D",
        (10, 4): "D",
        (10, 5): "D",
        (10, 6): "D",
        (10, 7): "D",
        (10, 8): "D",
        (10, 9): "D",
        (10, 10): "H",
        (10, 11): "H",
        (11, 2): "D",
        (11, 3): "D",
        (11, 4): "D",
        (11, 5): "D",
        (11, 6): "D",
        (11, 7): "D",
        (11, 8): "D",
        (11, 9): "D",
        (11, 10): "D",
        (11, 11): "H",
        (12, 2): "H",
        (12, 3): "H",
        (12, 4): "S",
        (12, 5): "S",
        (12, 6): "S",
        (12, 7): "H",
        (12, 8): "H",
        (12, 9): "H",
        (12, 10): "H",
        (12, 11): "H",
        (13, 2): "S",
        (13, 3): "S",
        (13, 4): "S",
        (13, 5): "S",
        (13, 6): "S",
        (13, 7): "H",
        (13, 8): "H",
        (13, 9): "H",
        (13, 10): "H",
        (13, 11): "H",
        (14, 2): "S",
        (14, 3): "S",
        (14, 4): "S",
        (14, 5): "S",
        (14, 6): "S",
        (14, 7): "H",
        (14, 8): "H",
        (14, 9): "H",
        (14, 10): "H",
        (14, 11): "H",
        (15, 2): "S",
        (15, 3): "S",
        (15, 4): "S",
        (15, 5): "S",
        (15, 6): "S",
        (15, 7): "H",
        (15, 8): "H",
        (15, 9): "H",
        (15, 10): "H",
        (15, 11): "H",
        (16, 2): "S",
        (16, 3): "S",
        (16, 4): "S",
        (16, 5): "S",
        (16, 6): "S",
        (16, 7): "H",
        (16, 8): "H",
        (16, 9): "H",
        (16, 10): "H",
        (16, 11): "H",
        (17, 2): "S",
        (17, 3): "S",
        (17, 4): "S",
        (17, 5): "S",
        (17, 6): "S",
        (17, 7): "S",
        (17, 8): "S",
        (17, 9): "S",
        (17, 10): "S",
        (17, 11): "S",
        (18, 2): "S",
        (18, 3): "S",
        (18, 4): "S",
        (18, 5): "S",
        (18, 6): "S",
        (18, 7): "S",
        (18, 8): "S",
        (18, 9): "S",
        (18, 10): "S",
        (18, 11): "S",
        (19, 2): "S",
        (19, 3): "S",
        (19, 4): "S",
        (19, 5): "S",
        (19, 6): "S",
        (19, 7): "S",
        (19, 8): "S",
        (19, 9): "S",
        (19, 10): "S",
        (19, 11): "S",
        (20, 2): "S",
        (20, 3): "S",
        (20, 4): "S",
        (20, 5): "S",
        (20, 6): "S",
        (20, 7): "S",
        (20, 8): "S",
        (20, 9): "S",
        (20, 10): "S",
        (20, 11): "S",
        (21, 2): "S",
        (21, 3): "S",
        (21, 4): "S",
        (21, 5): "S",
        (21, 6): "S",
        (21, 7): "S",
        (21, 8): "S",
        (21, 9): "S",
        (21, 10): "S",
        (21, 11): "S",
    }
    # 當起手牌有A
    if (player_hand.cards[0].rank == "Ace"or player_hand.cards[1].rank == "Ace") and len(player_hand.cards) == 2:
        strategy[(18,2)] = "D"
        strategy[(18,3)] = "D"
        strategy[(18,4)] = "D"
        strategy[(18,5)] = "D"
        strategy[(18,6)] = "D"
        strategy[(17,3)] = "D"
        strategy[(17,4)] = "D"
        strategy[(17,5)] = "D"
        strategy[(17,6)] = "D"
        strategy[(16,4)] = "D"
        strategy[(16,5)] = "D"
        strategy[(16,6)] = "D"
        strategy[(15,4)] = "D"
        strategy[(15,5)] = "D"
        strategy[(15,6)] = "D"
        strategy[(14,6)] = "D"
        strategy[(14,5)] = "D"
        strategy[(13,6)] = "D"
        strategy[(13,5)] = "D"
    # 當真數>0
    if truth > 0:
        strategy[(16,10)] = "S"
    if  truth > 1:
        if (player_hand.cards[0].rank == "Ace"or player_hand.cards[1].rank == "Ace") and len(player_hand.cards) == 2:
            strategy[(19,5)] = "D"
            strategy[(19,6)] = "D"
            strategy[(17,2)] = "D"
        strategy[(11,11)] = "D"
        strategy[(9,2)] = "D"
    strategy[(9,2)] = "D"
    if  truth > 2:
        strategy[(12,6)] = "S"
        strategy[(8,6)] = "D"
    if  truth > 3:
        if (player_hand.cards[0].rank == "Ace"or player_hand.cards[1].rank == "Ace") and len(player_hand.cards) == 2:
            strategy[(19,4)] = "D"
        strategy[(12,2)] = "S"
        strategy[(9,7)] = "D"
    if  truth > 4:
        strategy[(16,9)] = "S"
        strategy[(15,10)] = "S"
        strategy[(10,10)] = "D"
    
    try :
        return strategy[(player_hand.value,dealer_card)]
    except:
        return "S"


# 定義遊戲函數
def blackjack(cycle=1):
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
    player1_hand,player2_hand,player3_hand,player4_hand,player5_hand = [],[],[],[],[]
    player6_hand,player7_hand,player8_hand,player9_hand = [],[],[],[]
    total_chips,dealer_visible,dealer_hand,truths = [],[],[],[]
    total_rounds = 0
    Top ,Bottom = 10000,10000
    sum_ = 0
    total_bets = 0
    # 遊戲迴圈
    
    while total_bets < 22400:
        total_rounds+=1
        # 如果牌組卡數低於一定值，重新洗牌
        if len(deck.cards) < 52 * 5:
            print("=================重新洗牌=================")
            deck = Deck()
            deck.shuffle()
            count = 0
        # 真數
        truth = count / (len(deck.cards) / 52)
        if truth > 2:
            truths.append(truth)
            # 開5家
            sum_ += 1
        # 玩家下注
        players = [player1, player2, player3, player4, player5]
        for player in players:
            player.hand = Hand()
            player.bet = player.place＿bet(len(deck.cards), count)

        dealer.hand = Hand()
        
        # 發牌
        for i in range(2):
            for player in players:
                player.hit(deck)
                count += check_count(player.hand.cards[-1].value)
            dealer.hit(deck)
            count += check_count(dealer.hand.cards[-1].value)
        
            
        # 玩家回合 使用基本策略，根據手牌與莊家名牌決定s or h
        r = 6
        for player in players:
            # 如果player是分牌Ａ跳過player
            while True:
                advisor = basic_strategy(
                    player.hand, dealer.hand.cards[1].value,truth
                )   
                if advisor == "S":
                    break
                # ＡＡ分牌
                elif advisor == "HS":
                    player.hit(deck)
                    count += check_count(player.hand.cards[-1].value)
                    break
                elif advisor == "D":
                    player.hit(deck)
                    count += check_count(player.hand.cards[-1].value)
                    player.bet*=2
                    player.double = True
                    break
                elif advisor == "H":
                    player.hit(deck)
                    count += check_count(player.hand.cards[-1].value)
                elif advisor == "SP":
                    exec(f"player{r}=Player(player.name)")
                    exec(f"players.append(player{r})")
                    card = player.hand.cards.pop()
                    exec(f"player{r}.hand.add_card(card)")
                    exec(f"player{r}.bet = player.bet")
                    r+=1
        # 莊家回合
        while True :
            if  dealer.hand.value < 17  :
                dealer.hit(deck)
                count += check_count(dealer.hand.cards[-1].value)
            else :
                break
        # 如果真數 < 2不紀錄
        if player1.bet == 0:
            continue
        
        # 判斷勝負/分配籌碼
        for player in players:
            total_bets += player.bet
            if player.hand.value <= 21:
                # 天生21點
                if player.hand.value == 21 and len(player.hand.cards) == 2:
                    if dealer.hand.value == 21 and len(player.hand.cards) == 2:
                        pass 
                    else:
                        player.chips += player.bet * 1.5
                # 莊家爆牌
                elif dealer.hand.value > 21:
                    player.chips += player.bet
                # 莊家輸
                elif dealer.hand.value < player.hand.value:
                    player.chips += player.bet
                # 莊家贏
                elif dealer.hand.value > player.hand.value:
                    player.chips -= player.bet
                # 平手
                else:
                    if dealer.hand.value == 21 and len(player.hand.cards) == 2:
                        player.chips -= player.bet
            else:
                player.chips -= player.bet
        
        # 將分牌後輸贏的籌碼加回本人
        for player_ in players[6:]:
            if player_.name == "Player1":
                player1.chips += player_.chips-10000
            elif player_.name == "Player2":
                player2.chips += player_.chips-10000
            elif player_.name == "Player3":
                player3.chips += player_.chips-10000
            elif player_.name == "Player4":
                player4.chips += player_.chips-10000
            elif player_.name == "Player5":
                player5.chips += player_.chips-10000
            
        

        # 顯示最終結果
        chips = player1.chips+player2.chips+player3.chips+player4.chips+player5.chips-40000
        total_chips.append(chips)
        dealer_visible.append(dealer.hand.cards[1].value)
        player1_hand.append([i.value for i in player1.hand.cards])
        player2_hand.append([i.value for i in player2.hand.cards])
        player3_hand.append([i.value for i in player3.hand.cards])
        player4_hand.append([i.value for i in player4.hand.cards])
        player5_hand.append([i.value for i in player5.hand.cards])
        dealer_hand.append([i.value for i in dealer.hand.cards])
        # r 用來計算要加在
        r = 5
        for player_ in (players+[None,None,None,None,None])[5:10]:
            if player_ == None:
                break
            if r == 5:
                player6_hand.append([i.value for i in players[r].hand.cards])
                r+=1
            elif r == 6:
                player7_hand.append([i.value for i in players[r].hand.cards])
                r+=1
            elif r == 7:
                player8_hand.append([i.value for i in players[r].hand.cards])
                r+=1
            elif r == 8:
                player9_hand.append([i.value for i in players[r].hand.cards])
                r+=1
        # 如果沒有分牌，則紀錄None
        for i in [player6_hand,player7_hand,player8_hand,player9_hand]:
            if len(i)<len(player1_hand):
                i.append(None)

        # 將分牌所產生的牌桌清空
        players = players[:5]
        # 
        if chips > Top:
            Top = chips
        if chips < Bottom:
            Bottom = chips

    
    df = pd.DataFrame({'total_chips' : total_chips,
                        '真數': truths,
                        'dealer_visible':dealer_visible,
                        'player1_hand':player1_hand,
                        'player2_hand':player2_hand,
                        'player3_hand':player3_hand,
                        'player4_hand':player4_hand,
                        'player5_hand':player5_hand,
                        'player6_hand':player6_hand,
                        'player7_hand':player7_hand,
                        'player8_hand':player8_hand,
                        'player9_hand':player9_hand,
                        'dealer_hand':dealer_hand,
                        })
    desktop_path = '/Users/fuqianzhi/Desktop/21點專案/每回合詳細資料/'  # 桌面路径
    file_name = f'{cycle}data.csv'    # 文件名
    file_path = desktop_path + file_name  # 文件路径
    df.to_csv(file_path, index=False)
    
    return chips,Top,Bottom


def check_count(card_value):
    if card_value in [2, 3, 4, 5, 6]:
        return 1
    elif card_value in [7, 8, 9]:
        return 0
    else:
        return -1


if __name__ == "__main__":
    # blackjack函式會根據流水決定玩幾手。result會記錄結束後剩餘的籌碼量
    results = []
    # cycle 代表要模擬的週期數
    cycle = 500
    # 每個cycle中，贏到最多的籌碼與輸到最多的籌碼量
    Top,Bottom = [],[]

    for i in range(cycle):
        start_time = time.time()    
        result,top,bottom = blackjack(i+1)
        results.append(result)
        Top.append(top)
        Bottom.append(bottom)
        end_time = time.time()
    df = pd.DataFrame({'chips': results,
                        'Top':Top,
                        'Bottom':Bottom,
                        })
    df.to_csv("/Users/fuqianzhi/Desktop/21點專案/data.csv", index=False)

# if __name__ == "__main__":
#     start_time = time.time()
#     chips = []
#     for i in range(200):
#         chips.append(blackjack())
#     mean, std = np.mean(chips), np.std(chips)
    

#     # 繪製常態分佈的曲線
#     count, bins, ignored = plt.hist(chips, 30, density=True)
#     plt.plot(bins, 1/(std * np.sqrt(2 * np.pi)) * np.exp(-(bins - mean)**2 / (2 * std**2)), linewidth=2, color='r')
#     # 顯示平均值、標準差
#     plt.axvline(mean, color='green', linestyle='dashed', linewidth=2)
#     plt.axvline(mean + std, color='orange', linestyle='dashed', linewidth=2)
#     plt.axvline(mean - std, color='orange', linestyle='dashed', linewidth=2)

#     # 顯示信賴區間
#     confidence_interval = stats.norm.interval(0.95, loc=mean, scale=std/np.sqrt(len(chips)))
#     plt.axvline(confidence_interval[0], color='red', linestyle='dashed', linewidth=2)
#     plt.axvline(confidence_interval[1], color='red', linestyle='dashed', linewidth=2)
#     end_time = time.time()
#     print('RunTime:',end_time-start_time)
#     plt.show()


