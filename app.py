from flask import Flask, request, render_template, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON
from wikidata import WIKIDATA_REQUEST1, WIKIDATA_REQUEST2
from urllib.error import HTTPError
from datetime import date

app = Flask(__name__)

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
@app.route('/search')
def index():
    return render_template('index4.html')

@app.route('/discussion')
@app.route('/discussion/page/<int:num_page>')
def mon_chat(num_page=1):
    premier_msg = 1 + 50 * (num_page -1)
    dernier_msg = premier_msg + 50
    return 'affichages des messages {} à {}'.format(premier_msg, dernier_msg)

@app.errorhandler(404)
def page_404(error):
    return "Voici ma Jolie page 404", 404

@app.route('/date')
def date():
    d = date.today().isoformat()
    return render_template('accueil.html', la_date=d)

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
        la_recherche = search
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
        return render_template('index4.html', items = results, codepostal = la_recherche )

if __name__ == '__main__':
    app.run()
    #app.run()
