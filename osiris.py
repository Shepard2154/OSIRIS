import pandas as pd
from twitter import getFollowers

def start():
    data = pd.read_csv('data/id_influencers.csv')
    data_id_list = list(data['id'])
    getFollowers(data_id_list,True)
    return ('oks')

if __name__ == "__main__":
    start()