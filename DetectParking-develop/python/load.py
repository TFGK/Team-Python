import yaml

f = open(r"../datasets/parking2.yml", 'r')

docs = yaml.load(f)
print(docs)
    