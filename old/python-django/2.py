n = int(input())
ans = 0
old_a, old_b = None, None
for idx in range(n):
    a, b = map(int, input().split())
    ans += (b - a) * 2 + 2 # adding all rectangle
    if old_a and old_b:
        st = max(old_a, a)
        en = min(old_b, b)
        if(st < en):
            ans -= (en - st) * 2
    old_a, old_b = a, b
    
print(ans)