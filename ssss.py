# Written by Henry Dau
# Date: 4/5/2017

# Pseudocode from https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing

email_available = False;
BE_FANCY = True;

import random
import getpass
try:
    import message3 as email
    email_available = True;
except:
    print "No email available"

prime = 257;
#prime = 982451653

# Split number into the shares
def split(number, available, needed):
    shares = []

    # Generate random coefficients
    coefficients = [number]
    for c in range(1, needed):
        coefficients.append(int(random.random() * (prime  - 1)))

    for x in range(1, available+1):
        accum = coefficients[0]
        for exp in range(1, needed):
            accum = (accum + (coefficients[exp] * (pow(x, exp) % prime) % prime)) % prime

        shares.append([x, accum])

    return shares;

#Gives the decomposition of the gcd of a and b.  Returns [x,y,z] such that x = gcd(a,b) and y*a + z*b = x
def gcdD(a,b):
    if (b == 0):
        return [a, 1, 0]
    else:
        n = int(a/b)
        c = a % b
        r = gcdD(b,c)
        return [r[0], r[2], r[1] - r[2] * n]

# Gives the multiplicative inverse of k mod prime.  In other words (k * modInverse(k)) % prime = 1 for all prime > k >= 1
def modInverse(k):
    k = k % prime;
    r = -gcdD(prime,-k)[2] if (k < 0) else gcdD(prime,k)[2];
    return (prime + r) % prime;

# Join the shares into a number
def join(shares):
    accum = 0
    for formula in range(0, len(shares)):

        numerator = 1;
        denominator = 1;
        for count in range(0, len(shares)):
            if (formula == count):
                continue; # If not the same value
            startposition = shares[formula][0]
            nextposition = shares[count][0]
            numerator = (numerator * -nextposition) % prime
            denominator = (denominator * (startposition - nextposition)) % prime

        value = shares[formula][1]
        accum = (prime + accum + (value * numerator * modInverse(denominator))) % prime

    return accum;

def hexify(keys):
    new_keys = [];
    for key in keys:
        new_keys.append(hex(key[1] * 100 + key[0])[2:])

    return new_keys


while 1:
    print "Generate key (1) or decode (2)?"
    ans = raw_input()
    if (ans == '1'):

        secret = getpass.getpass('Secret number (must be less than ' + str(prime) + '): ')
        #keys_generated = 3;
        #keys_needed = 2;

        print "Please enter the number of keys to generate: "
        keys_generated = int(raw_input());

        print "Please enter the number of keys needed to decode the message (< " + str(keys_generated) + "): "
        keys_needed = int(raw_input());

        # The encoded number is the first argument to the function
        # Second argument is number of keys to generate
        # Third argument is the number of keys needed to decode the message
        shs = split(int(secret), keys_generated, keys_needed)
        if (BE_FANCY):
            shs = hexify(shs);

        if (email_available):
            for i in range (0, keys_generated):
                print "Send to: "
                TO = raw_input()
                if (TO == "print"):
                    print shs;
                    break;
                if (TO == ""):
                    email.sendMessage(TO, str(shs[i:]))
                    break;
                email.sendMessage(TO, str(shs[i]))

                print "Message sent!\n"
        else:
            print shs

        print "All keys sent"
    elif (ans == '2'):

        keys = []
        while 1:
            print "Please enter a key: "
            key = raw_input();
            if (key == ""):
                break
            elif (key == "-"):
                print "Removing last key"
                keys = keys[0:-1]
            else:
                if (BE_FANCY):
                    num = int(key, 16)
                    keys.append(eval('[' + str(num % 100) + ', ' + str(int(num / 100)) + ']'))
                else:
                    keys.append(eval(key))

        print "Decoded message: " + str(join(keys))
    elif (ans == 'be fancy'):
        print "Alright, lets clean those keys up"
        BE_FANCY = True;
    elif (ans == 'dont be fancy'):
        print "Sounds good, make it easier to see why this is so cool"
        BE_FANCY = False;
    elif (ans == ""):
        print "Done!"
        break;
