import Rotor

class Config:
    def __init__(self):
        rotor_I_wiring = 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'
        rotor_I_turnover = 'Q'
        rotor_II_wiring = 'AJDKSIRUXBLHWTMCQGZNPYFVOE'
        rotor_II_turnover = 'E'
        rotor_III_wiring = 'BDFHJLCPRTXVZNYEIWGAKMUSQO'
        rotor_III_turnover = 'V'
        reflector_B_wiring = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'

        self.rotor_I = Rotor.Rotor(rotor_I_wiring, rotor_I_turnover)
        self.rotor_II = Rotor.Rotor(rotor_II_wiring, rotor_II_turnover)
        self.rotor_III = Rotor.Rotor(rotor_III_wiring, rotor_III_turnover)
        self.reflector_B = Rotor.Rotor(reflector_B_wiring, '')