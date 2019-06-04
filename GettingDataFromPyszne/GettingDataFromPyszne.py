from bs4 import BeautifulSoup
import requests
import re
import json

with requests.Session() as c:

      nasdaq_baseurl = 'https://www.pyszne.pl/'
      nasdaq_url_restaurantname="pasibus-wroclaw-arkady-wroclawskie" #tyle wystarczy zmienić
      nasdaq_url = nasdaq_baseurl.__add__(nasdaq_url_restaurantname)


      url_fetch = c.get(nasdaq_url)
      soup = BeautifulSoup(url_fetch.text, 'html.parser')
      pattern= re.compile(r"MenucardProducts")
      matches=pattern.finditer(soup.text)
      for match in matches:
        print(match)
      textVariable=soup.text
      textVariable=textVariable[match.span()[0]:]
      pattern= re.compile(r";")
      matches=pattern.finditer(textVariable)
      listMatches=[]
      for match in matches:
        listMatches.append(match.span()[0])
      textVariable=textVariable[:listMatches[0]]
      pattern= re.compile(r"\[")
      matches1=pattern.finditer(textVariable)
      listMatches1=[]
      for match1 in matches1:
        listMatches1.append(match1.span()[0])
      textVariable=textVariable[listMatches1[0]:]
      textVariable='{"MenucardProducts":\n'+textVariable+'\n }'
      d = json.loads(textVariable)
      with open(nasdaq_url_restaurantname+".json", 'w') as json_file:  
        json.dump(d, json_file)
        json_file.close()
      productlist=""
      pricelist=""
      for product in d['MenucardProducts']:
        productlist=productlist+str(product['name'])+"\n"
        pricelist=pricelist+str(product['price'])+"\n"
      f=open(nasdaq_url_restaurantname+"_products.txt", 'w')
      f.write(productlist)
      f.close()
      g=open(nasdaq_url_restaurantname+"_prices.txt", 'w')
      g.write(pricelist)
      g.close()
      c.close()
#end
