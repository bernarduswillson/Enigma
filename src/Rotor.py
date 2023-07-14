class Rotor:
    def __init__(self, wiring, turnover):
        self.wiring = wiring
        self.turnover = turnover

    def encrypt_forward(self, letter, position, prev_position):
        if prev_position == None:
            return self.wiring[((position + ord(letter) - 65) % 26)]
        else:
            return self.wiring[((position + ord(letter) - 65 - prev_position) % 26)]

    def encrypt_reflect(self, letter, prev_position):
        if 0 > (ord(letter) - 65) % 26:
            return self.wiring[((0 + ord(letter) - 65) % 26)]
        else:
            return self.wiring[((0 + ord(letter) - 65 - prev_position) % 26)]
        
        
    def encrypt_backward(self, letter, position, prev_position):
        if prev_position == None:
            return chr(((ord(letter) - 65 + position) % 26) + 65)
        elif position == None:
            index = self.wiring.find(letter)
            return chr(((index - prev_position) % 26) + 65)
        else:
            index = self.wiring.find(letter)
            return chr(((index + position - prev_position) % 26) + 65)