
def interp(t, list1, list2):
    if len(list1) != len(list2):
        raise ValueError('list1 and list2 must have same length')

    zipped = zip(list1, list2)

    for a, b in zipped:
        yield int(a + t * (b - a))


if __name__ == '__main__':
    l1 = (1, 2, 3)
    l2 = (4, 5, 6)
    o,t,i = interp(2, l1, l2)
    print(o)

