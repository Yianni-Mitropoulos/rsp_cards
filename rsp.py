import tkinter as tk
import random

# Game settings
cards = ['Rock', 'Paper', 'Scissors']

def create_hand():
    """Create a random hand for a player."""
    return [random.choice(cards) for _ in range(5)]

def determine_winner(attack, defend):
    """Determine if the defender takes damage."""
    if (attack == 'Rock' and defend == 'Scissors') or \
       (attack == 'Scissors' and defend == 'Paper') or \
       (attack == 'Paper' and defend == 'Rock'):
        return True
    return False

class RPSGame:
    def __init__(self, master, player_number, other_game=None):
        self.master = master
        self.player_number = player_number
        self.other_game = other_game
        self.score = 0
        self.attack_hand = create_hand()
        self.defense_hand = create_hand()
        self.chosen_card = None
        self.chosen_index = None
        self.is_attacker = True if player_number == 1 else False

        self.master.title(f"Player {player_number} - Rock-Paper-Scissors")
        self.score_label = tk.Label(master, text=f"Score: {self.score}")
        self.score_label.pack()

        self.attack_frame = tk.Frame(master)
        self.attack_frame.pack()
        self.defense_frame = tk.Frame(master)
        self.defense_frame.pack()

        self.status_label = tk.Label(master, text="Select your card")
        self.status_label.pack()

        self.create_buttons()

    def create_buttons(self):
        # Create attack buttons
        self.attack_buttons = []
        for i, card in enumerate(self.attack_hand):
            btn = tk.Button(self.attack_frame, text=f"Attack with {card}",
                            command=lambda i=i: self.select_card(i, True))
            btn.pack(side='left')
            self.attack_buttons.append(btn)

        # Create defense buttons
        self.defense_buttons = []
        for i, card in enumerate(self.defense_hand):
            btn = tk.Button(self.defense_frame, text=f"Defend with {card}",
                            command=lambda i=i: self.select_card(i, False))
            btn.pack(side='left')
            self.defense_buttons.append(btn)

        self.update_buttons_state()

    def select_card(self, index, is_attack):
        card_list = self.attack_hand if is_attack else self.defense_hand
        self.chosen_card = card_list[index]
        self.chosen_index = index
        self.status_label.config(text=f"Selected: {self.chosen_card} to {'attack' if is_attack else 'defend'}")
        self.disable_buttons()
        if self.other_game.chosen_card is not None:
            self.resolve_round()
        elif self.other_game:
            self.other_game.status_label.config(text="Waiting for other player...")

    def resolve_round(self):
        if self.is_attacker:
            attack_card = self.chosen_card
            defend_card = self.other_game.chosen_card
        else:
            attack_card = self.other_game.chosen_card
            defend_card = self.chosen_card

        if determine_winner(attack_card, defend_card):
            if self.is_attacker:
                self.score += 1
            else:
                self.other_game.score += 1

        self.update_scores()
        self.replace_card()
        self.switch_roles()

    def update_scores(self):
        self.score_label.config(text=f"Score: {self.score}")
        self.other_game.score_label.config(text=f"Score: {self.other_game.score}")
        self.status_label.config(text="Turn resolved. Waiting for next turn...")
        self.other_game.status_label.config(text="Turn resolved. Waiting for next turn...")

    def replace_card(self):
        # Replace the played card with a new one
        new_card = random.choice(cards)
        if self.is_attacker:
            self.attack_hand[self.chosen_index] = new_card
        else:
            self.defense_hand[self.chosen_index] = new_card
        self.update_buttons()

    def update_buttons(self):
        for i, btn in enumerate(self.attack_buttons):
            btn.config(text=f"Attack with {self.attack_hand[i]}")
        for i, btn in enumerate(self.defense_buttons):
            btn.config(text=f"Defend with {self.defense_hand[i]}")

    def switch_roles(self):
        self.is_attacker = not self.is_attacker
        self.other_game.is_attacker = not self.other_game.is_attacker
        self.chosen_card = None
        self.other_game.chosen_card = None
        self.update_buttons_state()
        self.other_game.update_buttons_state()

    def update_buttons_state(self):
        for btn in self.attack_buttons:
            btn.config(state='normal' if self.is_attacker else 'disabled')
        for btn in self.defense_buttons:
            btn.config(state='normal' if not self.is_attacker else 'disabled')

    def disable_buttons(self):
        for btn in self.attack_buttons + self.defense_buttons:
            btn.config(state='disabled')

def main():
    root1 = tk.Tk()
    root2 = tk.Tk()
    game1 = RPSGame(root1, 1)
    game2 = RPSGame(root2, 2, game1)
    game1.other_game = game2
    root1.geometry("300x200+100+100")
    root2.geometry("300x200+500+100")
    root1.mainloop()
    root2.mainloop()

if __name__ == "__main__":
    main()
