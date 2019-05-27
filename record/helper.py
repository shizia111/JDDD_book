# 京东 papa
import requests
from lxml import etree
import time

class JDDD:
    def __init__(self,book_name,page=1):
        self.page=page
        self.book_name = book_name
        self.data_list = []
    def JD(self):
        url = 'https://search.jd.com/Search'
        headers = {
            'User-Agent': '"Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"',
            'Connection': 'close',
        }
        params = {
            'keyword': f'{self.book_name}',
            'enc': 'utf-8',
            'qrst': "1",
            'rt': "1",
            'stop': 'stop',
            "vt": "2",
            'suggest': '1.his.0.0',
            'page': f'{self.page}',
            "s": "60",
            'click': '0'
        }
        html = requests.get(url, params=params, headers=headers)
        tree = etree.HTML(html.content)
        info = tree.xpath('//*[@id="J_goodsList"]/ul/li')
        pag = tree.xpath('//*[@id="J_bottomPage"]/span[2]/em[1]/b/text()')
        print(pag)
        for i in info:
            title = i.xpath('./div/div[@class="p-img"]/a/@title')[0]
            img_url = i.xpath('./div/div[@class="p-img"]/a/img/@source-data-lazy-img')[0]
            price = i.xpath('./div/div[@class="p-price"]/strong/i/text()')[0]
            url = i.xpath('./div/div[@class="p-commit"]/strong/a/@href')[0]
            url = f'https:{url}' if 'http' not in url else url
            img_url = f'https:{img_url}' if 'https' not in img_url else img_url
            res = requests.get(url, params=params, headers=headers)
            trees = etree.HTML(res.text)
            data = trees.xpath('//ul[@id="parameter2"]/li/@title')
            if '\n  ' in data: data.remove('\n  ')
            tit = trees.xpath('//ul[@id="parameter2"]/li/text()')
            tit = [i.split('：')[0] for i in tit]
            if '\n    ' in tit:tit.remove('\n    ')
            data = {tit[i]: v for i, v in enumerate(data)}
            user = trees.xpath('//*[@id="p-author"]/a/text()')
            dic_info = {
                'name': title,
                'url': url,
                'user': user,
                'img': img_url,
                'terrace': '京东',
                'price': price,
                'info': data
            }
            self.data_list.append(dic_info)
        return self.data_list
    def dangdang(self):
        url = "http://search.dangdang.com/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        }
        params = {
            "key": self.book_name,
            "act": "input",
            "page_index": None

        }

        ret = requests.get(url=url, params=params, headers=headers).text
        tree = etree.HTML(ret)
        pag = tree.xpath('//a[@name="bottom-page-turn"]/text()')
        if pag:
            pag = int(pag[-1])
        else:
            pag = 2
        for now_pag in range(1, pag):
            params["page_index"] = now_pag
            rea = requests.get(url=url, params=params, headers=headers).text

            tree = etree.HTML(rea)
            url_list = tree.xpath('//ul[@id="component_59"]/li/a/@href')

            for i in url_list:
                ref = requests.get(url=i, headers=headers).text
                tree = etree.HTML(ref)
                tit = tree.xpath('//ul[@class="key clearfix"]/li/text()')
                tit = [i.split('：') for i in tit]
                name =tree.xpath('//div[@class="name_info"]/h1/@title')[0] if tree.xpath('//div[@class="name_info"]/h1/@title') else '暂无数据'
                img= tree.xpath('//img[@id="largePic"]/@src')[0] if tree.xpath('//img[@id="largePic"]/@src') else '暂无数据'
                price = tree.xpath('// *[@id="dd-price"]/text()')[-1].strip() if tree.xpath('// *[@id="dd-price"]/text()') else '暂无数据'
                dic = {
                    'name': name ,
                    'url':i,
                    'user': "".join(tree.xpath('//span[@id="author"]//text()')).replace("\u3000", ""),
                    'img': img,
                    'terrace':'当当',
                    'price': price,
                    'info':{i[0]:"否"  if not i[1] else i[1] for i in tit }
                }

                self.data_list.append(dic)
            return self.data_list


