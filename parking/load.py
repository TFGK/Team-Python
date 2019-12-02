import yaml

f = open(r"./data/parking_sapce_data.yml", 'r')
docs = yaml.load(f)
print(docs)
    