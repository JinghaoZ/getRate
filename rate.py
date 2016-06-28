import urllib.request
import re
import hashlib
import xml.etree.ElementTree as ET
import web

class Rate:
    def GET(self):
        data = web.input()
        echostr = data.echostr
        timestamp = data.timestamp
        nonce = data.nonce
        signature = data.signature
        token = 'zjh0815xl'
        lista = [token, timestamp, nonce]
        sorta = sorted(lista)
        stra = "".join(sorta)
        sha1a = hashlib.sha1(stra).hexdigest()
        if sha1a == signature:
            return echostr
        else:
            return "error"

    def POST(self):
        data = web.data()
        root = ET.fromstring(data)
        fromUser = root.findtext(".//FromUserName")
        toUser = root.findtext(".//ToUserName")
        CreateTime = root.findtext(".//CreateTime")
        MsgType = root.findtext(".//MsgType")
        Content = root.findtext(".//Content")
        Content = Content.encode('UTF-8')
        d = self.checkRate(Content)
        if d == -1:
            pdata_text = "输入错误"
        else:
            pdata_text = '100 %s（%s）= %s CNY' % (d["currency"], d["code"], d["refePrice"]) + '1 CNY = %.3f %s（%s）' % (100 / float(d["refePrice"]), d["currency"], d["code"])
        texttpl = '''<xml>
            <ToUserName>''' + fromUser + '''</ToUserName>
            <FromUserName>''' + toUser + '''</FromUserName>
            <CreateTime>''' + CreateTime + '''</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content>''' + pdata_text + '''</Content>
            </xml>'''
        return texttpl

    def getRate(self):
        url = "http://data.bank.hexun.com/other/cms/fxjhjson.ashx?callback=PereMoreData"
        req = urllib.request.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')
        opener = urllib.request.build_opener()
        f= opener.open(req)
        t = f.read().decode('GBK')
        m = re.findall(r"\{(.*?)\}",t)
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

    def checkRate(self,cId):
        rate = self.getRate(self)
        if self.is_chinese(cId):
            for d in rate:
                if cId == d['currency']:
                    return d
                    '''
                    print('100 %s（%s）= %s CNY' % (d["currency"], d["code"], d["refePrice"]))
                    print('1 CNY = %.3f %s（%s）' % (100 / float(d["refePrice"]), d["currency"], d["code"]))
                 '''

        elif self.is_alphabet(cId):
            for d in rate:
                if cId == d['code']:
                    return d
                    '''
                    print('100 %s（%s）= %s CNY' % (d["currency"], d["code"], d["refePrice"]))
                    print('1 CNY = %.3f %s（%s）' % (100 / float(d["refePrice"]), d["currency"], d["code"]))
                 '''

        else:
            return -1




