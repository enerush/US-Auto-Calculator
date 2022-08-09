from datetime import date

from calculator.forms import ResultForm
from calculator.models import City

PORT_UNLOAD_COST = 400.00
BROKER_COST = 400.00


def get_result_form(request):
    res = get_total_cost(request)
    return ResultForm(res)


def get_total_cost(req):
    """returns the full price of the car, which includes customs fees, delivery, registration"""
    price = float(req.POST['price'])
    bank_fee = calc_bank_fee(price)
    auction_fee = get_auc_fee(price)
    ship_cost = calc_ship_cost(req.POST['auction_name'], req.POST['city'])
    import_fee = calc_import_fee(req)
    port_unload = PORT_UNLOAD_COST
    broker = BROKER_COST
    company_fee = float(req.POST['company_fee'])

    total = round(price + auction_fee + bank_fee + ship_cost + import_fee + port_unload + broker + company_fee, 2)

    return {
            'price': price, 'auction_fee': round(auction_fee, 2),
            'bank_fee': bank_fee, 'ship_cost': ship_cost,
            'port_unload': port_unload, 'broker': broker,
            'import_fee': import_fee, 'company_fee': company_fee,
            'total': total
            }


def get_auc_fee(price):
    if price < 1000:
        buyer_fee = 275
        bid_fee = 39
    elif 1000 <= price < 1800:
        buyer_fee = 69
        bid_fee = 59
    elif 1800 <= price < 3000:
        buyer_fee = 480
        bid_fee = 79
    elif 3000 <= price < 5000:
        buyer_fee = 650
        bid_fee = 89
    elif 5000 <= price < 10000:
        buyer_fee = 750
        bid_fee = 99
    elif 10000 <= price < 15000:
        buyer_fee = 800
        bid_fee = 119
    else:
        buyer_fee = price * 0.07
        bid_fee = 119

    gate_fee = 79

    return buyer_fee + gate_fee + bid_fee


def calc_bank_fee(price):
    res = price * 0.005
    return 500 + 12 if res > 500 else res + 12


def calc_ship_cost(auction, city):
    c = City.objects.filter(auction=auction, city=city)
    return float(c[0].price)


def calc_import_fee(req):
    price = int(req.POST['price'])
    engine_type = req.POST['engine_type']
    engine_cc = float(req.POST['engine_cc'])
    kwh = req.POST['kwh']
    year = int(req.POST['year'])

    if engine_type == 'ELECTRIC' and kwh:
        return round(int(kwh) * 1.02, 2)
    elif engine_type == 'ELECTRIC' and not kwh:
        return 0

    year_kof = calc_year_kof(year)
    engine_kof = get_engine_kof(engine_type, engine_cc)

    import_tax = price * 0.1
    excise_tax = engine_kof * engine_cc * year_kof
    print(engine_kof, engine_cc, year_kof)
    vat = (import_tax + excise_tax + price) * 0.2
    print(import_tax*36.56, excise_tax*36.56, vat*36.56, sep='\n')
    return round(import_tax + excise_tax + vat, 2)


def calc_year_kof(year):
    kof = date.today().year - year - 1
    return 15 if kof > 15 else 1 if kof < 1 else kof


def get_engine_kof(engine_type, engine_cc):

    if engine_type == 'DIESEL':
        if engine_cc > 3.5:
            return 154.10
        else:
            return 77.05

    if engine_type in ('GAS', 'HYBRID'):
        if engine_cc > 3.0:
            return 102.73
        else:
            return 51.37


