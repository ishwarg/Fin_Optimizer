import numpy as np

# inputed
G = "shear modulus" # may differ in directions, use minimum value with safety factor 
t = "fin thickness"

# taken from open rocket at maximum velocity
a = "speed of sound @ sim temp height"
P = "atmospheric presure @ sim temp height"

root_cord = 10
tip_cord = 15
S = "surface area of fin"
b = "semispan"

# natural
P0 = "atmospheric presure @ sea level temp height"

def get_flutter(root_chord, tip_chord, G, S, t, b, a, P, P0):
  lam = tip_chord/root_chord
  AR = (b**2)/S
  denom = ((39.3*(AR**3)) / (((t/root_chord)**3) * (AR + 2))) * ((lam+1)/2) * (P/P0)
  return a * np.sqrt(G / denom)


def get_divergence(root_chord, tip_chord, G, S, t, b, a, P, P0):
  AR = (b**2)/S
  calc = (3.3*P)/(1+(2/AR)) * ((root_chord+tip_chord)/(t**3)) * b**2 
  return a * np.sqrt(G / calc)