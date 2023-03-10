# K=input('Enter key : ')
K="00111010100101001101011000111111"                                    # key 32bits
def split_bin(s): return [l for l in s]                                 # spilt the key in to 32 element
# extract 16 elements to form key
def get_sub_key(K, r): return K[4*r-4:4*r+12]


S_key = split_bin(K)

# displays the 5 keys
for i in range(1, 6):                                                   # for loop to extract the 5 keys for the given 32 bits key
    K_i = get_sub_key(K, i)                                             # key1 to key5


# Addition of two lists                                                        #to add the result of addition column by column
def addition(N, M):
    listi = []
    for i in range(len(M)):
        tmp = int(N[i], 2) ^ int(M[i], 2)
        tmp = bin(tmp)
        listi.append(tmp.replace("0b", ''))
    return listi


# S-box
# list containing hexadecimal notation
hexa_list = [hex(i) for i in range(0, 16)]

# Subs_list is a substitution of hexa_list
N = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5,
     9, 0, 7]                                                               # order of index in the substitution
Subs_list = [hex(j) for j in N]

# apply S-box in the list


def apply_S_box(a):
    for i in range(len(a)):
        k = hexa_list.index(a[i])
        a[i] = Subs_list[k]
    return a


# inverse of the S-box 
def inverse_S_box(a):
    for i in range(len(a)):
        k = Subs_list.index(a[i])
        a[i] = hexa_list[k]
    return a


# permutation

def permutation(L):
    ind_per = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
    i = 0
    L_new = []
    for i in range(16):
        L_new.append(L[ind_per[i]])
    return L_new


# Convertion of a list containing string character in hex
def conv_hex(a):
    a_n = ''.join(a)
    a = int(a_n, 2)
    return hex(a)

# Convert a list of string of hexa element to a split of each character on each component


def convert_bin(L):
    N = []
    for i in range(len(L)):
        a = int(L[i], 16)
        a = bin(a)
        a = a.replace('0b', '')
        if len(a) < 4:
            a = '0'*(4-len(a))+a
        a = split_bin(a)
        N = N+a
    return N


###########################  E  N  C  R  Y  P  T  I  O  N  #######################################
def spn_encrypt(msg, K):
    msg = split_bin(msg)
    for i in range(3):
        msg = addition(msg, get_sub_key(K, i+1))
        print(i+1, ''.join(msg))
        msg = [conv_hex(msg[0:4]), conv_hex(msg[4:8]),
               conv_hex(msg[8:12]), conv_hex(msg[12:16])]
        msg = apply_S_box(msg)
        msg = convert_bin(msg)
        print('s', ''.join(msg))
        msg = permutation(msg)
        print('p', ''.join(msg),'\n')
    msg = addition(msg, get_sub_key(K, 4))
    print(4,''.join(msg))
    msg = [conv_hex(msg[0:4]), conv_hex(msg[4:8]),
           conv_hex(msg[8:12]), conv_hex(msg[12:16])]
    msg = apply_S_box(msg)
    msg = convert_bin(msg)
    print('s',''.join(msg))
    msg = addition(msg, get_sub_key(K, 5))
    return ''.join(msg)



###########################  D  E  C  R  Y  P  T  I  O  N  #######################################
def spn_decrypt(msg, K):
    msg = split_bin(msg)
    msg = addition(msg, get_sub_key(K, 5))
    print(5, ''.join(msg))
    msg = [conv_hex(msg[0:4]), conv_hex(msg[4:8]),conv_hex(msg[8:12]), conv_hex(msg[12:16])]
    msg = inverse_S_box(msg)
    msg = convert_bin(msg)
    print('s',''.join(msg),'\n')
    for i in range(3,0,-1):
        msg = addition(msg, get_sub_key(K, i+1))
        print(i+1, ''.join(msg))
        msg = permutation(msg)
        print('p', ''.join(msg))
        msg = [conv_hex(msg[0:4]), conv_hex(msg[4:8]),conv_hex(msg[8:12]), conv_hex(msg[12:16])]
        msg = inverse_S_box(msg)
        msg = convert_bin(msg)
        print('s', ''.join(msg),'\n')
    msg=addition(msg, get_sub_key(K, 1))
    return ''.join(msg)

#msg = '0010011010110111'


msg = '0010011010110111'
print(' E N C R Y P T I O N ','\n')
y=spn_encrypt(msg, K)
print('y=',y)
print('=========================================')
print(' D E C R Y P T I O N ','\n')
print('x=',spn_decrypt(y, K))
