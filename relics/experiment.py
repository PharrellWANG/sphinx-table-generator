from data import data

if __name__ == "__main__":
    arg_data = data if data else [['No Data']]
    table = []

    list_outer = []
    for member in arg_data:
        list_inner = []
        for elt in member:
            list_inner.append(len(str(elt)))
        list_outer.append(list_inner)

    list_outer2 = [[len(str(elt)) for elt in member]
                   for member in arg_data]

    print list_outer
    print list_outer2

    # max size of each column
    zipped = zip(*[[len(str(elt)) for elt in member]
                   for member in arg_data])
    print zipped
    sizes = map(max, zipped)
    print 'End.'
