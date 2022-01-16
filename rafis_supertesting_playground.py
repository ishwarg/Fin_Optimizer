import numpy as np


# Murican Eagle Units:
# Presure in Psi
# Speeds in mph
# Lengths in inches

# inputed
G = 1667934 #"shear modulus" # may differ in directions, use minimum value with safety factor 
t = .118 #"fin thickness"

# taken from open rocket at maximum velocity
a = 720.23 #"speed of sound @ sim temp height" -> taken to be m/s
P = 10.57 #"atmospheric presure @ sim temp height"

root_chord = 11.811
tip_chord = 0.394
b = 6.3 #"semispan"
S = 0.5*(root_chord+tip_chord)*b #"surface area of fin"

# natural
P0 = 14.7 #"atmospheric presure @ sea level temp height"

def get_flutter(root_chord, tip_chord, G, S, t, b, a, P, P0):
  lam = tip_chord/root_chord
  AR = (b**2)/S
  denom = ((39.3*(AR**3)) / (((t/root_chord)**3) * (AR + 2))) * ((lam+1)/2) * (P/P0)
  return a * np.sqrt(G / denom)


def get_divergence(root_chord, tip_chord, G, S, t, b, a, P, P0):
  AR = (b**2)/S
  calc = (3.3*P)/(1+(2/AR)) * ((root_chord+tip_chord)/(t**3)) * b**2
  return a * np.sqrt(G / calc)

print(get_flutter(root_chord, tip_chord, G, S, t, b, a, P, P0))
print(get_divergence(root_chord, tip_chord, G, S, t, b, a, P, P0))