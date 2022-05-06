import requests
from bs4 import BeautifulSoup as BS
import json

txt = {}
cd = {}
ci = 0

for idx in range(15):
    url = f"https://gottwein.de/Lat/ov/met{idx+1:02d}la.php"
    
    content = requests.get(url).text
    soup = BS(content, "html.parser")
    
    #table style="width:100%;"
    tables = soup.find_all('table', attrs={'style':'width:100%;'})
    
    table = tables[0]
    
    rows = table.find_all('tr')
    
    for row in rows:
        if len(row.find_all('td')) < 2:
            continue
        td = row.find_all('td')[1]
        if td['style'] == "vertical-align:top; font-size:1.5em; background-color:#FFFF99;":
            cd[ci] = ' '.join(i.strip() for i in td.get_text().split('\n'))
            ci += 1
        elif td['style'] == "vertical-align:top; background-color:#CCFFCC;":
            pass
        else:
            if ci not in txt:
                txt[ci] = []
            txt[ci] += [i.strip() for i in ''.join([i for i in td.get_text().lower() if i.isalpha() or i==' ']).split(" ")]
res = {'text':txt, 'index':cd}
with open("data.json","w") as f:
    json.dump(res, f)
