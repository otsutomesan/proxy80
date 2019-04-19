

# import math

import requests
import re

def get_url():
  return ''.join([
    'http'+ ':' + '//',
    '.'.join(['www', 'cyber'+'syndrome', 'net']),
    '/'+'search.cgi'+'?' + '&'.join(['q=JP', 'a=A', 'f=d', 's=new', 'n=100'])
  ])

def read_page():
  url = get_url()
  ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
  headers = {
    'User-Agent': ua,
  }
  session = requests.Session()
  session.headers.update(headers)
  res = session.get(url)
  return res.text

def parse_as(html):
  re_str = r'as=\[([\d,]+)\];'
  r = re.search(re_str, html)
  res = ''
  if r:
    res = r.group(1).split(',')
  # print('as:', res)
  return res

def parse_ps(html):
  re_str = r'var ps=\[([\d,]+)\];'
  r = re.search(re_str, html)
  res = ''
  if r:
    res = r.group(1).split(',')
  # print('ps:', res)
  return res

def parse_n(html, ps):
  re_str = r'var n=(\(.+?\)\%\d+);'
  r = re.search(re_str, html)
  res = ''
  if r:
    _n = r.group(1)
    # print('_n:', _n)
    for r2 in re.findall(r'ps\[(\d+)\]', _n):
      # print('n:r2:', r2)
      _n = _n.replace('ps[%s]'%r2, ps[int(r2)])
    # print('_n:', _n)
    res = eval(_n)
  # print('n:', res)
  return res

def decode_ip_addrs(var_as, var_ps, var_n):
  as1 = var_as[0:var_n]
  as2 = var_as[var_n:]

  # tmp = {} 
  # for i, a in enumerate(as2+as1):
  #   idx = math.floor(i/4)
  #   # print('idx:', idx)

  #   if not idx in tmp:
  #     # tmp[idx] = [None, None, None, None]
  #     tmp[idx] = []

  #   # if i%4 == 0:
  #   #   tmp[idx].append(a)
  #   # elif i%4 == 3:
  #   #   tmp[idx].append(a)
  #   # else:
  #   #   tmp[idx].append(a)
  #   tmp[idx].append(a)
  # for i in sorted(tmp.keys()):
  # for i in tmp.keys():
  #   # print('n%s:'%(i+1), '%s:%s'%(''.join(tmp[i]), ps[i]))
  #   addrs = '%s:%s'%('.'.join(tmp[i]), var_ps[i])
  #   res.append(addrs)
  #   # print('n%s:'%(i+1),  addrs)
  res = []
  tmp = [] 
  for i, a in enumerate(as2+as1):
    tmp.append(a)
    if len(tmp) == 4:
      ps_idx = len(res)
      adrs = '.'.join(tmp) + ':' + var_ps[ps_idx]
      res.append(adrs)
      tmp = []

  return res
  
def get_proxies():
  html = read_page()
  # print(html)

  var_as = parse_as(html)
  var_ps = parse_ps(html)
  var_n = parse_n(html, var_ps)
  ips = decode_ip_addrs(var_as, var_ps, var_n)
  return ips

if __name__ == '__main__':
  proxies = get_proxies()
  print(proxies)

