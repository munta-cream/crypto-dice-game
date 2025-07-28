import sys
import argparse
from dice_game import DiceGame
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Cryptographically secure dice game with HMAC-based fair play verification",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
The game uses HMAC-SHA3 for cryptographic security and ensures fair play
by having both computer and user contribute to the randomness.
        """
    ) 
    parser.add_argument(
        'dice_sets',
        nargs='+',
        help='Multiple dice sets (comma-separated values). Each set represents one die option.'
    )
    return parser.parse_args()
def validate_dice_sets(dice_sets_input):
    if len(dice_sets_input) < 2:
        raise ValueError("Must provide at least 2 dice sets.")
    dice_sets = []
    for i, dice_set_str in enumerate(dice_sets_input):
        try:
            faces = [int(face.strip()) for face in dice_set_str.split(',')]
        except ValueError as e:
            raise ValueError(f"All dice faces must be integers in set {i+1}. Error: {e}")    
        if len(faces) < 2:
            raise ValueError(f"Dice set {i+1} must have at least 2 faces.")    
        dice_sets.append(faces) 
    return dice_sets
def main():
    try:
        args = parse_arguments()
        try:
            dice_sets = validate_dice_sets(args.dice_sets)
        except ValueError as e:
            print(f"Error: {e}")
            print("Use --help for usage information.")
            sys.exit(1)
        game = DiceGame(dice_sets)
        game.run()      
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
if __name__ == "__main__":
    main()