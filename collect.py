#!/usr/bin/env python3
"""Daily Raiffeisen NAV collector. Fails closed if any price/date is missing."""
import datetime as dt, json, pathlib, re, urllib.request, html
ROOT=pathlib.Path(__file__).parent
FUNDS={
 'DE0008477076':'fu_100011481',
 'DE0005314116':'fu_531411',
 'LU0101441672':'fu_921559',
}
BASE='https://www.raiffeisen.it/de/kastelruth-stulrich/rgo-mp/top-navi/finanzinformationen/investmentfonds/detail/fund/{}.html'
def parse(text,isin):
    clean=html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'<(script|style)\b[^>]*>.*?</\1>',' ',text,flags=re.I|re.S)))
    clean=re.sub(r'\s+',' ',clean)
    if isin not in clean:raise ValueError('ISIN not found: '+isin)
    dm=re.search(r'Kurszeit:\s*(\d{1,2}\.\d{1,2}\.\d{4})',clean,re.I)
    pm=re.search(r'Aktuell:\s*([\d.,]+)',clean,re.I)
    if not dm or not pm:raise ValueError('NAV or NAV date missing: '+isin)
    day=dt.datetime.strptime(dm.group(1),'%d.%m.%Y').date().isoformat()
    nav=float(pm.group(1).replace('.','').replace(',','.'))
    if not (0<nav<1000000):raise ValueError('Invalid NAV: '+isin)
    return {'nav':nav,'date':day,'source':BASE.format(FUNDS[isin])}
def collect():
    prices={}
    for isin,slug in FUNDS.items():
        req=urllib.request.Request(BASE.format(slug),headers={'User-Agent':'Mozilla/5.0 (compatible; PersonalInvestmentTracker/1.0)'})
        with urllib.request.urlopen(req,timeout=25) as r:page=r.read().decode('utf-8','replace')
        prices[isin]=parse(page,isin)
    path=ROOT/'data/history.json'
    records=json.loads(path.read_text(encoding='utf-8'))
    now=dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
    local_day=dt.datetime.now(dt.timezone(dt.timedelta(hours=1))).date().isoformat() # replaced below with Europe/Rome
    from zoneinfo import ZoneInfo
    local_day=dt.datetime.now(ZoneInfo('Europe/Rome')).date().isoformat()
    # Replace a previous run on the same day; keep one immutable record per calendar day.
    records=[r for r in records if r['recorded_at'][:10]!=local_day]
    records.append({'recorded_at':local_day+' (Europe/Rome)','collected_utc':now,'prices':prices})
    records.sort(key=lambda r:r['recorded_at'])
    path.write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('Collected:',local_day,[(k,v['nav'],v['date']) for k,v in prices.items()])
if __name__=='__main__':collect()
