import numpy as np


# Murican Eagle Units:
# Presure in Psi
# Speeds in mph
# Lengths in inches

# inputed
G = 5000000000 #"shear modulus" # may differ in directions, use minimum value with safety factor in pascal
t = .003 #"fin thickness"

# taken from open rocket at maximum velocity
a = 316 #"speed of sound @ sim temp height" -> taken to be m/s
P = 47000 #"atmospheric presure @ sim temp height" pascal

root_chord = 0.3 # in meters
tip_chord = 0.07 # in meters
b = 0.16 #"semispan" in meters

# natural
P0 = 101325 #"atmospheric presure @ sea level temp height" pascal

## Conversions:


def get_flutter(root_chord, tip_chord, G, t, b, a, P, P0):
  '''
  All inputs to the top function are in meters, meters/second, and pascals. Conversions neccesary 
  since equation sources use a mixture of units: freedom/eagle and stars/stripe.
  '''
  # conversion equations
  m_to_inch = 39.370
  mpers_to_mph = 2.237
  pasc_to_psi = (1/6895.000)
  mph_to_mpers = (1/2.237)
  mph_to_ftpers = 1.467
  ftpers_to_mpers = (1/3.281)
  # conversions
  root_chord = root_chord*m_to_inch
  tip_chord = tip_chord*m_to_inch
  t = t*m_to_inch
  b = b*m_to_inch
  a = a*mpers_to_mph
  S = 0.5*(root_chord+tip_chord)*b
  G = G*pasc_to_psi
  P = P*pasc_to_psi
  P0 = P0*pasc_to_psi
  # formula
  lam = tip_chord/root_chord
  AR = (b**2)/S
  denom = ((39.3*(AR**3)) / (((t/root_chord)**3) * (AR + 2))) * ((lam+1)/2) * (P/P0)
  model1 = (a * np.sqrt(G / denom))*mph_to_mpers
  a = a*mph_to_ftpers
  model2 = a*(np.sqrt(G / ((1.337*(AR**3)*P*(lam+1)) / (2*(AR+2)*(t/root_chord)**3)))) * ftpers_to_mpers
  print("model1:", model1, "model2:", model2)
  return (model1 + model2) / 2


def get_divergence(root_chord, tip_chord, G, t, b, a, P, P0):
  scalarMultiplier = 1.3
  # conversion equations
  m_to_inch = 39.370
  mpers_to_mph = 2.237
  pasc_to_psi = (1/6895.000)
  mph_to_mpers = (1/2.237)
  # conversions
  root_chord = root_chord*m_to_inch
  tip_chord = tip_chord*m_to_inch
  t = t*m_to_inch
  b = b*m_to_inch
  a = a*mpers_to_mph
  S = 0.5*(root_chord+tip_chord)*b
  G = G*pasc_to_psi
  P = P*pasc_to_psi
  P0 = P0*pasc_to_psi
  # formula  
  AR = (b**2)/S
  calc = (3.3*P)/(1+(2/AR)) * ((root_chord+tip_chord)/(t**3)) * b**2
  return a * np.sqrt(G / calc)*mph_to_mpers * scalarMultiplier

print(get_flutter(root_chord, tip_chord, G, t, b, a, P, P0))
print(get_divergence(root_chord, tip_chord, G, t, b, a, P, P0))