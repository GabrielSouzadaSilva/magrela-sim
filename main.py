from src.dataParser import DataParser, DataLoader
from src.model import World
import random
import simpy

if __name__== "__main__":
    
    env = simpy.Environment()
    
    data_loader_init = DataLoader()
    exp = data_loader_init.get_explorer()

    data_parser_init = DataParser(exp)
       
    all_stations_id = data_parser_init.get_all_stations_id()

    user_time = data_parser_init.get_user_time('Annual Member')


    station_id = ['BT-05','UW-06']
    month = 2 #O mês começa em 1
    weekDay = 3 #A semana começa no domingo e em 0
    horario = [i for i in range(5)]
    rain_time = random.randint(0, 120)/60 #Minutos
        
    for stations in station_id:
        month_rain_risk = data_parser_init.get_risk_of_rain(month)
        
        info_estacao = {'id':data_parser_init.get_station_id(stations), 
                        'bicicletas':data_parser_init.get_bikes_qt(stations), 
                        'tempo_espera':data_parser_init.get_wait_time(stations)}
            
        info_mes = {'nome_mes':data_parser_init.get_month_name(month), 'qt_maxima':data_parser_init.get_month_users(stations, month)} 
        
        info_dia_semana = {'nome_dia':data_parser_init.get_dayWeek(weekDay), 'porc_assinantes':data_parser_init.get_perc_dayWeek(stations, weekDay)}
        
        info_horario = {'nome_horario':horario, 'porc_assinantes':data_parser_init.get_perc_hour(stations, horario)}
        
        world1 = World(env, 
                    info_estacao, 
                    info_mes, 
                    info_dia_semana, 
                    info_horario, 
                    month_rain_risk, 
                    rain_time, 
                    data_parser_init.get_user_time)

    
    env.run()
