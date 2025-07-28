

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
        'dice_faces',
        nargs='+',
        help='Dice face values (space or comma separated). Must have at least 2 faces.'
    )
    
    return parser.parse_args()


def validate_dice_faces(faces_input):

    if len(faces_input) == 1 and ',' in faces_input[0]:
        faces_input = faces_input[0].split(',')
    
    try:
        faces = [int(face.strip()) for face in faces_input]
    except ValueError as e:
        raise ValueError(f"All dice faces must be integers. Error: {e}")
    
    if len(faces) < 2:
        raise ValueError("Dice must have at least 2 faces.")
    
    if len(set(faces)) < 2:
        raise ValueError("Dice must have at least 2 different face values.")
    
    return faces


def main():

    try:
        args = parse_arguments()
        
        try:
            dice_faces = validate_dice_faces(args.dice_faces)
        except ValueError as e:
            print(f"Error: {e}")
            print("Use --help for usage information.")
            sys.exit(1)
        
        game = DiceGame(dice_faces)
        game.run()
        
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
