import pandas as pd
import numpy as np
import os

path = 'Textos/'
filelist = os.listdir(path)
filelist.sort()
filelist.remove('Promulgacion.txt')

texto_total = ''

for file in filelist[:-1]:
    with open(path+file, 'r', encoding = 'utf-8') as f:
        text = f.read()
        if text[-1:] != '\n':
            text = text+'\n'
        else:
            text = text
    
    texto_total = texto_total + text

serie = texto_total.split('\n')

df = pd.DataFrame({'texto':serie})
df['texto'] = df['texto'].str.strip()

df['capitulo'] = np.where(df['texto'].str.contains('Preámbulo'),df['texto'],np.nan)
df['capitulo'] = np.where(df['texto'].str.contains('DISPOSICIONES TRANSITORIAS'),df['texto'],df['capitulo'])
df['capitulo'] = np.where(df['texto'].str.contains('Capítulo'),df['texto'],df['capitulo'])
df['capitulo'] = np.where(df['texto'].str.contains('DECIMOSEXTA'),np.nan,df['capitulo'])
df['capitulo'] = np.where(df['texto'].str.contains('Los procesos iniciados, de oficio o a petición de parte, o que se iniciaren en la Corte Suprema'),np.nan,df['capitulo'])
df['capitulo'] = np.where(df['texto'].str.contains('Las contiendas de competencia actualmente trabadas ante la Corte Suprema'),np.nan,df['capitulo'])
df['capitulo'] = np.where(df['texto'].str.contains('En lo no previsto en este Capítulo, serán aplicables'),np.nan,df['capitulo'])
#Para asegurar que aparezca el capitulo IV
df['articulo'] = np.where(df['texto'].str.contains('Artículo'),df['texto'],np.nan)
df['texto'] = np.where(df['texto']=='', np.nan, df['texto'])
df['texto'] = np.where(df['texto']==df['articulo'], np.nan, df['texto'])
df['texto'] = np.where(df['texto']==df['capitulo'], np.nan, df['texto'])
# Agregar numeral y ordinal (??)
df['nro_articulo'] = df['articulo'].str.split('.- ', expand = True)[0]
df['txt_articulo'] = df['articulo'].str.split('.- ', expand = True)[1]

df['capitulo'].fillna(method='pad', inplace=True)
df['nro_articulo'].fillna(method='pad', inplace=True)

df['texto'] = np.where(df['texto'].isna(), df['txt_articulo'], df['texto'])
df.dropna(subset=['texto'], inplace = True)
df['nro_capitulo'] = df['capitulo'].str.split(':', expand = True)[0]
df['nro_capitulo'] = df['nro_capitulo'].str.replace('# ','')
df['titulo_capitulo'] = df['capitulo'].str.split(':', expand = True)[1]
df['titulo_capitulo'] = df['titulo_capitulo'].str.strip()

df['titulo_capitulo'] = np.where(df['titulo_capitulo'].isna(), df['nro_capitulo'], df['titulo_capitulo'])
df = df[['nro_capitulo','titulo_capitulo','nro_articulo','texto']]
df.rename(columns = {'nro_capitulo':'capitulo'}, inplace = True)
df['nro_articulo'] = np.where(df['texto']=='Presidente de la República','Artículo 24', df['nro_articulo'])

df_capitulos = df[df['capitulo']!='DISPOSICIONES TRANSITORIAS']

texto_total = ''

for file in filelist[-1:]:
    with open(path+file, 'r', encoding = 'utf-8') as f:
        text = f.read()
        if text[-1:] != '\n':
            text = text+'\n'
        else:
            text = text
    
    texto_total = texto_total + text

serie = texto_total.split('\n')

df = pd.DataFrame({'texto':serie})
df['texto'] = df['texto'].str.strip()

df['titulo_capitulo'] = 'DISPOSICIONES TRANSITORIAS'
df['capitulo'] = 'DISPOSICIONES TRANSITORIAS'
df['nro_capitulo'] = 'DISPOSICIONES TRANSITORIAS'

df['capitulo'] = np.where(df['texto'].str.contains('DECIMOSEXTA'),np.nan,df['capitulo'])
df['capitulo'] = np.where(df['texto'].str.contains('Los procesos iniciados, de oficio o a petición de parte, o que se iniciaren en la Corte Suprema'),np.nan,df['capitulo'])
df['capitulo'] = np.where(df['texto'].str.contains('Las contiendas de competencia actualmente trabadas ante la Corte Suprema'),np.nan,df['capitulo'])
df['capitulo'] = np.where(df['texto'].str.contains('En lo no previsto en este Capítulo, serán aplicables'),np.nan,df['capitulo'])
#Para asegurar que aparezca el capitulo IV
df['articulo'] = np.where(df['texto'].str.contains('Artículo'),df['texto'],np.nan)
df['texto'] = np.where(df['texto']=='', np.nan, df['texto'])
df['texto'] = np.where(df['texto']==df['articulo'], np.nan, df['texto'])
df['texto'] = np.where(df['texto']==df['capitulo'], np.nan, df['texto'])
# Agregar numeral y ordinal (??)
df['nro_articulo'] = df['articulo'].str.split('.- ', expand = True)[0]
df['nro_articulo'] = df['texto'].str.split('.- ', expand = True)[0]
df['texto'] = df['texto'].str.split('.- ', expand = True)[1]

df['nro_articulo'] = np.where(df['nro_articulo']==df['texto'], np.nan, df['nro_articulo'])
df['txt_articulo'] = df['articulo'].str.split('.- ', expand = True)[1]

df['capitulo'].fillna(method='pad', inplace=True)
df['nro_articulo'].fillna(method='pad', inplace=True)

df['texto'] = np.where(df['texto'].isna(), df['txt_articulo'], df['texto'])
df.dropna(subset =['texto'], inplace = True)

df = df[['nro_capitulo','capitulo','titulo_capitulo','nro_articulo','texto']]

df_DT = df[df['capitulo']=='DISPOSICIONES TRANSITORIAS']


df_DT = df_DT[['capitulo','titulo_capitulo','nro_articulo','texto']]

df = df_capitulos.append(df_DT)
df = df.reset_index(drop=True)
df = df.reset_index()
df.columns = ['id', 'capitulo', 'titulo_capitulo', 'nro_articulo', 'texto']
#df['text'] = df.groupby(['capitulo','titulo_capitulo','nro_articulo'])['texto'].transform(lambda x: ' '.join(x))
#df = df[['capitulo','titulo_capitulo','nro_articulo', 'text']].drop_duplicates().reset_index(drop=True)

df.to_csv('data/processed/constitucion_actual.csv', index=False)
