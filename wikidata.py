"""
WIKIDATA_REQUEST1 et WIKIDATA_REQUEST2 sont les deux fragrments de la request
pour intéroger la base de données wikidata lors de la demande pour le
codepostal.
"""
WIKIDATA_REQUEST1 = """SELECT ?commune ?communeLabel ?image ?codepostal """ + \
       """ ?population ?superficie ?altitude ?site WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:""" + \
          """language "[AUTO_LANGUAGE],fr". }
  ?commune wdt:P31 wd:Q484170.
  OPTIONAL { ?commune wdt:P18 ?image. }
  OPTIONAL { ?commune wdt:P281 ?codepostal. } 
  filter(?codepostal = """

WIKIDATA_REQUEST2 = """).
  OPTIONAL { ?commune wdt:P1082 ?population. } 
  OPTIONAL { ?commune wdt:P2046 ?superficie. }
  OPTIONAL { ?commune wdt:P2044 ?altitude. }
  OPTIONAL { ?commune wdt:P856 ?site. }   
}
LIMIT 100 """
