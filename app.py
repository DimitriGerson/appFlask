#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Voici mon application Flask pour la recherche de commune en fonction
    de leur code postal.
    Une deuxième recherche sera créer pour chercher le code postal en
    fonction d'un nom de commune.
    le module wikidata.py doit être ajouté car il contient la requête.
    C'est un module que j'ai créé.
"""

from datetime import date
from urllib.error import HTTPError
from flask import Flask, request, render_template #, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON
from wikidata import WIKIDATA_REQUEST1, WIKIDATA_REQUEST2

app = Flask(__name__)

ENDPOINT_URL = "https://query.wikidata.org/sparql"
def get_results(query):
    """
        get_results est une fonction qui va intéroger la base de données
        wikidata.
        Le langage de requete est le sparql et elle renvoie un objet au
        format JSON.
    """
    #creation d'un objet SPARQLWrapper
    sparql = SPARQLWrapper(ENDPOINT_URL)
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
        return None

@app.route('/')
@app.route('/search')
def index():
    """
        this function is for the index page.
    """
    return render_template('index4.html')

@app.route('/discussion')
@app.route('/discussion/page/<int:num_page>')
def mon_chat(num_page=1):
    """
        this function is for an example for numerotation
    """
    premier_msg = 1 + 50 * (num_page -1)
    dernier_msg = premier_msg + 50
    return 'affichages des messages {} à {}'.format(premier_msg, dernier_msg)

@app.errorhandler(404)
def page_404(adresse):
    """
        This function is for create my personnal error 404 page
        pylint n'aime pas le error dans page_404(error)je le remplace
        par page_404(): vu que je ne me sert pas de error
    """
    return "Voici ma Jolie page 404", 404
    #return "Voici ma Jolie page 404"
@app.route('/date')
def date_du_jour():
    """
        This function tells the date of the day.
    """
    today = date.today().isoformat()
    return render_template('accueil.html', la_date=today)

#quand le bouton du formulaire sur le fichier html va être cliqué
#l'utilisateur va accéder à la page search grâce à action="search"
# du formulaire et le controller va déclencher la fonction search()
#qui va permettre à la page search de se construir
@app.route('/search', methods=['post'])
def search():
    """
        This function made the answer of client request
    """
    #Si la methode est bien 'POST'
    if request.method == 'POST' :
        #Aller chercher dans le fomulaire les données de la balise qui à l'id 'search'
        the_search = request.form['search']
        la_recherche = the_search
        #passer search en miniscule
        the_search = the_search.lower()
        print(the_search)
        #Dans le cas où le code postal ne comporte que 4 chiffre rajouter un 0 devant
        if len(the_search) == 4:
            the_search= "0" + the_search
        #création de la requete par concaténation des deux morceaux de requete
        #et de l'insertion de l'entrée utilisateur search
        wikidata_request_send = WIKIDATA_REQUEST1 + "\"" + the_search + "\"" + WIKIDATA_REQUEST2
        print(wikidata_request_send)
        #utilisation de la fonction get_result avec comme paramètres
        #l'adresse du site wikidata la constante endpoint_url
        #et la requete wikidata_request_send
        #le resultat de la requete est stocké dans la variable results
        results = get_results(wikidata_request_send)
        #creation d'une liste vide qui va contenir les données
        list_results = []
        #J'ai l'impression que je ne me sert pas de list_results
        try:
            #creation d'une table à plat qui permet d'accéder aux données facilement
            results = results["results"]["bindings"]
            for result in results:
                list_results.append(result)
        except (RuntimeError, TypeError, NameError):
            print("Erreur déclenchée")
            return None
        return render_template('index4.html', items = results, codepostal = la_recherche )

if __name__ == '__main__':
    app.run()
    #app.run()
