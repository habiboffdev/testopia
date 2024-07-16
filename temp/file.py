from math import isqrt
def masala1():
    n = int(input())
    x = 1
    for i in range(2,isqrt(n)+1):
        if n%i == 0:
            x+=i
            x+=n/i
    if x == n:
        print("Yes")
    else:
        print("No")
def masala2():
    arr = input().split('-')
    arr.sort()
    print('-'.join(arr))
def masala3():
    n = int(input())
    dp = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(i+1):
            if i == j or j == 0:
                dp[i][j] = 1
            else:
                dp[i][j] = dp[i-1][j-1]+dp[i-1][j]
    for i in range(n)   :
        for j in range(i+1):
            print(dp[i][j],end=" ")
        print()
