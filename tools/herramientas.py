def validar_caracteres_espacio(text):
    return text.isalpha() or text.isspace()

def validar_numeros(num):
    flag = False
    if num in '0123456789-':
        flag = True 
    return flag 

def entradas_vacias(*args):
    retorno = False
    for i in range(3):
        if len(args[i].get()) == 0:
            retorno =  True
    return retorno

def texto_formato_uper_sin_espacios(texto):
    return texto.rstrip().title()