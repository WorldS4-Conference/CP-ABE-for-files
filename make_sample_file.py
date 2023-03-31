with open("files/numbers.txt", "w") as f:
    i = 1
    while True:
        f.write(str(i) + "\n")
        if f.tell() > 1000 * 1000 * 2:
            break
