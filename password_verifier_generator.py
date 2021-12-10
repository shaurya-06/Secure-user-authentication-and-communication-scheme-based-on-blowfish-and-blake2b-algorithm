def function_G(initial_seed):
    G = 223
    x = int(initial_seed, 16)
    x = str(x)
    N = 36389
    result = ''
    for i in x:
        result += str(pow(G, int(i)) % N)
    return result
