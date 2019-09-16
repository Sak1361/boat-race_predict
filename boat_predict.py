import openpyxl
import string as stg
import requests, re, sys, os, time
from bs4 import BeautifulSoup
import openpyxl as opxl

class Scraping_page:
    def __init__(self,data,rno):
        self.page = rno
        self.date = data
        self.dir_name = f'fukuoka_{data}'
        self.scrape_cls = ['racer_name','boat_result','boat_course',
        'course_result','course_winning_tech','pool_result']

    def crawling(self):
        #レース情報URL
        url = f'https://www.boatrace.jp/owpc/pc/race/racelist?rno={self.page}&jcd=22&hd={self.date}'
        #ディレクトリ作成部
        race_num = f'{self.page}R'
        if not os.path.exists(f'{self.dir_name}/{race_num}'):
            os.mkdir(f'{self.dir_name}/{race_num}')
        f_name = f'{self.dir_name}/{race_num}/{race_num}.html'
        #ページ保存部
        self.craw_init(url,f_name)
        ##個人成績取得
        html = open(f_name,'r')
        soup = BeautifulSoup(html, "html.parser")
        racer_n = 1
        for boat_number in soup.find_all(class_="is-fs11"):
            print(boat_number.text)
            print(len(boat_number.text))
            
            if len(boat_number.text) > 11:
                continue
            f_racer = f'{self.dir_name}/{race_num}/boat_{racer_n}.html'
            print(boat_number)
            print()
            b_num = re.sub('[ /]','',boat_number.text)
            print(b_num)
            b_num = int(b_num+" ")
            """try:
                #b_num = int( boat_number.find('p').text )
                b_num = re.sub('[ /]','',boat_number.text)
            except ValueError:  #最後は文字列なのでbreak
                print(f"{race_num}取得")
                break
            """
            url_recer = f"http://www.boatrace-db.net/racer/yresult/regno/{b_num}/year/2019/"  #選手情報（期別から検索
            self.craw_init(url_recer,f_racer)
            time.sleep(2) #時間を開けないとダメだってさ
            print(f'{race_num}R-{racer_n}人目取得')
            racer_n += 1
        #ページ遷移
        self.page += 1
        if self.page > 12:
            self.page = 8
            return None
        elif self.page > 9:
            tmp_url = url[-19:] #レース番号以降を保持
            url = url[:-1] + str(self.page) + tmp_url
        else:
            tmp_url = url[-19:] #レース番号以降を保持
            url = url[:-2] + str(self.page) + tmp_url
        html.close()    #ちゃんと閉じます
        self.crawling()

    def craw_init(self,url,f_name):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(url,headers=headers)
        response.encoding = response.apparent_encoding
        with open(f_name,'w',encoding="utf-8") as f:
            f.write(response.text)

    def open_html(self,dir_p):
        try:
            #with open(dir_p,'r') as f:
            #    html = f
            html = open(dir_p,'r')
        except FileNotFoundError:
            print("File not found.")
            return None    
        return html

    def scrap_racer(self,race):
        res = []
        for racer in range(1,7):
            dir_p = f"{self.dir_name}/{race}R/boat_{racer}.html"
            html = self.open_html(dir_p)
            soup = BeautifulSoup(html, "html.parser") 
            for cnt in range(6):    #名前と成績を取得
                if cnt==5:  #福岡勝率だけ抜き出す
                    j = 1
                    tmp_cls = soup.find(class_=self.scrape_cls[cnt])
                    strings = tmp_cls.find(class_='header').text
                    for b in tmp_cls.find_all(class_='even'):
                        if j==11:
                            b = b.text
                            strings = strings + b
                            res.append(self.shaping(strings))
                            j += 1
                        else:
                            j += 1
                else:
                    strings = soup.find(class_=self.scrape_cls[cnt]).text  #タグが入るのでtext
                    res.append(self.shaping(strings))

        return res

    def shaping(self,strings):
        tmp_res = []
        strings = strings.replace(' ','') #空白除去
        strings = strings.split('\n')
        for i in strings:    #空文字除去
            if i != '':
                tmp_res.append(i)
        return tmp_res



class Write_excel:
    def __init__(self):
        self.vert1 = 2
        self.vert2 = 3
        self.hori1 = 2
        self.hori2 = 2
        self.capa = 0
        self.alph = list(stg.ascii_uppercase)    #ABCのリスト

    def write_xl(self,data,xls):
        hori_n = 1
        if len(data) == 1:
            al = self.alph[hori_n-1]
            data = re.sub(r'[!-~\s+]','',data[0]) #空白文字が混ざってる時があるので除く
            xls[f'{al}{self.vert1}'].value = data
            self.capa = 0
        else:
            c = 0
            count = 0
            for s in data:
                #judge=10 if len(data)>56 else 9
                if not c:
                    c = 1
                    if len(data)>56:
                        judge = 10
                    elif len(data)<40:
                        judge = 12
                    else:
                        judge = 9
                    if self.capa:
                        tmp_h = self.hori1      #横に滑るので値の入れ替え
                        self.hori1 = self.hori2 + 2
                        self.hori2 = tmp_h
                        tmp_v = self.vert1
                        self.vert1 = self.vert2
                        self.vert2 = tmp_v
                        judge += self.hori1
                        self.capa = 0
                    else:
                        self.capa = 1
                        self.vert1 = self.vert2
                        self.hori1 = self.hori2

                if self.hori1 > judge:
                    self.hori1 -= count
                    self.vert1 += 1
                    count = 0

                if int(self.hori1/len(self.alph)):
                    al = f'A{self.alph[(len(self.alph)+1)-self.hori1]}'
                else:
                    al = self.alph[self.hori1-1]
                try:
                    s = int(s)  #なるだけ数字はintに
                except ValueError:
                    pass
                xls[f'{al}{self.vert1}'].value = s
                self.hori1 += 1
                count += 1
            self.capa = 1
            self.vert1 += 1  #表のあとに1列空ける
        self.vert1 += 1
        self.hori2 = self.hori1     #2つ目用に値を移行
        self.hori1 = 2
        return xls

if __name__ == "__main__":
    day = sys.argv[1]
    race_number = int(sys.argv[2])
    if not os.path.exists('fukuoka_'+day):
        os.mkdir('fukuoka_'+day)
    scrape = Scraping_page(int(day),race_number)
    excel = Write_excel()                
            
    scrape.crawling()    #クローリング
    data_boat = ''
    xl = opxl.Workbook()   #新規作成
    xs = xl.active    #シート指定
    xs.title = "demo"  #シート名変更
    xs['A1'].value = f'【福岡 {race_number}R】'
    for num in range(race_number,13):
        for data in scrape.scrap_racer(num):
            xs = excel.write_xl(data,xs)
    xl.save("/Users/sak1361/repository/boat_race/a.xlsx")   #保存

    #ws = wb.get_sheet_by_name('SHEETNAME') #SHEETNAMEを検索して指定

    #進入コース boat_course
    # コースリザ    course_result
    # 決まり手  course_winning_tech
    #開催場の勝率　pool_result even (11ばんめが福岡)
    
    #http://www.boatrace-db.net/racer/yresult/regno/4444/year/2019/     各選手 期別と年指定
    #http://www.boatrace-db.net/race/index/      ホーム　当日開催分表示or過去分検索
    #http://www.boatrace-db.net/race/races/date/20190901/pid/22/        日付と福岡22で当日のレース情報
    #http://www.boatrace-db.net/race/detail/date/20190901/pid/22/rno/01/    日付、開催番号、レース番号

    #http://www.boatrace-db.net/stadium/motor/pid/22/   モータ勝率  下記のトップ
    #http://www.boatrace-db.net/stadium/boat/pid/22/    ボート
    #http://www.boatrace-db.net/stadium/tcourse/pid/22/     コース別総合
    #http://www.boatrace-db.net/stadium/ccourse/pid/22/     条件別（風やSG
    #http://www.boatrace-db.net/stadium/result/pid/22/      出目
    #http://www.boatrace-db.net/stadium/demo/pid/22/        展示タイム別

#ボートレース公式サイト
    #https://www.boatrace.jp/owpc/pc/extra/data/download.html   公式の選手成績
    #https://www.boatrace.jp/owpc/pc/race/racelist?rno=1&jcd=22&hd=20190916     rno=レースnum,jcd=開催状,hd=年日
    # https://www.boatrace.jp/owpc/pc/race/index?hd=20190916    レース一覧
    #https://www.boatrace-fukuoka.com/modules/datafile/?page=index_mrankdtl&kind=1&type=1   福岡モータ成績
    #https://www.boatrace-fukuoka.com/modules/datafile/?page=index_tanpyou  選手別戦評（多分当節のみ
    #

    '''
    レース場	場コード
    桐生	01
    戸田	02
    江戸川	03
    平和島	04
    多摩川	05
    浜名湖	06
    蒲郡	07
    常滑	08
    津	09
    三国	10
    びわこ	11
    住之江	12
    尼崎	13
    鳴門	14
    丸亀	15
    児島	16
    宮島	17
    徳山	18
    下関	19
    若松	20
    芦屋	21
    福岡	22
    唐津	23
    大村	24
    '''
