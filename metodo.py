# from flask import Flask

# app = Flask(__name__)

# if __name__ == '__main__':
#     app.run(debug=True)

cadena = """

# Gboard Dictionary version:1

gg	Hola\\\nHol\\\nHo   es-MX
hh	Mariar\\\nHol\\\nHo es-MX

"""

with open('dictionary.txt', 'w', encoding='utf-8') as f:
    f.write(cadena)
