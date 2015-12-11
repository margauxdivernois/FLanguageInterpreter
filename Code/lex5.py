#Avec les parentheses
# -*- coding: utf-8 -*-

import ply.lex as lex

reserved_words = (
    'while',
    'Affiche',
    'par',
	'de',
	'est',
	'a',
	'ou',
	'alors',
	'pour',
	'pas')

tokens = (
            'NUMBER',
            'ADD_OP',
            'MUL_OP',
            'ENDOFLINE',
            'CROCHET_OPEN',
            'CROCHET_CLOSE',
            'AFFECTATION',
            'VARIABLE',
            'SUPERIEUR',
            'INFERIEUR',
            'EGAL',
            'DIFFERENT',
            'STRING',
			'FOR',
			'TO',
         ) + tuple(map(lambda s: s.upper(), reserved_words))
### AJOUTE LES ELEMENTS DE reserved_words

literals = '():'

def t_ADD_OP(t):
    r'\plus|moins'
    return t

def t_MUL_OP(t):
    r'\multiplié|divisé'
    return t

def t_NUMBER(t):
    r'\d+[. ,]\d+|\d+'
    try:
        t.value = int(t.value)
    except:
        t.value = float(t.value)
    return t

def t_ENDOFLINE(t):
    r'~'
    return t

def t_SI(t):
    r'si'
    return t

def t_AFFECTATION(t):
    r'vaut'
    return t

def t_FOR(t):
    r'Répéte'
    return t

def t_SUPERIEUR(t):
    r'superieur'
    return t

def t_INFERIEUR(t):
    r'\inferieur'
    return t

def t_EGAL(t):
    r'egal'
    return t

def t_DIFFERENT(t):
    r'different'
    return t
def t_VARIABLE(t):
    r'[A-Za-z_]\w*'
    if t.value in reserved_words:
        t.type = t.value.upper()
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_CROCHET_OPEN(t):
    r'\['
    return t

def t_CROCHET_CLOSE(t):
    r'\]'
    return t

def t_STRING(t):
    r'\^.*\^'
    return t

def t_TO(t):
    r'à'
    return t

t_ignore = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lex.lex()

if __name__ == "__main__":
    import sys
    #prog = open(sys.argv[1]).read()
    prog = open("test.txt").read()
    lex.input(prog)

    while 1:
        tok = lex.token()
        if not tok: break
        print("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))
