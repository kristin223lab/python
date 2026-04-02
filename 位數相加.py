def f(n):
    while(n >= 10):
        total = 0
        for ch in str(n):
            total += int(ch)
        n = total
    return n


while(True):
    a = input("請輸入數字： ")
    
    if not a.isdigit():
        print("輸入錯誤請重新輸入")
        continue

    n = int(a)
    if(n == 0): break

    if n < 1 or n > 1000000000:
        print("輸入錯誤請重新輸入")
        continue

    print("Answer: ",f(n))

