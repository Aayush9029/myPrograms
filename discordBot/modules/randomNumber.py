import random
def generaterandom(msg):
    if "from" in msg:
        m = msg.split()
        fr = m[m.index("from") + 1]
        to = m[m.index("to") + 1]
        return random.randint(int(fr), int(to))
    if "between" in msg:
        m = msg.split()
        fr = m[m.index("between")+1]
        to = m[m.index("and")+1]
        return random.randint(int(fr)+1,int(to)-1)
    return random.randint(1,6)
