import pandas as pd

dic = {'casa': 3, 'cantidad': 3}
df = pd.DataFrame(dic)
df.to_csv('prueba2.csv', index = False, mode = 'a' ) 
