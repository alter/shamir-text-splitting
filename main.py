#!/usr/bin/env python3

import numpy as np
import sympy
from secrets import randbelow

# Кодирование строки в число
def encode_string(s):
    return int.from_bytes(s.encode('utf-8'), 'big')

# Декодирование числа обратно в строку
def decode_number(n):
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode('utf-8')

# Генерация случайного полинома второго порядка с заданным свободным членом
def generate_polynomial(secret, p):
    a_1 = randbelow(p)
    a_2 = randbelow(p)
    return np.poly1d([a_2, a_1, secret])

# Генерация долей секрета
def generate_shares(poly, n_shares, p):
    shares = [(i, poly(i) % p) for i in range(1, n_shares + 1)]
    return shares

# Восстановление секрета из долей
def recover_secret(shares, p):
    x = sympy.Symbol('x')
    lagrange_poly = sum([share[1]*np.prod([(x-i)/(share[0]-i) for i in range(1, len(shares)+1) if i != share[0]]) for share in shares])
    lagrange_poly = sympy.expand(lagrange_poly)

    return int(lagrange_poly.subs(x, 0)) % p

def main():
  # Ваша строка
  s = "Привет, мир!"
  
  # Кодируем строку в число
  secret = encode_string(s)
  
  # Выберем большое простое число. Это число должно быть больше любого возможного числа, полученного при кодировании вашей строки.
  p = sympy.nextprime(secret+1)
  
  # Генерируем полином
  poly = generate_polynomial(secret, p)
  
  # Генерируем доли секрета
  shares = generate_shares(poly, 4, p)
  print("Доли секрета: ", shares)
  
  # Восстанавливаем секрет из любых двух долей
  recovered_secret = recover_secret(shares[:2], p)
  recovered_string = decode_number(recovered_secret)
  
  print("Восстановленная строка: ", recovered_string)

if __name__ == "__main__":
  main()
