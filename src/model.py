import simpy
import random, time

random.seed(time.time())

class Assinante:

  def __init__(self, env, nome, tipo, horario_chegada, tempo_pedalada):
    self.env = env
    self.nome = nome
    self.horario_chegada = horario_chegada
    self.tipo = tipo #Influencia no tempo de pedalada
    self.tempo_pedalada = tempo_pedalada


class Estacao:

    def __init__(self, env, station_id, bicicletas, bicicletarios, rain_event, rain_boolean, rain_time):
       
      
      self.env = env
      self.station_id = station_id
      self.bicicletas = bicicletas
      self.bicicletarios = bicicletarios
      
      self.chuva_event = self.env.event()
      if rain_boolean:
        self.env.process(self.rain())
        self.rain_event = rain_event
        self.rain_boolean = rain_boolean
        self.rain_time = rain_time
        self.message_aux = True
      else:
          self.chuva_event.succeed()
    
    
    def parte_estacao(self, assinante):
        
        yield self.env.timeout(assinante.horario_chegada)
        print(assinante.nome, "Chegou na estação ",self.station_id," em", self.env.now)
        
        # chuva
        yield self.chuva_event

        with self.bicicletas.request() as bicicleta:
          available_resources = self.bicicletas.capacity - self.bicicletas.count
          yield bicicleta
          print(assinante.nome, "partiu com a bicicleta em ", 
                self.env.now," que durou ", assinante.tempo_pedalada, 
                "|", available_resources, 'bicicletas disponíveis')
          
          yield self.env.timeout(assinante.tempo_pedalada)
          self.env.process(self.chega_estacao(assinante))
        
            
    def rain(self):
        if self.message_aux:
            print('Às', self.env.now, 'começa a chover')
            self.message_aux = False
            
        with self.rain_event.request() as rain:
            print("espera a chuva passar a partir das", self.env.now)
            
            yield rain
            yield self.env.timeout(self.rain_time)
            self.chuva_event.succeed()
            
            self.message_aux = True
            if self.message_aux:
                print("A chuva para depois de", self.rain_time,)
                self.message_aux = False
                   
                   
    def chega_estacao(self, assinante):
        
        with self.bicicletarios.request() as bicicletario:
          available_resources = self.bicicletarios.capacity - self.bicicletarios.count
          yield bicicletario
          print(assinante.nome, "colocou a bicicleta no bicicletario em ", self.env.now, "|", available_resources, 'bicicletarios disponíveis')
          #yield self.env.timeout(100000)
        
    


class World:
    
    def __init__(self, env, info_estacao, info_mes, info_dia_semana, info_horario, risk_of_rain, rain_time, func_tempo_pedalada):
        
        self.env = env
        
        self.id_estacao = info_estacao['id']
        self.bicicletas = info_estacao['bicicletas'] #Indica a quantidade de bicicletas naquela estação
        print(self.bicicletas)
        self.tempo_espera = info_estacao['tempo_espera']
        
        self.mes = info_mes['nome_mes']
        self.assinantes_maximo = info_mes['qt_maxima']
        
        self.dia = info_dia_semana['nome_dia']
        self.assinantes_dia = info_dia_semana['porc_assinantes'] #Indica a porcentagem de assinantes para aquele dia
        
        self.horario = info_horario['nome_horario']
        self.assinantes_horario = info_horario['porc_assinantes']#Indica a porcentagem de assinantes para aquele horário
        
        self.rain = False
        
        if (risk_of_rain + (random.randint(0,5))/10 ) > 0.5:
            self.rain = True

        self.assinantes = []
        
        for h in self.horario:
            for i in range(int(self.assinantes_maximo*self.assinantes_dia*self.assinantes_horario[self.horario.index(h)])):
                self.assinantes.append(Assinante(self.env,
                                                'Assinante '+ str((i+1)*(self.horario.index(h)+1)),
                                                self.get_random_usertype(),
                                                h + random.randint(0,59)/100,
                                                func_tempo_pedalada(self.get_random_usertype())))
            
        
        self.bicicletarios = simpy.Resource(self.env, capacity = self.bicicletas)
        self.bicicletas = simpy.Resource(self.env, capacity = self.bicicletas)
        self.rain_event = simpy.Resource(self.env, capacity = 1)
        
        self.estacao = Estacao(self.env, self.id_estacao, self.bicicletas, self.bicicletarios, self.rain_event, self.rain, rain_time)
        
        for i in range(len(self.assinantes)):
            self.env.process(self.estacao.parte_estacao(self.assinantes[i]))

    def get_random_usertype(self):
        
        tmp = random.randint(1,2)
            
        if tmp == 1:
            return 'Annual Member'
        
        else:
            return 'Short-Term Pass Holder'

    
    def run(self):
        for i in range(len(self.assinantes)):
            self.env.process(self.estacao.parte_estacao(self.assinantes[i]))
        
        self.env.run()

      