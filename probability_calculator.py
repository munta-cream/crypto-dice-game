from collections import Counter
from fractions import Fraction
class ProbabilityCalculator:
    def __init__(self, dice_faces):
        self.dice_faces = sorted(dice_faces)
        self.num_faces = len(dice_faces)
        self._calculate_probabilities()  
    def _calculate_probabilities(self):
        outcomes = []
        for computer_move in range(self.num_faces):
            for user_move in range(self.num_faces):
                result_index = (computer_move + user_move) % self.num_faces
                result_value = self.dice_faces[result_index]
                outcomes.append(result_value)
        outcome_counts = Counter(outcomes)
        total_outcomes = len(outcomes)
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
        print("Probability of each outcome:")
        print()
        face_values = sorted(set(self.dice_faces))
        max_face_width = max(len(str(face)) for face in face_values)
        max_fraction_width = max(len(str(self.probabilities[face]['fraction'])) 
                               for face in face_values)
        max_decimal_width = 8 
        max_percent_width = 7  
        face_width = max(max_face_width, 4)
        fraction_width = max(max_fraction_width, 8)
        decimal_width = max_decimal_width
        percent_width = max_percent_width
        header_line = f"| {'Face':>{face_width}} | {'Fraction':>{fraction_width}} | {'Decimal':>{decimal_width}} | {'Percent':>{percent_width}} |"
        separator_line = "+" + "-" * (face_width + 2) + "+" + "-" * (fraction_width + 2) + "+" + "-" * (decimal_width + 2) + "+" + "-" * (percent_width + 2) + "+"      
        print(separator_line)
        print(header_line)
        print(separator_line)
        for face_value in face_values:
            prob = self.probabilities[face_value]
            fraction_str = str(prob['fraction'])
            decimal_str = f"{prob['decimal']:.4f}"
            percent_str = f"{prob['percentage']:.2f}%"    
            row = f"| {face_value:>{face_width}} | {fraction_str:>{fraction_width}} | {decimal_str:>{decimal_width}} | {percent_str:>{percent_width}} |"
            print(row)
        print(separator_line)
        print()
        total_combinations = self.num_faces * self.num_faces
        print(f"Total possible combinations: {total_combinations}")
        print(f"Each combination has equal probability: 1/{total_combinations}")
        print()
        face_counts = Counter(self.dice_faces)
        print("Face value distribution on the die:")
        for face_value in sorted(face_counts.keys()):
            count = face_counts[face_value]
            print(f"  Value {face_value}: appears {count} time(s)")
        print()
    def get_probability(self, face_value):
        return self.probabilities.get(face_value)
    def get_most_likely_outcome(self):
        max_prob = max(prob['decimal'] for prob in self.probabilities.values())
        return [face for face, prob in self.probabilities.items() 
                if prob['decimal'] == max_prob]
    def get_least_likely_outcome(self):
        min_prob = min(prob['decimal'] for prob in self.probabilities.values())
        return [face for face, prob in self.probabilities.items() 
                if prob['decimal'] == min_prob]
