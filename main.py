import re
#la funcion sirve para hacer split de expresiones
#y que podamos trabajar con una unica declaracion a la vez
# hacemos split por comas y puntos y comas, siempre que 
# estos no formen parte de la declaración de un arreglo
# o esten dentro de un string 
def procesaEntrada(linea):
  #eliminamos el espacio despues de puntos y coma
  linea = re.sub(r"; +(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)", ";", linea)
  iteradorPuntoComaFueraStrings = re.finditer(r"(;(?![^\[]+\]))", linea)
  puntosComaFueraStrings = [match.start(0) for match in iteradorPuntoComaFueraStrings]

  #ponemos un espacio frente a comas que no van dentro de strings 
  linea = re.sub(r",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)", ", ", linea)
  #obtenemos los indices de las comas que estan dentro de strings o 
  #declaraciones de arreglos 
  iteradorComasArreglos = re.finditer(r"(,(?![^\[]+\]))", linea)
  comasDentroArreglos = [match.start(0) for match in iteradorComasArreglos]
  iteradorComasStrings = re.finditer(r",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)", linea)
  comasDentroStrings= [match.start(0) for match in iteradorComasStrings]
  interseccion = set(comasDentroStrings).intersection(comasDentroArreglos)
  comasOPuntoComa = list(interseccion.union(puntosComaFueraStrings))
  indices = [-1]
  indices.extend(comasOPuntoComa)
  indices.sort()
  indices.append(len(linea))
  #hacemos el split
  declaraciones = [linea[indices[i]+1:indices[i+1]] for i in range(len(indices)-1)]
  return declaraciones


def procesaDeclaracion(declaracion, varsDeclaradas, inicializadas):
  print(declaracion)
  nombreVariable = (re.search('(?<=\s)[a-zA-Z][a-zA-Z0-9_]*',declaracion)).group(0)
  x = re.search('[:=]+?', declaracion)
  #tenemos que definir el tipo de variable para ponerla en el diccionario
  # y ver si esta inicializada o no

  #caso en que te dan el tipo
  if(x.group(0) == ":"):
    primerIgual = re.search('[=]+?', declaracion)
    if primerIgual is None:
      tipoVar = re.sub(r"\s+", "", declaracion[x.start()+1 : ])
    else:
      tipoVar = re.sub(r"\s+", "", declaracion[x.start()+1 : primerIgual.start()])
      inicializadas[0] = inicializadas[0] + 1
    tipoArreglo = re.search('\[|Array',tipoVar)
    if tipoArreglo is None:
      varsDeclaradas[tipoVar].append(nombreVariable)
    else:
      varsDeclaradas['Array'].append(nombreVariable)
  #caso en que no te dan el tipo
  else:
    inicializadas[0] = inicializadas[0] + 1
    #nos quedamos solo con la parte del igual y quitamos los espacios iniciales
    valor = re.sub(r"^\s+", "", declaracion[x.start()+1 : ])
    tipoArray = re.search(r"^[\[|Array]", valor)
    tipoBool = re.search(r'^[false|true]+', valor)
    tipoDouble = re.search(r'^([0-9]+[.][0-9]+)', valor)
    #el tipo Entero va a funcionar porque primero descartaremos el tipoDouble
    #aunque aqui parezca que si tenemos un Double, estamos tambien pensando que 
    #es un entero
    tipoInt = re.search(r'^[0-9]+', valor)
    
    #anexamos el nombre de la variable al tipo adecuado
    if tipoArray is not None:
      varsDeclaradas['Array'].append(nombreVariable)
    elif tipoBool is not None:
      varsDeclaradas['Bool'].append(nombreVariable)
    elif tipoDouble is not None:
      varsDeclaradas['Double'].append(nombreVariable)
    elif tipoInt is not None:
      varsDeclaradas['Int'].append(nombreVariable)
    else:
      varsDeclaradas['String'].append(nombreVariable)


linea = input()
reachedEOF = False

inicializadas = [0]

varsDeclaradas = {}
varsDeclaradas['Character'] = []
varsDeclaradas['String'] = []
varsDeclaradas['Character'] = []
varsDeclaradas['Bool'] = []
varsDeclaradas['Int'] = []
varsDeclaradas['Float'] = []
varsDeclaradas['Double'] = []
varsDeclaradas['Array'] = []

while(not reachedEOF):
  declaraciones = procesaEntrada(linea)
  print(declaraciones)
  for declaracion in declaraciones:
    procesaDeclaracion(declaracion, varsDeclaradas, inicializadas)
    #contestar preguntas
  try:
    linea = input()
  except:
    reachedEOF = True

totalDeclaradas = 0  
tiposUtilizados = []
for tipo, variables in varsDeclaradas.items():
    totalDeclaradas += len(variables)
    if len(variables) > 0:
        tiposUtilizados.append(tipo)

print("Número total de variables declaradas:", totalDeclaradas,'\n')
print('Número de tipos utilizados:', len(tiposUtilizados))
print('\tlos tipos fueron: ', tiposUtilizados,'\n', sep="")
print('Número de variables declaradas por tipo:\n')
for tipo, variables in varsDeclaradas.items():
    print('\t',tipo,': ', len(variables), sep = "")
print('Número de variables inicializadas:', inicializadas[0],'\n')
print('Número total de variables tipo arreglo:', len(varsDeclaradas['Array']), '\n')
print('Clasificación de variables por tipo:')
for tipo, variables in varsDeclaradas.items():
    print('\t',tipo,': ', variables, sep="")
 
