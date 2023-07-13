import Enigma
import Config

Config = Config.Config()
rotor_config = [Config.rotor_I, Config.rotor_II, Config.rotor_III]
rotor_positions = [ord('A') - 65, ord('A') - 65, ord('A') - 65]
reflector_config = Config.reflector_B
plugboard_config = []

enigma = Enigma.EnigmaM3(rotor_config, rotor_positions, reflector_config, plugboard_config)

plaintext = 'AAA'
ciphertext = enigma.encrypt(plaintext)
print('Ciphertext:', ciphertext)