category=['Ja','Ma','En','So','Sc','Mu','Ar']
score=[35,15,20,30,25,15,25]
multiplier=[
    [1,1,2,3,5,8,13],
    [1,5,9,13,17,21,25],
    [1,5,8,12,15,19,22],
    [1,3,5,7,9,11,13],
    [1,2,4,6,8,10,12],
    [1,4,6,9,11,14,16],
    [1,2,2,3,5,8,11],
]

def sumscore(retsu):
    total = 0
    for i in range(7):
        total += score(retsu[i])
    return total

