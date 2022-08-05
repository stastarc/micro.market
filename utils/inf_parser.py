
# 난이도:쉬움
# 높이:40cm
# 수명:다년생

def parseinf(raw_inf: str):
    inf_list = raw_inf.split('\n')
    inf_dict = {}
    for inf in inf_list:
        i = inf.index(":")
        inf_dict[inf[:i]] = inf[i+1:]
    return inf_dict

def encodeinf(inf_dict: dict[str, str]):
    inf_list = []
    for key, value in inf_dict.items():
        inf_list.append(f"{key.replace(':', '')}:{value}")
    return '\n'.join(inf_list)