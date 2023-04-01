with open("files/numbers.txt", "w") as f:
    i = 1
    while True:
        # f.write(str(i) + "\n")
        f.write("Indian Institute of Information Technology (IIIT) Kottayam ")
        if f.tell() > 1000 * 1000 * 2:
            break
