def dec2bin(n):
    binary = []
    while n > 0:
        binary.insert(0, n % 2)
        n = n // 2
    return binary

def bin2dec(vector):
  dec = 0
  list = vector[::-1]
  for i in range (len(list)):
    if list[i] == 1:
      dec += (2 ** i)
  return dec

def xor(list1, list2):
  if len(list1) < len(list2):
    list1, list2 = list2, list1
  result = [0] * len(list1)
  list1 = list1[::-1]
  list2 = list2[::-1]
  for i in range(len(list2)):
    result[i] = int(list1[i] != list2[i])
  for i in range(len(list2), len(list1)):
    result[i] = list1[i]
  return result[::-1]

def AI(game_state, play_style):
  target_state = game_state
  bin_vectors = []
  for pile in game_state:
      bin_vectors.append(dec2bin(pile))
  vector_sum = []
  for vector in bin_vectors:
    vector_sum = xor(vector, vector_sum)
  nim_sum = bin2dec(vector_sum)
  if play_style == "misere":
    zero_piles = []
    for vector in bin_vectors:
      if xor(dec2bin(nim_sum), vector) == 0:
        zero_piles.append(bin2dec(vector))
    if len(zero_piles) > 1:
      target_pile = max(zero_piles)
    possible_moves = []
    for i in range(1, target_pile):
      if xor(dec2bin(nim_sum), dec2bin(target_pile - i)) == 0:
        possible_moves.append(target_pile - i)
    for i in range (len(game_state)):
      if game_state[i] == target_pile:
        target_state[i] = max(possible_moves)
        break
  elif play_style == "normal":
    non_zero_piles = []
    nim_sums = []
    for vector in bin_vectors:
      nim_sum = bin2dec(xor(dec2bin(nim_sum), vector))
      if nim_sum != 0:
        non_zero_piles.append(bin2dec(vector))
        nim_sums.append(nim_sum)
    if len(non_zero_piles) > 1:
      target_pile = non_zero_piles[min(nim_sums)]
    possible_moves = []
    for i in range(1, target_pile):
      if xor(dec2bin(nim_sum), dec2bin(target_pile - i)) != 0:
        possible_moves.append(target_pile - i)
    for i in range (len(game_state)):
      if game_state[i] == target_pile:
        target_state[i] = max(possible_moves)
        break
  
  return target_state