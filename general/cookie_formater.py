def format_cookie(s):
    cokie_json = {}
    li = s.split(';')
    for ele in li:
        ele = ele.strip().split('=')
        if len(ele) == 2:
            name = ele[0]
            value = ele[1]
            cokie_json[name] = value
    print("sucessfully refactord cookies")
    return cokie_json
