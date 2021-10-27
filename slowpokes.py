with open("slow.txt", "r") as f:
    sets = list(map(set, (s.rstrip("\n").split(" ") for s in f.readlines())))

print("solo slow:", *(s[0] for s in sets if len(s) == 1))
