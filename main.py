from src.dataParser import DataParser, DataLoader
from src.model import World
import random

if __name__== "__main__":
    
    
    data_loader_init = DataLoader()
    exp = data_loader_init.get_explorer()

    data_parser_init = DataParser(exp)
       
    all_stations_id = data_parser_init.get_all_stations_id()

    user_time = data_parser_init.get_user_time('Annual Member')


    station_id = 'BT-05'
    month = 2 #O mês começa em 1
    weekDay = 3 #A semana começa no domingo e em 0
    horario = [7]
    # horario = 28800
    rain_time = random.randint(0, 120) #Minutos
        
    
    month_rain_risk = data_parser_init.get_risk_of_rain(month)
       
    info_estacao = {'id':data_parser_init.get_station_id(station_id), 'bicicletas':data_parser_init.get_bikes_qt(station_id),
                    'tempo_espera':data_parser_init.get_wait_time(station_id)}
        
    info_mes = {'nome_mes':data_parser_init.get_month_name(month), 'qt_maxima':data_parser_init.get_month_users(station_id, month)} 
    
    info_dia_semana = {'nome_dia':data_parser_init.get_dayWeek(weekDay), 'porc_assinantes':data_parser_init.get_perc_dayWeek(station_id, weekDay)}
    
    info_horario = {'nome_horario':horario, 'porc_assinantes':data_parser_init.get_perc_hour(station_id, horario)}
    
    world1 = World(info_estacao, info_mes, info_dia_semana, info_horario, month_rain_risk, rain_time, data_parser_init.get_user_time)

    world1.run()
    
    # horario = 10
   
    # month_rain_risk = data_parser_init.get_risk_of_rain(month)
       
    # info_estacao = {'id':data_parser_init.get_station_id(station_id), 'bicicletas':data_parser_init.get_bikes_qt(station_id),
    #                 'tempo_espera':data_parser_init.get_wait_time(station_id)}
        
    # info_mes = {'nome_mes':data_parser_init.get_month_name(month), 'qt_maxima':data_parser_init.get_month_users(station_id, month)} 
    
    # info_dia_semana = {'nome_dia':data_parser_init.get_dayWeek(weekDay), 'porc_assinantes':data_parser_init.get_perc_dayWeek(station_id, weekDay)}
    
    # info_horario = {'nome_horario':horario, 'porc_assinantes':data_parser_init.get_perc_hour(station_id, 8)}
    
    # world2 = World(info_estacao, info_mes, info_dia_semana, info_horario, month_rain_risk, rain_time, data_parser_init.get_user_time)
    
     
    # world2.run()