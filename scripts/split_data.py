import os
os.makedirs('data/splits', exist_ok=True)
print('split data')
with open('data/splits/splits.txt', 'w') as f:
    f.write('split data')