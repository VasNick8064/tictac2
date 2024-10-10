def even_chars(st):
    if len(st)>100 or len(st)<2:
        return "invalid string"
    return [st[i] for i in range(1,len(st),2)]

print(even_chars([]))
#["b", "d", "f", "h", "j", "l"]