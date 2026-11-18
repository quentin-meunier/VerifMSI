
l = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']


n = 3

def tuple_enum_rec(s, l, tuple_len, i):
    if i == len(l):
        print(' '.join(list(s)))
    else:
        if len(s) < tuple_len:
            s.add(l[i])
            tuple_enum_rec(s, l, tuple_len, i + 1)
            s.remove(l[i])
        if tuple_len - len(s) < len(l) - i:
            tuple_enum_rec(s, l, tuple_len, i + 1)


s = set()

tuple_enum_rec(s, l, n, 0)



