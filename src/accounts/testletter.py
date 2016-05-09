
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
translate = {u'ą':'a', u'ć':'c', u'ę':'e', u'ł':'l', u'ń':'n', u'ó':'o', u'ś':'s', u'ż':'z', u'ź':'z'}


def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

if __name__ == '__main__':
    dic = replace_all(text="Paweł Stępak", dic=translate)
    print(dic)