# avec parentheses et "moins unaire"
# -*- coding: utf-8 -*-

import ply.yacc as yacc
import AST
from lex5 import tokens

def p_programme_statement(p):
    """ programme : statement"""
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
    """structure :  """

def p_expression_bool(p):
    """expression : expression_boolSimple
                    | expression_boolCombined """
    p[0] = p[1]
    
def p_expression_boolsimple(p):
    """expression_boolSimple : expression EST DIFFERENT DE expression
                    | expression EST EGAL TO expression
                    | expression EST SUPERIEUR TO expression
                    | expression EST INFERIEUR TO expression"""
    p[0] = AST.OpNode(p[3],[p[1],p[5]])

def p_expression_boolcombined(p):
    """expression_boolCombined : expression EST INFERIEUR OU EGAL TO expression
                    | expression EST SUPERIEUR OU EGAL TO expression"""
    p[0] = AST.OpNode(p[3]+p[5],[p[1],p[7]])

def p_structure_while(p):
    """structure : TANT QUE expression CROCHET_OPEN programme CROCHET_CLOSE"""
    p[0] = AST.WhileNode([p[3], p[5]])

def p_structure_si(p):
    """structure : SI expression ALORS ':' CROCHET_OPEN programme CROCHET_CLOSE"""
    p[0] = AST.SiNode([p[2], p[6]])

def p_for(p):
    """structure : FOR POUR VARIABLE DE NUMBER TO NUMBER PAR PAS DE NUMBER CROCHET_OPEN programme CROCHET_CLOSE"""
    p[0] = AST.ForNode([p[3],
                       AST.TokenNode(p[5]),
                       AST.TokenNode(p[7]),
                       AST.TokenNode(p[11]),
                       p[13]]);

def p_printExpression(p):
    """ printExpression : AFFICHE expression"""
    p[0] = AST.PrintNode(p[2])

def p_expression_case(p):
    """ expression : LA CASE expression DE VARIABLE"""
    p[0] = AST.GetValueAtNode([AST.TokenNode(p[5]), AST.TokenNode(p[3])])

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
    """expression : NUMBER"""
    p[0] = AST.TokenNode(p[1])

def p_expression_paren(p):
    """expression : '(' expression ')' """
    p[0] = p[2]

def p_minus(p):
    """expression : ADD_OP expression %prec UMINUS"""
    p[0] = AST.OpNode(p[1], [p[2]])

def p_createTable(p):
    """structure : VARIABLE EST UN TABLEAU DE TAILLE NUMBER"""
    p[0] = AST.CreateTableNode([AST.TokenNode(p[1]),AST.TokenNode(p[7])])

def p_affectTable(p):
    """structure : LA CASE expression DE VARIABLE AFFECTATION expression"""
    p[0] = AST.AffectTableNode([AST.TokenNode(p[5]), AST.TokenNode(p[3]), p[7]])

def p_comment(p):
    """statement : COMMENT statement
                   | COMMENT expression"""
    p[0] = AST.CommentNode(p[2])
    
def p_error(p):
    print("Syntax error in line %d" % p.lineno)
    print(p)
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
