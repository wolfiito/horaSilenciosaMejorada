# def espaciar_cadena(cadena_a_espaciar):

#     resultado = ''
    
#     for i, caracter in enumerate(cadena_a_espaciar):
#         if i < len(cadena_a_espaciar) - 1 and caracter != ' ':
#             resultado += caracter + ' '
#         else:
#             pass
#     return resultado.strip()

def espaciar_cadena(cadena_a_espaciar):
    
    return ' '.join(c for c in cadena_a_espaciar if c != ' ')

# Ejemplo de uso
cadena_original = "hola amigos"
cadena_espaciada = espaciar_cadena(cadena_original)
print(cadena_espaciada)

with open('text.txt', 'w') as file:
    file.write(cadena_espaciada)
