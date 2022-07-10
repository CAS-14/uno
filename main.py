import random

powers = ["skip", "reverse", "+2", "+4"]
colors = ["red", "green", "blue", "yellow", "black"]

players = 2
step = True

# represents any Uno card
class Card:
    def __init__(self, color: str, value: int, power: str = None):
        self.color = color
        self.value = value
        self.power = power

    def get(self):
        if self.color == "black":
            if self.power:
                name = "Wild +4"
            else:
                name = "Regular Wild"
        else:
            name = self.color.capitalize() + " "
            if self.power:
                name += self.power.capitalize()
            else:
                name += str(self.value)

        return name

# generates a vanilla ordered Uno deck - shuffle before playing
def generate_deck():
    deck = []

    for ic in range(0, 3):
        color = colors[ic]

        for iv in range(1, 9):
            deck.append(Card(color, iv))
            deck.append(Card(color, iv))

        for ip in range(0, 2):
            deck.append(Card(color, 20, powers[ip]))
            deck.append(Card(color, 20, powers[ip]))

        deck.append(Card(color, 0))

    #for i in range(4):
    #    deck.append(Card("black", 50, "+4"))
    #    deck.append(Card("black", 50))

    return deck

# beginning of list is bottom, end is top - use pop() to take a card and [-1] to see top card
print("Generating deck...")
deck = generate_deck()
for card in deck:
    print(card.get())

print("Shuffling deck...")
random.shuffle(deck)
for card in deck:
    print(card.get())

print("Making discard pile...")
discard = []
discard.append(deck.pop())
print(f"Discard pile is {discard[-1].get()}.")

over = False

# checks if card can be placed on discard pile
def match(card: Card):
    return True if card.color == "black" or card.color == discard[-1].color or card.value == discard[-1].value else False

# represents a player
class Player:
    def __init__(self, name):
        self.name = name

        self.hand = []
        for i in range(7):
            self.draw()

    def draw(self):
        global deck, discard

        if len(deck) < 1:
            print("Deck empty, shuffling discard pile")

            aside = discard.pop()
            random.shuffle(discard)
            deck = discard

            discard = []
            discard.append(aside)

        self.hand.append(deck.pop())
        print(f"{self.name} drew: {self.hand[-1].get()}")

    def put(self, card):
        self.hand.remove(card)
        discard.append(card)

    def get(self):
        if len(self.hand) == 0:
            return("no cards")

        hand = self.hand[0].get()
        for card in self.hand[1:]:
            hand += ", " + card.get()

        return hand

    def uno(self):
        print(f"{self.name}: Uno!")

    def win(self):
        global over
        print(f"{self.name} is out of cards.")
        over = True

    def points(self):
        pts = 0
        for card in self.hand:
            pts += card.value

        return pts

# represents an AI player
class AI(Player):
    def __init__(self, name):
        super().__init__(name)
    
    def go(self):
        if not over:

            print(f"It is {discard[-1].get()} to {self.name}")

            moves = []
            for card in self.hand:
                if match(card):
                    moves.append(card)

            if len(moves) == 0:
                print(f"{self.name} doesn't have any moves and must draw")
                super().draw()
                self.go()

            else:
                print(f"{self.name} has {len(moves)} different moves")

                move = moves[0]
                for card in moves:
                    if card.value > move.value:
                        move = card
                
                super().put(move)
                print(f"{self.name} put down: {move.get()}")
                print(f"{self.name}'s hand: {self.get()}")

                if len(self.hand) == 1:
                    super().uno()
                
                if len(self.hand) == 0:
                    super().win()
                else:
                    if move.power:
                        print(f"Skip! {self.name} is going again")
                        self.go()

        else:

            print(f"Game is over, {self.name} is not going")

players = [AI("Joe"), AI("Bob")]

while not over:
    for p in players:
        print(f"\nIt is {p.name}'s turn")
        print(f"{p.name}'s hand: {p.get()}")

        p.go()

        input("Press enter to continue ") if step else None

for p in players:
    if len(p.hand) == 0:
        winner = p

print(f"{winner.name} has won the game!")
print("Losers:")

for p in players:
    if p != winner:
        print(f"{p.name} - {p.points()}")

print("Goodbye!")