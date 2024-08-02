import pygame as pg
import Scripts.Source.General.utils as utils_m


class DataManager:
    letters_width = []

    @staticmethod
    def parse_letter_widths(file_path):
        letter_widths = []

        with open(file_path, 'r') as f:
            for line in f:
                # Each line is expected to be in the format "Letter {idx}: {width}"
                parts = line.strip().split(': ')
                if len(parts) == 2:
                    width = float(parts[1])
                    letter_widths.append(width)

        return letter_widths

    @staticmethod
    def init():
        DataManager.letters_width = DataManager.parse_letter_widths('Data/letter_width.txt')

    @staticmethod
    def update_letters_width():
        DataManager.letter_widths = utils_m.calculate_width_letters('textures/Verdana_B_alpha.png')
        with open('Data/letter_width.txt', 'w') as f:
            for idx, width in enumerate(DataManager.letter_widths):
                f.write(f"Letter {idx}: {width}\n")
