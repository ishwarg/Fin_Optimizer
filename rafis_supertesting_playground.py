import math as m

# inputed
Fin = list(root_cord, tip_cord)
G = "shear modulus" # may differ in directions, use minimum value with safety factor 
S = "surface area of fin"
t = "fin thickness"
b = "semispan"

# calculated:
lam = tip_cord/root_cord # lambda
AR = ((b**2)/S)  # Aspect Ratio
a = "speed of sound @ sim temp height"
P = "atmospheric presure @ sim temp height"
P_o = "atmospheric presure @ sea level temp height"





def get_flutter(fin, G, a, P, P_o, AR, t):
  lam = (rootC / tipC)
  f_in_root = G / ((39.3*pow(AR,3))/(pow((t/rootC),3)*AR+2)*(lam+1)/2*(P/P_o))
  flutter_velocity = a * m.sqrt(f_in_root)
  return flutter_velocity

def get_divergence(fin, G, a, P, P_o, AR, t, b):
  d_in_root = G/((3.3*P)/(1+2/AR)*(rootC+tipC)/(pow(t,3))*pow(b,2))
  divergence_velocity = a * m.sqrt(d_in_root)
  return divergence_velocity

  # Assuming that the double "fin" contains all relevant fin parameters
  # e.g root chord (rootC)tip chord (tipC), fin thickness (t) and semispan (b), 
  # use rootC and tipC attributes of the fins
  # G is shear modulus of fin
  # a is speed of sound at simulation atmosphere
  # P and Po are atmospheric pressure at simulation altitude and sea level atmospheric pressure respectively
  # AR is Aspect Ratio = b^2/S * lambda where S is the surface area of the fin