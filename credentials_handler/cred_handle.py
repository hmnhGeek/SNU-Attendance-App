def reset():
    f = open('credentials.dat', 'wb')
    from pickle import dump

    dump({}, f)
    f.close()
