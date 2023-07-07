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
        # Rotate the rightmost rotor
        self.positions[2] = (self.positions[2] + 1) % 26

        # Rotate the middle rotor
        if self.positions[2] == ord(self.rotors[2].turnover) + 1  - 65:
            self.positions[1] = (self.positions[1] + 1) % 26

        # Rotate the leftmost rotor
        if self.positions[1] == ord(self.rotors[1].turnover) + 1 - 65:
            self.positions[0] = (self.positions[0] + 1) % 26

        print(self.positions)

    def _encrypt_letter(self, letter):
        if letter in string.ascii_uppercase:
            letter = letter.upper()

            # Step 1: Rotate Rotors
            self._rotate_rotors()

            # Step 2: Plugboard
            letter = self.plugboard.get(letter, letter)
            print("Plugboard: " + letter)

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
            print("result: " + letter)

            # # Step 6: Plugboard
            # letter = self.plugboard.get(letter, letter)

            print("")

        return letter

    def encrypt(self, text):
        encrypted_text = ''
        for char in text:
            encrypted_text += self._encrypt_letter(char)
        return encrypted_text

    def decrypt(self, text):
        return self.encrypt(text)

class Rotor:
    def __init__(self, wiring, turnover):
        self.wiring = wiring
        self.turnover = turnover

    def encrypt_forward(self, letter, position, prev_position):
        print(position)
        print(ord(letter) - 65)
        
        if prev_position == None: # ini bisa > atau >= belom tau
            print((position + ord(letter) - 65) % 26)
            print("con 1")
            return self.wiring[((position + ord(letter) - 65) % 26)]
        else:
            print((position + ord(letter) - 65 - prev_position) % 26)
            print("con 2")
            return self.wiring[((position + ord(letter) - 65 - prev_position) % 26)]

    def encrypt_reflect(self, letter, prev_position):
        if 0 > (ord(letter) - 65) % 26:
            print((0 + ord(letter) - 65) % 26)
            print("")
            return self.wiring[((0 + ord(letter) - 65) % 26)]
        else:
            print((0 + ord(letter) - 65 - prev_position) % 26)
            print("")
            return self.wiring[((0 + ord(letter) - 65 - prev_position) % 26)]
        
        
    def encrypt_backward(self, letter, position, prev_position):
        print(position)
        print(ord(letter) - 65)

        if prev_position == None:
            print(((ord(letter) - 65 + position) % 26) + 65)
            print("msk")
            return chr(((ord(letter) - 65 + position) % 26) + 65)
        elif position == None:
            # find index of letter in wiring
            index = self.wiring.find(letter)
            print(index)
            print("n")
            return chr(((index - prev_position) % 26) + 65)
        else:
            # find index of letter in wiring
            index = self.wiring.find(letter)
            print(index)
            print("m")
            return chr(((index + position - prev_position) % 26) + 65)

# config
rotor_I_wiring = 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'
rotor_I_turnover = 'Q'
rotor_II_wiring = 'AJDKSIRUXBLHWTMCQGZNPYFVOE'
rotor_II_turnover = 'E'
rotor_III_wiring = 'BDFHJLCPRTXVZNYEIWGAKMUSQO'
rotor_III_turnover = 'V'
reflector_B_wiring = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'

rotor_I = Rotor(rotor_I_wiring, rotor_I_turnover)
rotor_II = Rotor(rotor_II_wiring, rotor_II_turnover)
rotor_III = Rotor(rotor_III_wiring, rotor_III_turnover)
reflector_B = Rotor(reflector_B_wiring, '')

rotor_config = [rotor_I, rotor_II, rotor_III]
rotor_positions = [ord('A') - 65, ord('A') - 65, ord('A') - 65]
reflector_config = reflector_B
plugboard_config = [(None, None), (None, None), (None, None), (None, None), (None, None), (None, None)]

enigma = EnigmaM3(rotor_config, rotor_positions, reflector_config, plugboard_config)

plaintext = 'AAAAAAAAAAAAAAAAAAAAAAAAA'
ciphertext = enigma.encrypt(plaintext)
print('Ciphertext:', ciphertext)













# # Dekripsi teks
# decrypted_text = enigma.decrypt(ciphertext)
# print('Decrypted text:', decrypted_text)
