import mlflow

mlflow.start_run()
print('train model')
with open('models/output', 'w') as f:
    f.write('train model')
mlflow.end_run()
