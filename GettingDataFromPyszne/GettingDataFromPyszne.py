from bs4 import BeautifulSoup
import requests
import re
import json
import subprocess
import os

with requests.Session() as c:

      pyszne_baseurl = 'https://www.pyszne.pl/'
      pyszne_url_restaurantname="amir-kebab-katowice" #tyle wystarczy zmienić
      pyszne_url = pyszne_baseurl.__add__(pyszne_url_restaurantname)
      path_base = os.getcwd()


      url_fetch = c.get(pyszne_url)
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
# outside the context manager we are back wherever we started.
      path = path_base+"/Restaurants/"+pyszne_url_restaurantname
  
      try:  
          os.mkdir(path)
      except OSError:  
          print ("Creation of the directory %s failed" % path)
      else:  
          print ("Successfully created the directory %s " % path)
      os.chdir(path)
      with open(pyszne_url_restaurantname+".json", 'w') as json_file:  
        json.dump(d, json_file)
        json_file.close()
      productlist=""
      pricelist=""
      for product in d['MenucardProducts']:
        productlist=productlist+str(product['name'])+"\n"
        pricelist=pricelist+str(product['price'])+"\n"
      f=open(pyszne_url_restaurantname+"_products.txt", 'w')
      f.write(productlist)
      f.close()
      g=open(pyszne_url_restaurantname+"_prices.txt", 'w')
      g.write(pricelist)
      g.close()
      os.chdir(path_base)
      c.close()
#end
