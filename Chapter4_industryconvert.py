def convert(i):
    if (i in range(1,12)) or (i in range(13,52)) or (i in range(53,64)) or (i in range(65,69)) or (i in range(70,79)):
        return i
    elif (i in [12,52,64,80,81,94]) or (i in range(83,92)):
        return i-1
    elif i == 69:
        return 66
    elif i == 79:
        return 70
    elif i == 82:
        return 80
    elif i in [92,93,95,96]:
        return 90
