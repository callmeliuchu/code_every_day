def uv_load():
    ans = []
    with open('uv','r') as f:
        for line in f.readlines():
            arr = line.strip().split(' ')
            a = float(arr[0])
            b = float(arr[-1])
            ans.append([a,b])




def mat_load():
    ans = []
    with open('mat','r') as f:
        for line in f.readlines():
            arr = line.strip().split(' ')
            ans.append([float(v) for v in arr])
    return ans

print(mat_load())
