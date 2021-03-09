import pandas as pd
import re
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from urllib.request import urlopen
from bs4 import BeautifulSoup

url = 'http://www.comvest.unicamp.br/estatisticas-comvest/vestibulares/vestibulares-anteriores/estatisticas-do-vestibular-2020/notas-dos-ultimos-matriculados-2020/'
html = urlopen(url)
bs = BeautifulSoup(html, 'lxml')

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def gerar_df(url):
  html = urlopen(url)
  bs = BeautifulSoup(html, 'lxml')

  linhas = list(bs.find_all('tr'))

  # Tirando o cabeçalho
  for i in range(4):
    linhas.pop(0)

  cursos = []

  # Sem Cotas
  nc_v = []
  nc_a1 = []
  nc_cv = []
  nc_nm = []

  # Cotas
  sc_v = []
  sc_a1 = []
  sc_cv = []
  sc_nm = []

  # Geral
  g_v = []
  g_a1 = []
  g_cv = []
  g_nm = []

  #Grupos de classificação
  nc_g1 = []
  nc_g2 = []
  sc_g1 = []
  sc_g2 = []

  for i in range(0, len(trs)-1):
    linha = cleanhtml(str(trs[i]))
    linha.replace(',', '.')
    linha = linha.split('\n')[1:-1]
    if (len(linha) > 18):
      cursos.append('Curso 51')
    else:
      cursos.append(linha[0])

    # Sem Cotas
    nc_v.append(linha[1])
    nc_a1.append(linha[2])
    nc_cv.append(linha[3])
    nc_nm.append(linha[4])

    # Com Cotas
    sc_v.append(linha[5])
    sc_a1.append(linha[6])
    sc_cv.append(linha[7])
    sc_nm.append(linha[8])

    # Geral Cotas
    g_v.append(linha[9])
    g_a1.append(linha[10])
    g_cv.append(linha[11])
    g_nm.append(linha[12])

    # Grupos
    nc_g1.append(linha[13])
    nc_g2.append(linha[14])
    sc_g1.append(linha[15])
    sc_g2.append(linha[16])

  sem_cota = [nc_v, nc_a1, nc_cv, nc_nm]
  com_cota = [sc_v, sc_a1, sc_cv, sc_nm] 
  geral = [g_v, g_a1, g_cv, g_nm]
  grupos = [nc_g1, nc_g2, sc_g1, sc_g2]
  
  sem_cotas = pd.DataFrame({'Cursos': cursos, 'Vagas': sem_cota[0], 'Aprovados 1ª Fase': sem_cota[1], 'Relação C/V 2ª Fase': sem_cota[2], 'Notas Mínimas de Aprovação': sem_cota[3]})
  com_cotas = pd.DataFrame({'Cursos': cursos, 'Vagas': com_cota[0], 'Aprovados 1ª Fase': com_cota[1], 'Relação C/V 2ª Fase': com_cota[2], 'Notas Mínimas de Aprovação': com_cota[3]})
  geral = pd.DataFrame({'Cursos': cursos, 'Vagas': geral[0], 'Aprovados 1ª Fase': geral[1], 'Relação C/V 2ª Fase': geral[2], 'Notas Mínimas de Aprovação': geral[3]})
  notas_grupos = pd.DataFrame({'Cursos': cursos, 'Vagas': grupos[0], 'Aprovados 1ª Fase': grupos[1], 'Relação C/V 2ª Fase': grupos[2], 'Notas Mínimas de Aprovação': grupos[3]})
  return (sem_cotas, com_cotas, geral, notas_grupos)

sem_cota, com_cota, geral, grupos = gerar_df('http://www.comvest.unicamp.br/estatisticas-comvest/vestibulares/vestibulares-anteriores/estatisticas-do-vestibular-2020/notas-dos-ultimos-matriculados-2020/')
