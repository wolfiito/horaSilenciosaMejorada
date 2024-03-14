def sustituirVocales(cadena_sustituir_vocal):
    sustituciones = {
        'a': '1', 'á': '1',
        'e': '2', 'é': '2',
        'i': '3', 'í': '3',
        'o': '4', 'ó': '4',
        'u': '5', 'ú': '5'
    }

    return ''.join(sustituciones.get(caracter, caracter) for caracter in cadena_sustituir_vocal)