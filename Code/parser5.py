# avec parentheses et "moins unaire"
# -*- coding: utf-8 -*-

import ply.yacc as yacc
import AST
from lex5 import tokens

def p_programme_statement(p):
    """ programme : statement """
    p[0] = AST.ProgramNode(p[1])

def p_programme_recursive(p):
    """ programme : statement ENDOFLINE programme"""
    p[0] = AST.ProgramNode([p[1]] + p[3].children)

def p_statement(p):
    """ statement : affectation
        | structure
        | printExpression"""
    p[0] = p[1]

def p_structure(p):
    """structure : WHILE expression CROCHET_OPEN programme CROCHET_CLOSE"""
    p[0] = AST.WhileNode([p[2], p[4]]);

def p_printExpression(p):
    """ printExpression : AFFICHE expression"""
    p[0] = AST.PrintNode(p[2])

def p_expression_affectation(p):
    """affectation : VARIABLE AFFECTATION expression"""
    p[0] = AST.AssignNode([AST.TokenNode(p[1]), p[3]])

def p_expression_variable(p):
    """expression : VARIABLE"""
    p[0] = AST.TokenNode(p[1])

def p_expression_string(p):
    """expression : STRING"""
    p[0] = AST.TokenNode(p[1])

def p_expression_opAdd(p):
    """expression : expression ADD_OP expression"""
    p[0] = AST.OpNode(p[2],[p[1],p[3]])

def p_expression_opMul(p):
    """expression : expression MUL_OP PAR expression"""
    p[0] = AST.OpNode(p[2],[p[1],p[4]])

def p_expression_num(p):
    """expression : number"""
    p[0] = AST.TokenNode(p[1])

def p_number(p):
    """number : NUMBER"""
    p[0] = AST.TokenNode(p[1])

def p_expression_paren(p):
    """expression : '(' expression ')' """
    p[0] = p[2]

def p_minus(p):
    """expression : ADD_OP expression %prec UMINUS"""
    p[0] = AST.OpNode(p[1], [p[2]])

def p_for(p):
    """structure : FOR POUR affectation TO number PAR PAS DE number CROCHET_OPEN programme CROCHET_CLOSE"""
    p[0] = AST.ForNode([p[3], p[5], p[9], p[11]]);
    
def p_error(p):
    print("Syntax error in line %d" % p.lineno)
    yacc.yacc().errok()


def parse(program):
    return yacc.parse(program)

precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('right', 'UMINUS')
)

yacc.yacc(outputdir='generated')

if __name__ == "__main__":
	import sys
	prog = open("test.txt").read()
	#prog = open(sys.argv[1]).read()
	result = yacc.parse(prog)
	print(result)

	#import os
	#graph = result.makegraphicaltree()
	#name = os.path.splitext("test.txt")[0]+'-ast.pdf'
	#graph.write_pdf(name)
	#print("Wrote AST to", name)
