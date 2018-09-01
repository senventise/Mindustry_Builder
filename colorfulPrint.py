# 彩色输出
def generate(content, color):
    content = str(content)
    color = str(color)
    start = ("\033[0;"+color+";40m")
    end = "\033[0m"
    out = (start+content+end)
    return out