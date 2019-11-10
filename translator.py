from fuzzywuzzy import process
from yandex.Translater import Translater

tr = Translater()
tr.set_key('trnsl.1.1.20191110T032857Z.5cb504ab3196bc0f.e222fb57077985f5bc174f9f7b8ff5622b83d7ed') # Api key found on https://translate.yandex.com/developers/keys

def tran(text_from_user, to_lang, tr):
    tr.set_from_lang('th')
    tr.set_to_lang('en')
    tr.set_text(text_from_user)
    text_output = tr.translate()
    return (text_output)

def check_lang(Input):
    corpus = {
        'fr' : ['france','ฝรั่งเศส'], #90
        'de' : ['german','deutsch','เยอรมันนี'], #36
        'en' : ['english','อังกฤษ','อิ้ง'] #67
    }
    best_match = ''
    highest_score = 0
    for key,value in corpus.items():
        out = process.extractOne(Input, value)
        if out[1] > highest_score:
            highest_score = out[1]
            best_match = key
        else :
            continue
    return best_match

# while True:
#     in1 = input("Word: ")
#     lang = check_lang(in1)
#     in2 = input("Choose Language: ")
#     result = tran(in1, in2)
#     print(result)