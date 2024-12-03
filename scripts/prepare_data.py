import os

os.makedirs('data/processed', exist_ok=True)
print('prepare data')
with open('data/processed/test.txt', 'w') as f:
    f.write('prepare data')
