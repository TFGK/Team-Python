import pickle

with open('config.pkl', 'rb') as file:
    data = pickle.load(file)

print(data)

