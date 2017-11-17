import pickle, base64, getpass

def initiate_user():

    f = open('credentials.dat', 'wb')
    d = {}

    user = raw_input("Username for SNU NET ID: ")
    passw = getpass.getpass("Password: ")

    user = base64.b64encode(user)
    passw = base64.b64encode(passw)

    print "Registered!!"

    d.update({'username':user, 'password': passw})
    pickle.dump(d, f)

    f.close()

def authenticate():
    f = open('credentials.dat', 'rb')
    try:
        while True:
            d = {}
            d = pickle.load(f)
            if d == {}:
                first_time = True
            else:
                first_time = False
    except:
        f.close()

    return first_time


def check(bool_value):
    if bool_value == True:
        initiate_user()
        return 0
    else:
        f = open('credentials.dat', 'rb')
        try:
            while True:
                d = {}
                d = pickle.load(f)
                user = base64.b64decode(d['username'])
                passw = base64.b64decode(d['password'])
        except:
            f.close()

        return user, passw


def USER():

    auth = authenticate()

    further_check = check(auth)

    if not further_check:
        user, passw = check(False)
    else:
        user, passw = further_check[0], further_check[1]


    return user, passw
