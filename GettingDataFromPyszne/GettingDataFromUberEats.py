from bs4 import BeautifulSoup
import requests
import re
import json
import subprocess
import os

with requests.Session() as c:

      pyszne_baseurl = 'https://www.ubereats.com/'
      pyszne_url_restaurantname="pl-PL/warsaw/food-delivery/fenicja-swietokrzyska/VT6RTZF-TPupU_9ZgHWTuw/" #all you have to change
      pyszne_url = pyszne_baseurl.__add__(pyszne_url_restaurantname)
      path_base = os.getcwd()


      url_fetch = c.get(pyszne_url)
      soup = BeautifulSoup(url_fetch.text, 'html.parser')
      textVariable=soup.text
      #textVariable.replace(']}]}]}',']}]}')
      pattern= re.compile(r"displayItems")
      matches=pattern.finditer(textVariable)
      listMatches=[]
      for match in matches:
        listMatches.append(match.span()[0])
      productlist=[]
      pricelist=[]
      descriptionlist=[]
      for category in listMatches:
          #if any("Water" in s for s in productlist):
          #     break
          #if any("Woda" in s for s in productlist):
          #     break
          textData=textVariable[category-1:]
          pattern= re.compile(r"}]},")
          matches=pattern.finditer(textData)
          tempListMatch=[]
          for match in matches:
              tempListMatch.append(match.span()[0])
          textData=textData[:tempListMatch[0]+3]
          textData='{'+textData
          if(',"subsectionsMap"' in textData):
              textData=textData[:textData.index(',"subsectionsMap"')-1]
          #if('Coca-Cola' in textData or 'Pepsi' in textData or 'Woda' in textData or 'Water' in textData):
          #    textData=textData[:len(textData)-2]
          if('title' not in textData and 'price' not in textData):
              break
          while True:
              try:
                  d = json.loads(textData)
              except ValueError as e:
                  if("delimiter" in str(e)):
                      textData=textData+"]}"
                      continue
                  else:
                      textData=textData[:len(textData)-2]
                      continue
              break
          for product in d['displayItems']:
             if('title' not in product):
                 break
             productlist.append(product['title'])
             pricelist.append(product['price'])
             if('itemDescription' in product):
                descriptionlist.append(product['itemDescription'])
             else:
                descriptionlist.append("")
      print(len(productlist),len(descriptionlist),len(pricelist))