from calculator.models import City
from datetime import date

import lxml.html
import requests


class Calculator:
    PORT_UNLOAD_COST = 400.00
    BROKER_COST = 400.00

    def __init__(self, req):
        self._price = int(req.POST['price'])
        self._year = int(req.POST['year'])
        self._eng_type = req.POST['engine_type']
        self._eng_cc = float(req.POST['engine_cc'])
        self._kwh = int(req.POST['kwh']) if req.POST['kwh'] else 0
        self._auction_name = req.POST['auction_name']
        self._city = req.POST['city']
        self._company_fee = float(req.POST['company_fee'])

        self.auc_fee = self._calc_auc_fee()
        self.bank_fee = self._calc_bank_fee()
        self.ship_cost = self._calc_ship_cost()
        self.unload_cost = self.PORT_UNLOAD_COST
        self.broker_cost = self.BROKER_COST
        self.import_fee = self._calc_import_fee()
        self.total = self.auc_fee + self.bank_fee + self.ship_cost +\
                       self.unload_cost + self.broker_cost + self.import_fee

    def __call__(self):
        """returns the full price of the car, which includes customs fees, delivery, registration"""
        return {
                'price': self._price, 'auction_fee': self.auc_fee,
                'bank_fee': self.bank_fee, 'ship_cost': self.ship_cost,
                'port_unload': self.unload_cost, 'broker': self.broker_cost,
                'import_fee': self.import_fee, 'company_fee': self._company_fee,
                'total': self.total
                }

    def _calc_auc_fee(self):
        buyer_fee = self._price
        gate_fee = 0
        bid_fee = 0
        return round(buyer_fee + gate_fee + bid_fee, 2)

    def _calc_bank_fee(self):
        res = self._price * 0.005
        return 500 + 12 if res > 500 else res + 12

    def _calc_ship_cost(self):
        c = City.objects.filter(auction=self._auction_name, city=self._city)
        return float(c[0].price)

    def _calc_import_fee(self):
        if self._eng_type == 'ELECTRIC':
            return round(self._kwh * 1.02, 2)

        year_kof = self._calc_year_kof(self._year)
        engine_kof = self._calc_engine_kof(type=self._eng_type, cc=self._eng_cc)

        import_tax = self._price * 0.1
        excise_tax = engine_kof * self._eng_cc * year_kof
        vat = (import_tax + excise_tax + self._price) * 0.2
        return round(import_tax + excise_tax + vat, 2)

    @staticmethod
    def _calc_year_kof(year):
        kof = date.today().year - year - 1
        return 15 if kof > 15 else 1 if kof < 1 else kof

    @staticmethod
    def _calc_engine_kof(type, cc):
        if type == 'DIESEL':
            return 154.10 if cc > 3.5 else 77.05

        if type in ('GAS', 'HYBRID'):
            return 102.73 if cc > 3.0 else 51.37


class ScanData:
    RESPONSE_COPART = 'https://www.copart.com/public/data/lotdetails/solr/'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin'
    }

    ENGINE_TYPES = {
        'Gasoline': 'GAS',
        'Diesel': 'DIESEL',
        'Electric': 'ELECTRIC',
        'Hybrid': 'HYBRID'
    }

    def __init__(self, req):
        self._req = req
        self._url = req.POST['url']
        self._auc_name = self._get_auc_name(self._url)
        self._lot_number = self._get_lot_number()

    @staticmethod
    def _get_auc_name(url):
        name = url.split('.com')[0].split('.')[-1]
        return name.capitalize() if name == 'copart' else name.upper()

    def _get_lot_number(self):
        if self._auc_name == 'Copart':
            return self._url.split('/')[4]
        elif self._auc_name == 'IAAI':
            return self._url.split('/')[-1].split('~')[0]

    def get_data(self):
        dct = {}
        if self._auc_name == 'Copart':
            res = requests.get(url=self.RESPONSE_COPART + self._lot_number, headers=self.HEADERS)
            data = res.json()['data']['lotDetails']
            dct = {
                'year': data['lcy'],
                'engine_type': data['ft'],
                'engine_cc': data['egn'].split('L')[0],
                'auction_name': self._auc_name,
                'city': data['syn'].split('-')[-1].strip() + '-' + data['syn'].split()[0].strip()
            }

        elif self._auc_name == 'IAAI':
            res = requests.get(url=self._url, headers=self.HEADERS)
            tree = lxml.html.fromstring(res.text)

            city = \
            tree.xpath('/html/body/section/main/section[3]/div[1]/div[2]/div/div[1]/div[1]/div[2]/ul/li[2]/span[2]')[0].text_content()
            engine_cc = tree.xpath('//*[@id="engine_novideo"]')[0].text_content().split('L')[0]
            year = tree.xpath('/html/body/section/main/section[2]/div[2]/div/h1')[0].text_content().split()[0]
            engine_type = tree.xpath('//*[@id="waypoint-trigger"]/div[2]/ul/li[7]/span[2]')[0].text_content().strip()
            city = city.split('(')[0].replace('-', ' ').strip(' 1234').upper() + '-' + city.split('(')[1].strip(')')
            city = city.replace('  ', '')
            dct = {
                'year': year,
                'engine_type': self.ENGINE_TYPES[engine_type],
                'engine_cc': engine_cc.strip('-'),
                'auction_name': self._auc_name,
                'city': city
            }
        self._req.POST.update(dct)
        return self._req
