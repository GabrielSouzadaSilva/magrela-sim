import pandas as pd
import numpy as np
import gc, random
from src.eda import Explorer, OutlierDetector


class DataLoader:
    def __init__(self):
        
        print('Lendo dado serializado...')
        
        self.explorer = Explorer(serial_path="./data/exploration1.pickle") #Lê o dataframe atual
        


    def get_explorer(self):
        
        return self.explorer
        
        


class DataParser:
    
    def __init__(self, explorer):
        

        '''
        
            A partir daqui cria todas variáveis necessárias para a leitura dos
            dados
        
        '''
        
        print('Criando variáveis necessárias...')
        
        
        trip_df: pd.DataFrame = explorer.data["trip"]
        station_df: pd.DataFrame = explorer.data["station"]
        status_df: pd.DataFrame = explorer.data["status"]
        self.weather_df: pd.DataFrame = explorer.data["weather"]
        
        del explorer.data["trip"]
        del explorer.data["station"]
        del explorer.data["status"]
        del explorer.data["weather"]
        
        gc.collect()
        
        
        '''
        
            A partir daqui faz todo o processamento para linkar os ids 
            do arquivo status com o arquivo estação na variável station_history
        
        '''
        
        station_sids = set(station_df["id"].unique())
        status_sids = set(status_df["station_id"].unique())
        id2term = {sid: station_df.loc[station_df["id"] == sid]["terminal"].iloc[0] if sid in station_sids else sid for sid in status_sids}
        
        self.station_history = {id2term[sid]: status_df.loc[status_df["station_id"] == sid].iloc[:, 1:].reset_index(drop=True) for sid in status_sids}
        self.station_trip = dict(tuple(trip_df.groupby('from_station_id')))
        self.usertype_trip = dict(tuple(trip_df.groupby('usertype')))
        
        print('Inicialização concluída!')
        
    
    def get_station_id(self, station_id:str):
        
        return station_id
    
    def get_bikes_qt(self, from_station_id:str):
        
        return self.station_history[from_station_id]['docks_available'].max()

    
    def get_wait_time(self, from_station_id:str):
        
        return self.station_trip[from_station_id]['tripduration'].mean()/60
    
    
    def get_month_name(self, month:int):
        
        arr_month = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                     'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        
        return arr_month[month]
    
    def get_month_users(self, from_station_id:str, month:int):

        return self.station_trip[from_station_id]['starttime'].dt.month.value_counts()[month]
    
    
    def get_dayWeek(self, dayWeek:int):
        
        arr_dayWeek = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']
        
        return arr_dayWeek
    
    
    def get_perc_dayWeek(self, from_station_id:str, dayWeek:int):
        
        tmp = self.station_trip[from_station_id]['starttime'].dt.day_name().value_counts()
        
        perc = (tmp[dayWeek]+random.randint(0, int(tmp.describe()['std'])))/tmp.sum()
        
        return perc
    
    def get_perc_hour(self, from_station_id:str, hours:list):
        perc = []
        
        for i in hours:
            tmp = self.station_trip[from_station_id]['starttime'].dt.strftime("%H").value_counts()
            perc.append((tmp[i]+random.randint(0, int(tmp.describe()['std'])))/tmp.sum())
        
        return perc
    
    
    def get_user_time(self, user_type:str):
        
        #O tempo do usuário é a média do tempo mais o desvio padrão
        segundos = self.usertype_trip[user_type]['tripduration'].describe()['mean'] +\
            random.randint(0, int(self.usertype_trip[user_type]['tripduration'].describe()['std']))
            
        return segundos / 3600
            
    
    def get_risk_of_rain(self, month:int):
        

        month_weather = dict(tuple(self.weather_df.groupby(self.weather_df['Date'].dt.month)))
        
        tmp = month_weather[month]['Events'].value_counts()
        
        perc = tmp.sum()/30
        
        return perc
    
    def get_all_stations_id(self):
        
        return self.station_trip.keys()
        
    
    













