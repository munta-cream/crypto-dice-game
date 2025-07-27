"""
Main dice game implementation with HMAC-based fair play verification.
"""

import sys
import hashlib
import hmac
from crypto_utils import CryptoUtils
from probability_calculator import ProbabilityCalculator


class DiceGame:
    """Main dice game class implementing HMAC-based fair play."""
    
    def __init__(self, dice_faces):
        """
        Initialize the dice game with specified faces.
        
        Args:
            dice_faces: List of integers representing dice face values
        """
        self.dice_faces = sorted(dice_faces)
        self.num_faces = len(dice_faces)
        self.crypto = CryptoUtils()
        self.prob_calc = ProbabilityCalculator(dice_faces)
        
        # Game state
        self.computer_key = None
        self.computer_move = None
        self.computer_hmac = None
        self.user_move = None
        
    def display_welcome(self):
        """Display welcome message and game rules."""
        print("=" * 60)
        print("CRYPTOGRAPHICALLY SECURE DICE GAME")
        print("=" * 60)
        print()
        print("Game Rules:")
        print("- This is a fair dice game using HMAC-SHA3 for verification")
        print("- Both you and the computer contribute to the randomness")
        print("- The computer generates a secret key and makes its move first")
        print("- You make your move without knowing the computer's choice")
        print("- The computer then reveals its key for verification")
        print("- The final result is calculated using both moves")
        print()
        print(f"Dice Configuration: {self.dice_faces}")
        print(f"Available face indices: 0 to {self.num_faces - 1}")
        print()
    
    def display_menu(self):
        """Display the main menu options."""
        print("\nMAIN MENU:")
        print("0 - Roll dice")
        print("1 - View probability table")  
        print("X - Exit")
        print("? - Help")
        print()
    
    def display_help(self):
        """Display help information."""
        print("\n" + "=" * 50)
        print("HELP - How to Play")
        print("=" * 50)
        print()
        print("DICE CONFIGURATION:")
        print(f"Your dice has {self.num_faces} faces with values: {self.dice_faces}")
        print("You select faces by their INDEX (position), not their value:")
        for i, face_value in enumerate(self.dice_faces):
            print(f"  Index {i} -> Face value {face_value}")
        print()
        print("FAIR PLAY MECHANISM:")
        print("1. Computer generates a 256-bit cryptographically secure random key")
        print("2. Computer selects its dice face and calculates HMAC(key, computer_move)")
        print("3. Computer shows you the HMAC (but not the key or move)")
        print("4. You select your dice face")
        print("5. Computer reveals its key and move")
        print("6. You can verify the HMAC to ensure the computer didn't cheat")
        print("7. Final result = (computer_move + user_move) % num_faces")
        print()
        print("VERIFICATION:")
        print("- The HMAC proves the computer chose its move before seeing yours")
        print("- You can verify: HMAC-SHA3-256(revealed_key, computer_move) matches shown HMAC")
        print("- This ensures complete fairness and prevents cheating")
        print()
    
    def generate_computer_move(self):
        """Generate computer's move with cryptographic security."""
        print("Let's determine who makes the first move. You have to prove to the user that choice is fair (it's not enough to generate a random bit 0 or 1; the user needs")
        print("a proof of the fair play).")
        print()
        
        # Generate cryptographically secure random key
        self.computer_key = self.crypto.generate_secure_key()
        
        # Generate computer's dice selection (0 to num_faces-1) 
        self.computer_move = self.crypto.generate_secure_random(self.num_faces)
        
        # Calculate HMAC for the computer's move
        self.computer_hmac = self.crypto.calculate_hmac(self.computer_key, str(self.computer_move))
        
        print(f"I selected a random value in the range 0..{self.num_faces-1}")
        print(f"(HMAC={self.computer_hmac}).")
        print("Try to guess my selection.")
    
    def get_user_move(self):
        """Get and validate user's dice selection."""
        while True:
            try:
                for i in range(self.num_faces):
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
                    move = int(choice)
                    if 0 <= move < self.num_faces:
                        self.user_move = move
                        return move
                    else:
                        print(f"Error: Please select a number between 0 and {self.num_faces - 1}")
                        continue
                except ValueError:
                    print("Error: Invalid input. Please enter a number, 'X' to exit, or '?' for help.")
                    continue
                    
            except KeyboardInterrupt:
                return None
    
    def reveal_and_verify(self):
        """Show the result and let user verify if they want."""
        # Fair random result using both moves
        if self.computer_move is not None and self.user_move is not None:
            result_index = (self.computer_move + self.user_move) % self.num_faces
        else:
            result_index = 0
        result_value = self.dice_faces[result_index]
        
        print(f"Your roll result is {result_value}.")
        
        # For dice with more than 2 sides, show who goes first
        if self.num_faces > 2:
            first_player = "You" if result_index % 2 == 0 else "I"
            print(f"{first_player} win ({result_value} > 8)!" if result_value > 8 else f"It's time for your roll." if first_player == "You" else f"It's time for my roll.")
        
        return result_value
    
    def calculate_result(self):
        """Calculate and display the final dice roll result."""
        # This method is now handled in reveal_and_verify
        return None
    
    def play_round(self):
        """Play a single round of the dice game."""
        # Step 1: Computer generates move and HMAC
        self.generate_computer_move()
        
        # Step 2: Get user's move  
        user_choice = self.get_user_move()
        if user_choice is None:
            return False  # User chose to exit
        
        print(f"Your selection: {user_choice}")
        print(f"My number is {self.computer_move} (KEY={self.computer_key}).")
        print(f"The fair number generation result is {self.computer_move} + {user_choice} = {(self.computer_move + user_choice) % self.num_faces} (mod {self.num_faces}).")
        
        # Step 3: Show result and let user verify if needed
        result = self.reveal_and_verify()
        
        return True
    
    def show_probability_table(self):
        """Display probability analysis table."""
        print("\n" + "=" * 60)
        print("PROBABILITY ANALYSIS")
        print("=" * 60)
        print()
        print("This table shows the probability of each outcome when both")
        print("computer and user make random selections.")
        print()
        
        self.prob_calc.display_probability_table()
        print()
    
    def run(self):
        """Main game loop."""
        self.display_welcome()
        
        while True:
            self.display_menu()
            
            try:
                choice = input("Select option: ").strip().upper()
                
                if choice == '0':
                    # Play a round
                    if not self.play_round():
                        break
                        
                elif choice == '1':
                    # Show probability table
                    self.show_probability_table()
                    
                elif choice == 'X':
                    # Exit
                    break
                    
                elif choice == '?':
                    # Help
                    self.display_help()
                    
                else:
                    print("Invalid option. Please try again.")
                    
            except KeyboardInterrupt:
                break
        
        print("\nThank you for playing! Goodbye!")
