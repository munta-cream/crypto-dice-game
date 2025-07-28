import sys
from crypto_utils import CryptoUtils


class DiceGame:
    
    def __init__(self, dice_sets):
        self.dice_sets = dice_sets
        self.crypto = CryptoUtils()
        self.computer_goes_first = None
        self.computer_dice_index = None
        self.user_dice_index = None
        self.computer_dice = None
        self.user_dice = None   
    def determine_first_player(self):
        print("Let's determine who makes the first move.")
        computer_key = self.crypto.generate_secure_key()
        computer_choice = self.crypto.generate_secure_random(2)  
        computer_hmac = self.crypto.calculate_hmac(computer_key, str(computer_choice))     
        print(f"I selected a random value in the range 0..1")
        print(f"(HMAC={computer_hmac}).")
        print("Try to guess my selection.")
        while True:
            print("0 - 0")
            print("1 - 1") 
            print("X - exit")
            print("? - help")          
            choice = input("Your selection: ").strip().upper()           
            if choice == 'X':
                return False
            elif choice == '?':
                self.display_help()
                continue
            elif choice in ['0', '1']:
                user_guess = int(choice)
                break
            else:
                print("Please enter 0, 1, X, or ?")
                continue
        print(f"My selection: {computer_choice} (KEY={computer_key}).")
        if user_guess == computer_choice:
            self.computer_goes_first = True
            print("I make the first move and choose the dice.")
        else:
            self.computer_goes_first = False
            print("You make the first move and choose the dice.")    
        return True
    def display_dice_options(self, exclude_index=None):
        print("Choose your dice:")
        for i, dice_set in enumerate(self.dice_sets):
            if exclude_index is None or i != exclude_index:
                dice_str = ','.join(map(str, dice_set))
                print(f"{i} - {dice_str}")
        print("X - exit")
        print("? - help") 
    def select_dice_first_player(self):
        """First player selects dice."""
        if self.computer_goes_first:
            self.computer_dice_index = self.crypto.generate_secure_random(len(self.dice_sets))
            self.computer_dice = self.dice_sets[self.computer_dice_index]
            dice_str = ','.join(map(str, self.computer_dice))
            print(f"I make the first move and choose the [{dice_str}] dice.")
        else:
            self.display_dice_options() 
            while True:
                choice = input("Your selection: ").strip().upper()    
                if choice == 'X':
                    return False
                elif choice == '?':
                    self.display_help()
                    continue
                try:
                    dice_index = int(choice)
                    if 0 <= dice_index < len(self.dice_sets):
                        self.user_dice_index = dice_index
                        self.user_dice = self.dice_sets[dice_index]
                        dice_str = ','.join(map(str, self.user_dice))
                        print(f"You choose the [{dice_str}] dice.")
                        break
                    else:
                        print(f"Please select a number between 0 and {len(self.dice_sets) - 1}")
                except ValueError:
                    print("Please enter a valid number, X, or ?")   
        return True
    def select_dice_second_player(self):
        if self.computer_goes_first:
            self.display_dice_options(exclude_index=self.computer_dice_index)
            while True:
                choice = input("Your selection: ").strip().upper()
                if choice == 'X':
                    return False
                elif choice == '?':
                    self.display_help()
                    continue
                try:
                    dice_index = int(choice)
                    if 0 <= dice_index < len(self.dice_sets):
                        if dice_index != self.computer_dice_index:
                            self.user_dice_index = dice_index
                            self.user_dice = self.dice_sets[dice_index]
                            dice_str = ','.join(map(str, self.user_dice))
                            print(f"You choose the [{dice_str}] dice.")
                            break
                        else:
                            print("That dice set is already selected. Choose a different one.")
                    else:
                        print(f"Please select a number between 0 and {len(self.dice_sets) - 1}")
                except ValueError:
                    print("Please enter a valid number, X, or ?")
        else:
            available_indices = [i for i in range(len(self.dice_sets)) if i != self.user_dice_index]
            self.computer_dice_index = available_indices[self.crypto.generate_secure_random(len(available_indices))]
            self.computer_dice = self.dice_sets[self.computer_dice_index]
            dice_str = ','.join(map(str, self.computer_dice))
            print(f"I choose the [{dice_str}] dice.")
        return True
    def roll_dice(self, dice, player_name):
        num_faces = len(dice)    
        print(f"It's time for {player_name} roll.")
        computer_key = self.crypto.generate_secure_key()
        computer_choice = self.crypto.generate_secure_random(num_faces)
        computer_hmac = self.crypto.calculate_hmac(computer_key, str(computer_choice)) 
        print(f"I selected a random value in the range 0..{num_faces-1}")
        print(f"(HMAC={computer_hmac}).")
        print(f"Add your number modulo {num_faces}.")
        while True:
            for i in range(num_faces):
                print(f"{i} - {i}")
            print("X - exit")
            print("? - help")
            choice = input("Your selection: ").strip().upper()
            if choice == 'X':
                return None
            elif choice == '?':
                self.display_help()
                continue
            try:
                user_choice = int(choice)
                if 0 <= user_choice < num_faces:
                    break
                else:
                    print(f"Please select a number between 0 and {num_faces - 1}")
            except ValueError:
                print("Please enter a valid number, X, or ?")
        print(f"My number is {computer_choice} (KEY={computer_key}).")
        result_index = (computer_choice + user_choice) % num_faces
        result_value = dice[result_index]
        print(f"The fair number generation result is {computer_choice} + {user_choice} = {result_index} (mod {num_faces}).")
        print(f"{player_name} roll result is {result_value}.") 
        return result_value
    def play_game(self):
        if not self.determine_first_player():
            return False
        if not self.select_dice_first_player():
            return False
        if not self.select_dice_second_player():
            return False
        if self.computer_goes_first:
            computer_result = self.roll_dice(self.computer_dice, "my")
            if computer_result is None:
                return False
            user_result = self.roll_dice(self.user_dice, "your")
            if user_result is None:
                return False
        else:
            user_result = self.roll_dice(self.user_dice, "your")
            if user_result is None:
                return False
            computer_result = self.roll_dice(self.computer_dice, "my")
            if computer_result is None:
                return False
        if user_result > computer_result:
            print(f"You win ({user_result} > {computer_result})!")
        elif computer_result > user_result:
            print(f"I win ({computer_result} > {user_result})!")
        else:
            print(f"It's a tie ({user_result} = {computer_result})!")   
        return True
    def display_help(self):
        print("\n" + "=" * 50)
        print("HELP - How to Play")
        print("=" * 50)
        print()
        print("GAME FLOW:")
        print("1. Determine who goes first (0/1 choice with HMAC)")
        print("2. First player selects a dice set") 
        print("3. Second player selects a different dice set")
        print("4. Both players roll their dice using fair random generation")
        print("5. Highest roll wins")
        print()
        print("FAIR PLAY:")
        print("- All random choices use HMAC-SHA3-256 commitment")
        print("- Computer commits first, user contributes, then computer reveals")
        print("- You can verify any HMAC manually using the revealed key")
        print()
        print("DICE SETS:")
        for i, dice_set in enumerate(self.dice_sets):
            dice_str = ','.join(map(str, dice_set))
            print(f"  {i}: [{dice_str}]")
        print()
    def run(self):
        print("Welcome to the Cryptographically Secure Dice Game!")
        print()
        print("Available dice sets:")
        for i, dice_set in enumerate(self.dice_sets):
            dice_str = ','.join(map(str, dice_set))
            print(f"  {i}: [{dice_str}]")
        print()
        while True:
            if not self.play_game():
                break  
            print("\nPlay again? (Y/N)")
            choice = input().strip().upper()
            if choice != 'Y':
                break
        print("Thank you for playing!")