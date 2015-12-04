import AST
from AST import addToClass
from functools import reduce

operations = {
    'plus' : lambda x,y : x+y,
    'moins' : lambda x,y : x-y,
    'multiplié' : lambda x,y : x*y,
    'divisé' : lambda x,y : x/y,
    'inferieur' : lambda x,y : x<y,
    'superieur' : lambda x,y : x>y,
    'different' : lambda x,y : x!=y,
    'egal' : lambda x,y : x==y,
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
            else:
                ##p[1][1:-1] car on enlève les ^ de début et de fin [1:-1]
                self.tok = self.tok[1:-1]
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
    print(self.children[0].execute())

@addToClass(AST.WhileNode)
def execute(self):
    while self.children[0].execute() != 0 :
        self.children[1].execute()

@addToClass(AST.SiNode)
def execute(self):
    if self.children[0].execute():
        self.children[1].execute()

if __name__ == "__main__":

    from parser5 import parse
    import sys

    #fileName = sys.argv[1]
    fileName = "test.txt"
    prog = open(fileName).read()
    ast = parse(prog)

    ast.execute()
