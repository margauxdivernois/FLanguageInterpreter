# -*- coding: utf-8 -*-
import AST
from AST import addToClass
from functools import reduce

operations = {
    'plus' : lambda x,y : x+y,
    'moins' : lambda x,y : x-y,
    'multiplié' : lambda x,y : x*y,
    'divisé' : lambda x,y : x/y,
    'inférieur' : lambda x,y : x<y,
    'supérieur' : lambda x,y : x>y,
    'différent' : lambda x,y : x!=y,
    'égal' : lambda x,y : x==y,
    'superieuregal' : lambda x,y : x>=y,
    'inferieuregal' : lambda x,y : x<=y,
}

vars = {}

@addToClass(AST.ProgramNode)
def execute(self):
    for c in self.children:
        c.execute()

@addToClass(AST.TokenNode)
def execute(self):
    if isinstance(self.tok, str):
        try:
            return vars[self.tok]
        except KeyError:
            if self.tok[0] != '^':
               print ("*** ERROR: variable %s undefined!" %self.tok)
    return self.tok

@addToClass(AST.OpNode)
def execute(self):
    args = [c.execute() for c in self.children]
    if len(args) == 1:
        args.insert(0,0)
    return reduce(operations[self.op],args)

@addToClass(AST.AssignNode)
def execute(self):
    vars[self.children[0].tok] = self.children[1].execute()

@addToClass(AST.PrintNode)
def execute(self):
    result = self.children[0].execute()
    try :
        if result[0] == '^':
            ##result[1:-1] car on enlève les ^ de début et de fin [1:-1]
            result = result[1:-1]
    except Exception:
        pass              
    print(result)

@addToClass(AST.WhileNode)
def execute(self):
    while self.children[0].execute() :
        self.children[1].execute()

@addToClass(AST.SiNode)
def execute(self):
    if self.children[0].execute():
        self.children[1].execute()

@addToClass(AST.ForNode)
def execute(self):
    vars[self.children[0]] = self.children[1].tok
    start = self.children[1].tok
    stop = self.children[2].execute()
    step = self.children[3].execute()
    for i in range(start, stop, step):
        vars[self.children[0]] = i
        self.children[4].execute()

@addToClass(AST.CreateTableNode)
def execute(self):
    vars[self.children[0].tok] = [None] * self.children[1].execute()

@addToClass(AST.AffectTableNode)
def execute(self):
    indice = self.children[1].execute()
    if len(vars[self.children[0].tok]) < indice+1:
        print ("*** ERROR: CASE %s OUT OF RANGE !" %indice)
    else:
        vars[self.children[0].tok][indice] = self.children[2].execute()
    print(vars)

if __name__ == "__main__":

    from parser5 import parse
    import sys

    #fileName = sys.argv[1]
    fileName = "test.txt"
    prog = open(fileName).read()
    ast = parse(prog)

    ast.execute()
