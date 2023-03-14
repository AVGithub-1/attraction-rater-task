rows = ['a','b','c','d','e','f','g','h','i']

fullArray = [(i+str(j) for j in range(1,101)) for i in rows]
for i in rows:
    print('')
    for j in range(100):
        fullArray.append(i + str(j+1))

print (fullArray)