from random import expovariate
res = {}
for i in range(1000):
    r = int(expovariate(1.0))
    if r in res:
        res[r] += 1
    else:
        res[r] = 1
keys = sorted(res.keys())
for key in keys:
    print(key, '-' * res[key])
