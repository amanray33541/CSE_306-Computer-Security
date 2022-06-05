#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 21 10:10:12 2022

@author: amanray
"""
import numpy
import numpy as np
import time
from BitVector import *

import bitvector_demo

from collections import deque

count = 0
bv1 = 00


def convert_to_list(string):
    list1 = []
    list1[:0] = string
    return list1


def convert_to_hex(list1):
    hex_list = []
    for j in list1:
        hex_list.append(hex(ord(j)))
    return hex_list


def XOR(l1, l2):
    new_list = []
    lenth = len(l1)
    c = 0
    while c < lenth:
        # print(int(l1[c], 16))
        # print(int(l2[c], 16))
        element = hex(int(l1[c], 16) ^ int(l2[c], 16))[2:4]
        new_list.append(element)
        # print("element",element)
        c += 1
    return new_list


def XOR_two_hex_values(hex_val1, hex_val2):
    # print(type(hex_val1), type(hex_val2))
    added_hex_value = hex(int(hex_val1, 16) ^ int(hex_val2, 16))[2:4]
    return added_hex_value


def create_matrix(list1):
    a1 = list1[0:4]
    a2 = list1[4:8]
    a3 = list1[8:12]
    a4 = list1[12:16]
    matrix = numpy.array([a1, a2, a3, a4])
    # print(matrix)
    return matrix


def add_two_matrix(matrix_1, matrix_2):
    new_matrix = np.empty([0, 4])
    i = 0
    # print(XOR(matrix_1[i], matrix_2[i]))
    while i < 4:
        row_to_be_added = XOR(matrix_1[i], matrix_2[i])
        new_matrix = np.vstack((new_matrix, row_to_be_added))
        i += 1
    # print(new_matrix)
    return new_matrix


def multiply_two_hex_values(hex_1, hex_2):
    # hex_1 = BitVector(hexstring=hex_1)
    # hex_2 = BitVector(hexstring=hex_2)
    s = hex_1.gf_multiply_modular(hex_2, bitvector_demo.AES_modulus, 8)
    # print(hex(s.intValue()))
    return hex(s.intValue())


def substitute_bytes_of_matrix(m1):
    for i in range(4):

        for j in range(4):
            hex_val = str(m1[i][j])
            b = BitVector(hexstring=hex_val)
            int_val = b.intValue()
            s = bitvector_demo.Sbox[int_val]
            s = BitVector(intVal=s, size=8)
            m1[i][j] = s.get_bitvector_in_hex()
            # print(m1[i][j])
    return m1


def inverse_substitute_bytes_of_matrix(m1):
    for i in range(4):

        for j in range(4):
            hex_val = str(m1[i][j])
            b = BitVector(hexstring=hex_val)
            int_val = b.intValue()
            s = bitvector_demo.InvSbox[int_val]
            s = BitVector(intVal=s, size=8)
            m1[i][j] = s.get_bitvector_in_hex()
            # print(m1[i][j])
    return m1


def shift_rows_cyclically_by_offset(m1):
    for i in range(4):
        queue = deque(m1[i])
        queue.rotate(-i)
        m1[i] = queue
    # print(m1)
    return m1


def inverse_shift_rows_cyclically_by_offset(m1):
    for i in range(4):
        queue = deque(m1[i])
        queue.rotate(i)
        m1[i] = queue
    # print(m1)
    return m1


def mix_columns(m1):
    result = ([['0', '0', '0', '0'],
               ['0', '0', '0', '0'],
               ['0', '0', '0', '0'],
               ['0', '0', '0', '0']])
    # iterating by row of A
    for i in range(4):

        # iterating by coloum by B
        for j in range(4):

            # iterating by rows of B
            for k in range(4):
                # result[i][j] += const_matrix[i][k] * m1[k][j]
                result[i][j] = XOR_two_hex_values(result[i][j], multiply_two_hex_values(bitvector_demo.Mixer[i][k],
                                                                                        BitVector(hexstring=m1[k][j])))

    # print(result)
    result = numpy.array([result[0], result[1], result[2], result[3]])
    return result


def inverse_mix_columns(m1):
    result = ([['0', '0', '0', '0'],
               ['0', '0', '0', '0'],
               ['0', '0', '0', '0'],
               ['0', '0', '0', '0']])
    # iterating by row of A
    for i in range(4):

        # iterating by coloum by B
        for j in range(4):

            # iterating by rows of B
            for k in range(4):
                # result[i][j] += const_matrix[i][k] * m1[k][j]
                result[i][j] = XOR_two_hex_values(result[i][j], multiply_two_hex_values(bitvector_demo.InvMixer[i][k],
                                                                                        BitVector(hexstring=m1[k][j])))

    # print(result)
    result = numpy.array([result[0], result[1], result[2], result[3]])
    return result


def g(list1):
    global count
    global bv1
    count += 1
    g_list = []
    queue = deque(list1)
    # Circular byte left shift
    queue.rotate(-1)

    # Byte substitution
    for i in queue:
        hex_val = str(i)
        # print(hex_val)
        b = BitVector(hexstring=hex_val)
        int_val = b.intValue()
        s = bitvector_demo.Sbox[int_val]
        s = BitVector(intVal=s, size=8)
        g_list.append(s.get_bitvector_in_hex())
        # print(s.get_bitvector_in_hex())
    # print(g_list)

    # Adding round constant
    if count == 1:
        bv3 = BitVector(hexstring="01")
        bv1 = bv3
    else:
        bv2 = BitVector(hexstring="02")
        bv3 = bv1.gf_multiply_modular(bv2, bitvector_demo.AES_modulus, 8)
        bv1 = bv3

    sbyte = []
    sbyte.append(g_list[0])
    rc = []
    # print(hex(bv3.intValue()))
    rc.append(hex(bv3.intValue()))
    # print(rc[0])
    added = XOR(sbyte, rc)
    g_list[0] = added[0]
    # print('g list : ',g_list[0])
    return g_list


def concatenate_the_lists(a1, a2, a3, a4):
    list1 = a1 + a2 + a3 + a4
    return list1


def generate_round_keys(key_list):
    level = 0
    all_round_keys = []
    w0 = key_list[0:4]
    w1 = key_list[4:8]
    w2 = key_list[8:12]
    w3 = key_list[12:16]
    # print(w3)
    zero_level_key = concatenate_the_lists(w0, w1, w2, w3)
    all_round_keys.append(zero_level_key)

    while level < 10:
        w4 = XOR(w0, g(w3))
        w5 = XOR(w1, w4)
        w6 = XOR(w2, w5)
        w7 = XOR(w3, w6)
        new_level_key = concatenate_the_lists(w4, w5, w6, w7)
        all_round_keys.append(new_level_key)
        w0 = w4
        w1 = w5
        w2 = w6
        w3 = w7
        level += 1
    # for i in all_round_keys:
    #    print(i)
    return all_round_keys


def schedule_key(key):
    length_of_key = len(key)

    if length_of_key < 16:
        count1 = 16 - length_of_key
        i = 1
        while i <= count1:
            key += '0'
            i = i + 1
    elif length_of_key > 16:
        key = key[0: 16:]
        # print(key)

    hex_list = convert_to_hex(key)
    i = 0
    while i < len(hex_list):
        hex_list[i] = str(hex_list[i])[2: 4:]
        i += 1
    print()
    print("Key In ASCII: ", key)
    print("Key In Hex: ", end='')
    for i in range(len(hex_list)):
        print(hex_list[i], end='')
    print()
    return generate_round_keys(hex_list)


def encrypt(plaintext, keys):
    hex_list_of_plaintext = convert_to_hex(plaintext)
    i = 0
    while i < len(hex_list_of_plaintext):
        hex_list_of_plaintext[i] = str(hex_list_of_plaintext[i])[2: 4:]
        i += 1
    # print(hex_of_plaintext)
    # Adding round key
    matrix = (add_two_matrix(create_matrix(hex_list_of_plaintext), create_matrix(keys[0]))).transpose()
    # print(matrix)
    # Loop for 10 rounds
    round_number = 1
    while round_number < 11:
        matrix = substitute_bytes_of_matrix(matrix)
        matrix = shift_rows_cyclically_by_offset(matrix)
        if round_number != 10:
            matrix = mix_columns(matrix)
        # print(round_number)
        matrix = add_two_matrix(matrix, create_matrix(keys[round_number]).transpose())
        round_number += 1

    # print(matrix)
    # print(matrix[0], matrix[1], matrix[2], matrix[3])

    return matrix


def decrypt(matrix, keys):
    matrix = (add_two_matrix(matrix, create_matrix(keys[10]).transpose()))
    round_number = 9

    while round_number > -1:
        matrix = inverse_shift_rows_cyclically_by_offset(matrix)
        matrix = inverse_substitute_bytes_of_matrix(matrix)
        matrix = add_two_matrix(matrix, create_matrix(keys[round_number]).transpose())
        if round_number != 0:
            matrix = inverse_mix_columns(matrix)
        # print(round_number)
        round_number -= 1

    return matrix


def chunked(size, source):
    for i in range(0, len(source), size):
        yield source[i:i + size]


if __name__ == '__main__':

    key = input('Key: ')
    plaintext = input('Plaintext: ')

    #KEY SCHEDULING-

    start_of_key_scheduling = time.time()
    all_round_keys = schedule_key(key)
    end_of_key_scheduling = time.time()

    print()

    print('Plaintext In ASCII: ', plaintext)  
    print('Plaintext In Hex: ', end='') 
    plaintext_in_hex = convert_to_hex(plaintext) 
    for i in range(len(plaintext_in_hex)):  
        print((plaintext_in_hex[i])[2:4], end='')  

    print()
    print()

    #ENCRYPTION

    plaintext_in_list = list(
        chunked(16, plaintext))  # Processing plaintext into 16 bytes of chunks and adding them to the list
    encrypted_matrix_list = []

    start_of_encryption = time.time()
    for i in range(len(plaintext_in_list)):
        if len(plaintext_in_list[i]) < 16:
            count1 = 16 - len(plaintext_in_list[i])
            j = 1
            while j <= count1:
                plaintext_in_list[i] += ' '
                j += 1
        encrypted_matrix = encrypt(plaintext_in_list[i], all_round_keys)
        encrypted_matrix_list.append(encrypted_matrix)
    end_of_encryption = time.time()

    print("Cipher Text In ASCII: ", end='')
    for matrix in encrypted_matrix_list:
        matrix = matrix.transpose()
        for row in range(len(matrix)):
            for column in range(len(matrix[row])):
                hex_string = matrix[row][column]
                ascii_string = chr(int(hex_string, 16))
                print(ascii_string, end='')

    print()

    print("Cipher Text In Hex: ", end="")
    for matrix in encrypted_matrix_list:
        matrix = matrix.transpose()
        for row in range(len(matrix)):
            for column in range(len(matrix[row])):
                print(matrix[row][column], end='')

    print()
    print()

    #DECRYPTION

    decrypted_matrix_list = []

    start_of_decryption = time.time()
    for k in range(len(encrypted_matrix_list)):
        decrypted_matrix = decrypt(encrypted_matrix_list[k], all_round_keys)
        decrypted_matrix_list.append(decrypted_matrix)
    end_of_decryption = time.time()

    print("Deciphered Text In ASCII: ", end='')
    for matrix in decrypted_matrix_list:
        matrix = matrix.transpose()
        for row in range(len(matrix)):
            for column in range(len(matrix[row])):
                hex_string = matrix[row][column]
                ascii_string = chr(int(hex_string, 16))
                print(ascii_string, end='')

    print()

    print("Deciphered Text In Hex: ", end='')

    for matrix in decrypted_matrix_list:
        matrix = matrix.transpose()
        for row in range(len(matrix)):
            for column in range(len(matrix[row])):
                print(matrix[row][column], end='')

    print()
    print()

    #EXECUTION TIME

    print("Execution Time: ")
    print("Key Sceduling: ", end_of_key_scheduling - start_of_key_scheduling)
    print("Encryption Time: ", end_of_encryption - start_of_encryption)
    print("Decryption Time: ", end_of_decryption - start_of_decryption)