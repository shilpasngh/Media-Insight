import json
print('test model')

with open('metrics/test.json', 'w') as f:
    json.dump({'accuracy': 0.95}, f)