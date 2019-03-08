def myAtoi(str):
    """
    :type str: str
    :rtype: int
    """
    if str == '\0': return 0
    lstr = [each for each in str]

    i = 0
    flag = 0
    ban = 0

    for each in lstr:
        if flag ==0 and i == 0 and  ban == 0 and each == ' ':
            continue # 开头为空
        else:
            if flag == 0 and i == 0 and ban == 0and (each <'0'or each >'9'):
                if each == '+': flag = 1
                elif each == '-': flag = -1
                else: return 0  # 第一个非空字符
            else:
                if  each < '0' or each >'9':
                    break
                else:
                    i = i *10  + int(each)
                    ban = 1

    if flag == 0:
        flag = 1
    result = flag * i
    if result > 2 ** 31 - 1:
        return 2 ** 31 - 1
    elif result < -2 ** 31:
        return -2 ** 31
    else:
        return result

'''        if each == ' ':
            continue
        elif flag == 0 and each == '+' or each == '-':
            if each == '+':
                flag = 1
            else:
                flag = -1
        elif (i != 0 or  flag != 0) and (each > '9' or each < '0') :
            break
        else:
            if flag == 0 and each > '9' or each < '0':
                continue
            else:
                i = i * 10 + int(each)

    if flag == 0:
        flag = 1
    result = flag * i
    if result > 2 ** 31 - 1:
        return 2 ** 31 - 1
    elif result < -2 ** 31:
        return -2 ** 31
    else:
        return result'''


if __name__ == '__main__':
    s = "0  123"
    print(myAtoi(s))
