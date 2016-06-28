import urllib.request
import re

def get_rate():
    url = "http://data.bank.hexun.com/other/cms/fxjhjson.ashx?callback=PereMoreData"
    req = urllib.request.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')
    opener = urllib.request.build_opener()
    f = opener.open(req)
    t = f.read().decode('GBK')
    m = re.findall(r"\{(.*?)\}", t)
    rate = []
    for each in m:
        d = {}
        temp = each.split(',')
        d["currency"] = temp[0].split(':')[1][1:-1]
        d["refePrice"] = temp[1].split(':')[1][1:-1]
        d["code"] = temp[2].split(':')[1][1:4]
        rate.append(d)
    return rate


def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False


def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
        return True
    else:
        return False


def check_rate(cId):
    rate = get_rate()
    flag = 0
    if is_chinese(cId):
        for d in rate:
            if cId == d['currency']:
                print('100 %s（%s）= %s CNY' % (d["currency"], d["code"], d["refePrice"]))
                print('1 CNY = %.3f %s（%s）' % (100 / float(d["refePrice"]), d["currency"], d["code"]))
                flag = 1
    elif is_alphabet(cId):
        for d in rate:
            if cId == d['code']:
                print('100 %s（%s）= %s CNY' % (d["currency"], d["code"], d["refePrice"]))
                print('1 CNY = %.3f %s（%s）' % (100 / float(d["refePrice"]), d["currency"], d["code"]))
                flag = 1
    if flag == 0:
        print("输入错误")
if __name__ == '__main__':
    type = input("请输入要转换的币种：按'#'键退出：")
    while type != '#':
        check_rate(type)
        type = input("请输入要转换的币种，按'#'键退出：")
    print("谢谢使用")