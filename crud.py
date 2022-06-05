# -*- coding: utf-8 -*-
"""
Created on Tue May 17 22:36:44 2022

@author: Omotade
"""


from sqlalchemy.orm import sessionmaker
from tqdm.std import tqdm
from extract import extract_coindata
from models import Crypto
from config import cloud_engine
from datetime import datetime
import logging
logger = logging.Logger('catch_all')

coindata = extract_coindata()
Session = sessionmaker(bind=cloud_engine)

def load_data(data = coindata, s = Session()):
    start = datetime.now()
    #s = Session()
    cols = list(data[0].keys())
    
    try:
        for coin in tqdm(data, desc="Inserting data into {} table".format(Crypto.__tablename__)):
            vals = list(coin.values())
            s.rollback()
            query = '''INSERT INTO public."CryptoPrice" ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}") 
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}', '{}')'''\
            .format(cols[0], cols[1], cols[2], cols[3], cols[4], cols[5], cols[6], cols[7], cols[8], cols[9], 
            vals[0], vals[1], vals[2], vals[3], vals[4], vals[5], vals[6], vals[7], vals[8], vals[9])

            s.execute(query)
            s.commit()
        stop = datetime.now()  
        
        print('Batch Load Executed!!!')
        print("Total time: {} seconds".format(stop-start))
        
    except Exception as e:
        logger.error(e, exc_info=True)
        print("Could not load data into database")
        
    finally:
        s.close()
        
        