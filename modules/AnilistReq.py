
import requests
import json
import time
from datetime import datetime, timedelta


query = '''
{
  Page(page: 1) {
    mediaList(userId: 705297, status: CURRENT, type: ANIME) {
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


class AnilistaRequest():

	def __init__(self):
		self.listaSiguiendo=[]
		self.actualizarLista()

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




	def darformato(self,title,temporada,anio,estado,diayhora,capitulo,tiempohastasalida,episodios,progreso):
		if(estado == "FINISHED"):   #MEJORAR ALGUN DIA
			estado="FINALIZADO"
		else:
			estado="SALIENDO"

		linea1= title+"\n" + temporada + "/" + str(anio) + "   Estado:" + estado +"   progreso:["+str(progreso)+"/"+str(episodios)+"] "

		linea2=""
		if(estado != "FINALIZADO"):
			linea2= "\n\nEpisodio "+str(capitulo)+" sale en:\n"+tiempohastasalida+" "
			total=linea1+linea2
			self.listaSiguiendo.insert(0,total)
		else:
			total=linea1
			self.listaSiguiendo.append(total)


	def obtenerLista(self):
		return self.listaSiguiendo

	def actualizarLista(self):
		self.listaSiguiendo.clear()
		# Define our query variables and values that will be used in the query request
		variables = {}
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
			
			self.darformato(title,temporada,anio,estado,diayhora,capitulo,tiempohastasalida,episodios,progreso)





