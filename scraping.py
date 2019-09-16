from bs4 import BeautifulSoup
import MeCab, sys, re, mojimoji

def scrape():
    strings = ''
    for page in range(1,10):
        try:
            html = open("nega-posi/positive_{0}.html".format(page),'r')
        except FileNotFoundError:
            break
        soup = BeautifulSoup(html, "html.parser")
        for res in soup.find_all(class_="description"):
            strings += res.find('p').text + '\n'
    return strings

def labeling(words):
    tagger = MeCab.Tagger('-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
    tagger.parse('')
    data = ''
    label = "__label__positive, "
    re_word = re.compile(r"[!-~︰-＠…‥、。！？「」・”]")
    re_num = re.compile(r"[0-9]")
    words = words.split('\n')
    for line in words:
        if line:
            if re_num.match(line):
                line = mojimoji.han_to_zen(line, ascii=False)
            line = re_word.sub(' ',line)
            line = tagger.parse(line)
            data += label + line
    return data

if __name__ == "__main__":
    path = sys.argv[0]
    word = scrape()
    with open(path,'w') as f:
        f.write(labeling(word))
