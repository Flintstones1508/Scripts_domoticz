#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import json
import requests

############# Parametres #################################

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# les parametres de l'API
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

www_api='http://domogeek.entropialux.com'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# les parametres de Domoticz
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

domoticz_ip='adresse_ip'
domoticz_port='port'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IDX du switch "Alerte"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

IDX_vigi='IDX'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# associer ici les couleurs des alertes meteofrance aux couleurs de Domoticz
# rappel des couleurs Domoticz  0=gris, 1=vert,2=jaune,3=orange,4=rouge
# meteofrance envoie RAS qui ici est asscocie a gris
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

dict_couleur_widget_texte={'RAS' : 0,
                           'vert' : 1,
                           'jaune': 2,
                           'orange' : 3,
                           'rouge' : 4
                          }
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# les parametres de meteofrance
# on passe le numero du departement en appelant le script
# sinon supprimer ces lignes et decommenter Departement=
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if len(sys.argv) ==1:
    print "Donner un departement"
    sys.exit(0)

else:
    Departement =sys.argv[1]

###############  fin des parametres #############################

r = requests.get(www_api+'/vigilance/'+Departement+'/all')
if r.status_code == 200:

# l'API renvoie 200 si tout est OK
    print 'Recup OK'
    # vigijson est un dict au sens python
    vigijson=r.json()
    
    # extraire les valeurs
    risk  = vigijson['vigilancerisk']
    couleur_vigilance = vigijson['vigilancecolor']
    
    # on recupere la couleur associe au risque que l'on vient de trouver dans le dict des couleurs
    couleur_gen=str(dict_couleur_widget_texte[couleur_vigilance])

    # composons l'url
    url_domoticz='http://'+domoticz_ip+':'+domoticz_port+'/json.htm?type=command&param=udevice&idx='+IDX_vigi+'&nvalue='+couleur_gen+'&svalue='+risk
    
    r=requests.get(url_domoticz)
    if  r.status_code != 200:
        print "Erreur API"
  
else:
    print "Erreur API"




