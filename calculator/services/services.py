from datetime import date


def get_total_cost(request):
    """returns the full price of the car, which includes customs fees, delivery, registration"""
    url = request.GET['url']
    price = int(request.GET['price'])
    year = int(request.GET['year'])
    engine_type = request.GET['engine_type']
    engine_cc = float(request.GET['engine_cc'])
    auction_name = request.GET['auction_name']
    city = request.GET['city']

    res = get_tax_cost(price, engine_type, engine_cc, year)

    return {'USD': round(res, 2), 'UAH': round(res * 36.56, 2)}


def get_tax_cost(price, engine_type, engine_cc, year):

    year_kof = date.today().year - year - 1
    engine_kof = get_engine_kof(engine_type, engine_cc)

    import_tax = price * 0.1
    excise_tax = engine_kof * engine_cc * year_kof
    vat = (import_tax + excise_tax + price) * 0.2

    return import_tax + excise_tax + vat


def get_engine_kof(engine_type, engine_cc):

    if engine_type == 'DIESEL':
        if engine_cc > 3.5:
            return 154.10
        else:
            return 77.05

    if engine_type == 'GAS':
        if engine_cc > 3.0:
            return 102.73
        else:
            return 51.37


def get_ship_cost():
    pass


