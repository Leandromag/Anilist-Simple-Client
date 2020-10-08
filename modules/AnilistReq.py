
import requests
import json
import time
from datetime import datetime, timedelta


query = '''
query ($userid: Int) {
  Page(page: 1) {
    mediaList(userId: $userid, status: CURRENT, type: ANIME) {
      progress
      media {
        id
        title {
          romaji
        }
        season
        seasonYear
        status
        episodes

        coverImage {
          medium
        }

        airingSchedule(notYetAired:true, perPage:1){
          nodes{

            episode
            airingAt
            timeUntilAiring
          }
        }
      }
    }
  }

}
'''


queryUser = '''
query ($nombre: String) {
  User(name:$nombre){
    id
  }

}
'''

queryUserData = '''
query ($userid: Int) {
    User(id:$userid){
    	name
    	statistics{
        anime{
          count
          episodesWatched

        }
      }
    	avatar {
    	  large
    	  medium
    	}
    }

}

'''


class AnilistaRequest():
    def __init__(self):
        self.listaSiguiendoElem=[]
        self.datosUsr={}
        self.usrid=0
        #self.actualizarLista()
        #self.datosDeUsuario()

    def actualizar(self):
        with open('modules/data/user_data') as json_file:
            data = json.load(json_file)
            self.usrid=data['userId']
        self.actualizarLista()
        self.datosDeUsuario()

    def datosDeUsuario(self):
        variables = {'userid':self.usrid}
        url = 'https://graphql.anilist.co'     # Make the HTTP Api request
        response = requests.post(url, json={'query': queryUserData, 'variables': variables})
        response_json = json.loads(response.text)
        self.datosUsr['profileimg']=response_json['data']['User']['avatar']['medium']
        self.datosUsr['profilename']=response_json['data']['User']['name']

    def convertirtiempo(self,seconds):
        time = float(seconds)
        day = time // (24 * 3600)
        time = time % (24 * 3600)
        hour = time // 3600
        time %= 3600
        minutes = time // 60
        time %= 60
        seconds = time
        d="dias"
        h="horas"
        m="minutos"
        s="segundos"

        if(day == 1):
            d="dia"
        if(hour == 1):
            h="hora"
        if(minutes== 1):
            m="minuto"
        if(seconds == 1):
            s="segundo"

        striformat="%d "+d+", %d "+h+", %d "+m+", %d "+s+" "
        return(striformat % (day, hour, minutes, seconds))


    def obtenerId(self, id):
        variables={'nombre': id }
        url = 'https://graphql.anilist.co'     # Make the HTTP Api request
        response = requests.post(url, json={'query': queryUser, 'variables': variables})
        response_json = json.loads(response.text)
        if(response_json['data']['User'] == None):
            id="none"
        else:
            id=response_json['data']['User']['id']
        return(id)
    def obtenerAvatar(self):
        url = self.datosUsr['profileimg']
        response = requests.get(url)
        if response.status_code == 200:
            return(response.content)
        else:
            return("none")
    def obtenerLista(self):
        return self.listaSiguiendoElem
    def obtenerDatosdeUsuario(self):
        return self.datosUsr
    def actualizarLista(self):
        self.listaSiguiendoElem.clear()
        # Define our query variables and values that will be used in the query request
        variables = {'userid':self.usrid}
        print()
        url = 'https://graphql.anilist.co'     # Make the HTTP Api request
        response = requests.post(url, json={'query': query, 'variables': variables})
        response_json = json.loads(response.text)
        #print(json.dumps(response_json, indent=4, sort_keys=True))
        ind=0

        for media in response_json['data']['Page']['mediaList']:

            title=response_json['data']['Page']['mediaList'][ind]['media']['title']['romaji']
            temporada=response_json['data']['Page']['mediaList'][ind]['media']['season']
            anio=response_json['data']['Page']['mediaList'][ind]['media']['seasonYear']
            estado=response_json['data']['Page']['mediaList'][ind]['media']['status']
            episodios=response_json['data']['Page']['mediaList'][ind]['media']['episodes']
            #print(response_json['data']['Page']['mediaList'][ind]['media']['coverImage']['medium'])
            diayhora="NULL"
            capitulo="NULL"
            tiempohastasalida="NULL"
            progreso= response_json['data']['Page']['mediaList'][ind]['progress']

            if( len(response_json['data']['Page']['mediaList'][ind]['media']['airingSchedule']['nodes']) == 1):
                tiempoepoch = response_json['data']['Page']['mediaList'][ind]['media']['airingSchedule']['nodes'][0]['airingAt']
                diayhora=time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(tiempoepoch))
                capitulo= response_json['data']['Page']['mediaList'][ind]['media']['airingSchedule']['nodes'][0]['episode']
                tiempohastasalida= response_json['data']['Page']['mediaList'][ind]['media']['airingSchedule']['nodes'][0]['timeUntilAiring']
                tiempohastasalida= self.convertirtiempo(int(tiempohastasalida))
            ind+=1
            sublista={}
            sublista['titulo']=title
            sublista['temporada']=temporada
            sublista['anio']=anio
            if(estado == 'RELEASING'):
                sublista['estado']="SALIENDO"
            if(estado == 'FINISHED'):
                sublista['estado']="TERMINADA"
            sublista['diahora']=diayhora
            sublista['capitulo']=capitulo
            sublista['tiemposalida']=tiempohastasalida
            if(episodios == None):
                sublista['totepisodios']="?"
            else:
                sublista['totepisodios']=episodios
            sublista['progreso']=progreso
            self.listaSiguiendoElem.append(sublista)
