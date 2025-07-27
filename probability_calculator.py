"""
Probability calculator and table formatter for dice game analysis.
"""

from collections import Counter
from fractions import Fraction


class ProbabilityCalculator:
    """Calculate and display probability analysis for dice outcomes."""
    
    def __init__(self, dice_faces):
        """
        Initialize probability calculator.
        
        Args:
            dice_faces: List of integers representing dice face values
        """
        self.dice_faces = sorted(dice_faces)
        self.num_faces = len(dice_faces)
        self._calculate_probabilities()
    
    def _calculate_probabilities(self):
        """Calculate probabilities for all possible outcomes."""
        # Generate all possible outcomes
        outcomes = []
        for computer_move in range(self.num_faces):
            for user_move in range(self.num_faces):
                result_index = (computer_move + user_move) % self.num_faces
                result_value = self.dice_faces[result_index]
                outcomes.append(result_value)
        
        # Count occurrences of each face value
        outcome_counts = Counter(outcomes)
        total_outcomes = len(outcomes)
        
        # Calculate probabilities as fractions and decimals
        self.probabilities = {}
        for face_value in sorted(set(self.dice_faces)):
            count = outcome_counts[face_value]
            fraction = Fraction(count, total_outcomes)
            decimal = float(fraction)
            self.probabilities[face_value] = {
                'count': count,
                'fraction': fraction,
                'decimal': decimal,
                'percentage': decimal * 100
            }
    
    def display_probability_table(self):
        """Display probability table using ASCII formatting."""
        print("Probability of each outcome:")
        print()
        
        # Calculate column widths
        face_values = sorted(set(self.dice_faces))
        max_face_width = max(len(str(face)) for face in face_values)
        max_fraction_width = max(len(str(self.probabilities[face]['fraction'])) 
                               for face in face_values)
        max_decimal_width = 8  # For decimal display (.4f format)
        max_percent_width = 7  # For percentage (xx.xx%)
        
        # Ensure minimum widths
        face_width = max(max_face_width, 4)
        fraction_width = max(max_fraction_width, 8)
        decimal_width = max_decimal_width
        percent_width = max_percent_width
        
        # Create table header
        header_line = f"| {'Face':>{face_width}} | {'Fraction':>{fraction_width}} | {'Decimal':>{decimal_width}} | {'Percent':>{percent_width}} |"
        separator_line = "+" + "-" * (face_width + 2) + "+" + "-" * (fraction_width + 2) + "+" + "-" * (decimal_width + 2) + "+" + "-" * (percent_width + 2) + "+"
        
        print(separator_line)
        print(header_line)
        print(separator_line)
        
        # Print each probability row
        for face_value in face_values:
            prob = self.probabilities[face_value]
            fraction_str = str(prob['fraction'])
            decimal_str = f"{prob['decimal']:.4f}"
            percent_str = f"{prob['percentage']:.2f}%"
            
            row = f"| {face_value:>{face_width}} | {fraction_str:>{fraction_width}} | {decimal_str:>{decimal_width}} | {percent_str:>{percent_width}} |"
            print(row)
        
        print(separator_line)
        print()
        
        # Additional statistics
        total_combinations = self.num_faces * self.num_faces
        print(f"Total possible combinations: {total_combinations}")
        print(f"Each combination has equal probability: 1/{total_combinations}")
        print()
        
        # Show face distribution
        face_counts = Counter(self.dice_faces)
        print("Face value distribution on the die:")
        for face_value in sorted(face_counts.keys()):
            count = face_counts[face_value]
            print(f"  Value {face_value}: appears {count} time(s)")
        print()
    
    def get_probability(self, face_value):
        """
        Get probability information for a specific face value.
        
        Args:
            face_value: The face value to get probability for
            
        Returns:
            dict: Probability information or None if face value not found
        """
        return self.probabilities.get(face_value)
    
    def get_most_likely_outcome(self):
        """
        Get the most likely outcome(s).
        
        Returns:
            list: Face values with highest probability
        """
        max_prob = max(prob['decimal'] for prob in self.probabilities.values())
        return [face for face, prob in self.probabilities.items() 
                if prob['decimal'] == max_prob]
    
    def get_least_likely_outcome(self):
        """
        Get the least likely outcome(s).
        
        Returns:
            list: Face values with lowest probability
        """
        min_prob = min(prob['decimal'] for prob in self.probabilities.values())
        return [face for face, prob in self.probabilities.items() 
                if prob['decimal'] == min_prob]
