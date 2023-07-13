import string

class EnigmaM3:
    def __init__(self, rotor_config, rotor_positions, reflector_config, plugboard_config=None):
        self.rotors = rotor_config
        self.positions = rotor_positions
        self.reflector = reflector_config
        self.plugboard = self._create_plugboard(plugboard_config)

    def _create_plugboard(self, config):
        if config is None:
            return {}

        plugboard = {}
        for pair in config:
            plugboard[pair[0]] = pair[1]
            plugboard[pair[1]] = pair[0]
        return plugboard

    def _rotate_rotors(self):
        # if no turnover, rotate the rightmost rotor
        if self.positions[2] != ord(self.rotors[2].turnover) - 65 and self.positions[1] != ord(self.rotors[1].turnover) - 65:
            self.positions[2] = (self.positions[2] + 1) % 26
        # if right rotor is at turnover, rotate the middle rotor and the right rotor
        elif self.positions[2] == ord(self.rotors[2].turnover) - 65:
            self.positions[1] = (self.positions[1] + 1) % 26
            self.positions[2] = (self.positions[2] + 1) % 26
            # if middle rotor is at turnover, rotate the left rotor
            if self.positions[1] - 1 == ord(self.rotors[1].turnover) - 65:
                self.positions[0] = (self.positions[0] + 1) % 26
        # if middle rotor is at turnover, rotate the left rotor, middle rotor, and right rotor
        elif self.positions[1] == ord(self.rotors[1].turnover) - 65:
            self.positions[0] = (self.positions[0] + 1) % 26
            self.positions[1] = (self.positions[1] + 1) % 26
            self.positions[2] = (self.positions[2] + 1) % 26

        print(chr(self.positions[0] + 65) + chr(self.positions[1] + 65) + chr(self.positions[2] + 65))

    def _encrypt_letter(self, letter):
        letter = letter.upper()

        # Step 1: Rotate Rotors
        self._rotate_rotors()

        # Step 2: Plugboard
        letter = self.plugboard.get(letter, letter)
        print("Plugboard input: " + letter)

        # Step 3: Rotors (forward)
        letter = self.rotors[2].encrypt_forward(letter, self.positions[2], None)
        print("Rotor " + str(3) + ": " + letter)
        letter = self.rotors[1].encrypt_forward(letter, self.positions[1], self.positions[2])
        print("Rotor " + str(2) + ": " + letter)
        letter = self.rotors[0].encrypt_forward(letter, self.positions[0], self.positions[1])
        print("Rotor " + str(1) + ": " + letter)

        # Step 4: Reflector
        letter = self.reflector.encrypt_reflect(letter, self.positions[0])
        print("Reflector: " + letter)

        # Step 5: Rotors (backward)
        letter = self.rotors[0].encrypt_backward(letter, self.positions[0], None)
        print("Rotor " + str(1) + ": " + letter)
        letter = self.rotors[0].encrypt_backward(letter, self.positions[1], self.positions[0])
        print("Rotor " + str(2) + ": " + letter)
        letter = self.rotors[1].encrypt_backward(letter, self.positions[2], self.positions[1])
        print("Rotor " + str(3) + ": " + letter)
        letter = self.rotors[2].encrypt_backward(letter, None, self.positions[2])
        print("Result: " + letter)

        # Step 6: Plugboard
        letter = self.plugboard.get(letter, letter)
        print("Plugboard output: " + letter)

        print("")

        return letter if letter.isupper() else ''

    def encrypt(self, text):
        encrypted_text = ''
        for char in text:
            encrypted_text += self._encrypt_letter(char)
        return encrypted_text
