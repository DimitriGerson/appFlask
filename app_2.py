from flask import Flask, request, render_template, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON
from wikidata import WIKIDATA_REQUEST1, WIKIDATA_REQUEST2
from urllib.error import HTTPError
import os

WEBDIR = os.path.dirname(os.path.abspath('__files__'))
PAGESDIR = os.path.join(os.path.dirname(WEBDIR), 'essais/templates')
STATICDIR = os.path.join(os.path.dirname(WEBDIR), 'essais/static/')
app = Flask(__name__, template_folder=PAGESDIR, static_folder=STATICDIR)

endpoint_url = "https://query.wikidata.org/sparql"
def get_results(endpoint_url, query):
    #creation d'un objet SPARQLWrapper
    sparql = SPARQLWrapper(endpoint_url)
    #envoie de la requête
    sparql.setQuery(query)
    #soecification que le retour de la requête sera du JSON à déserialiser
    sparql.setReturnFormat(JSON)
    #essais de recupération de la requête
    try:

        result = sparql.query().convert()
        print (result)
        #la requete c'est bien passée la fonction get_result retourne un tableau de données
        return result
    except HTTPError as err:
        #la requete à rencontrée un problème j'affiche l'erreur dans la console
        print(err.code)

@app.route('/')
def index():
    return render_template('index2.html')

#quand le bouton du formulaire sur le fichier html va être cliqué
#l'utilisateur va accéder à la page search grâce à action="search"
# du formulaire et le controller va déclencher la fonction search()
#qui va permettre à la page search de se construir
@app.route('/search', methods=['post'])
def search():
    #Si la methode est bien 'POST'
    if request.method == 'POST' :
        #Aller chercher dans le fomulaire les données de la balise qui à l'id 'search'
        search = request.form['search']
        #passer search en miniscule
        search = search.lower()
        print(search)
        #Dans le cas où le code postal ne comporte que 4 chiffre rajouter un 0 devant
        if len(search) == 4:
            search= "0" + search
        #création de la requete par concaténation des deux morceaux de requete
        #et de l'insertion de l'entrée utilisateur search
        wikidata_request_send = WIKIDATA_REQUEST1 + "\"" + search + "\"" + WIKIDATA_REQUEST2
        print(wikidata_request_send)
        #utilisation de la fonction get_result avec comme paramètres
        #l'adresse du site wikidata la constante endpoint_url
        #et la requete wikidata_request_send
        #le resultat de la requete est stocké dans la variable results
        results = get_results(endpoint_url, wikidata_request_send)
        #creation d'une liste vide qui va contenir les données
        listResults = []
        try:
            #creation d'une table à plat qui permet d'accéder aux données facilement
            results = results["results"]["bindings"]
            for result in results:
                listResults.append(result)
        except:
            print("Erreur déclenchée")
        return render_template('index2.html', items = results)

if __name__ == '__main__':
    app.run()
    #app.run()
