# antlr4_tex2sym.py   Author: Akira Hakuta, Date: 2019/04/05 
# python.exe antlr4_tex2sym.py

import sys
import antlr4
from gen.TeX2SymLexer import TeX2SymLexer
from gen.TeX2SymParser import TeX2SymParser
from gen.TeX2SymVisitor import TeX2SymVisitor
from sympy import * 

# variable : a,b,...,z, A,B,..,Z, \\alpha, \\beta,..,\pi,... , \\omega (except E, I, N, O, S, zeta, omicron)
# math constant : pi; --> \\ppi, i --> \\ii, e --> \\ee
# LaTeX Code Style: \\sin{x},  \\log\_{2}{8}, \\sum\_{k=1}\^{n}{k(k+1)\^2},...


class LaTeX2SymPyVisitor(TeX2SymVisitor):
    
    def visitPrintExpr(self, ctx):
        value = self.visit(ctx.expr())
        return value


    def visitInt(self, ctx):
        return ctx.INT().getText()

        
    def visitFloat(self, ctx):
        float_str=ctx.FLOAT().getText()
        return 'nsimplify({:s})'.format(float_str)


    def visitAlphabet(self, ctx):
        return ctx.ALPHABET().getText()

        
    def visitGreek(self, ctx):
        return ctx.GREEK().getText()
    

    def visitMult(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))       
        return '{:s}*{:s}'.format(left,right)
        
        
    def visitDiv(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))       
        return '{:s}*{:s}**(-1)'.format(left,right)

        
    def visitMull(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        return '{:s}*{:s}'.format(left,right)
        

    def visitAddSub(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        if ctx.op.type == TeX2SymParser.PLUS:
            return '{:s}+{:s}'.format(left,right)
        else:
            return '{:s}-{:s}'.format(left,right)

            
    def visitCs_parens(self, ctx):
        expr = self.visit(ctx.expr())
        return '({:s})'.format(expr)


    def visitParens(self, ctx):
        expr = self.visit(ctx.expr())
        return '({:s})'.format(expr)
        
    
    def visitCs_bs_braces(self, ctx):
        expr = self.visit(ctx.expr())
        return '({:s})'.format(expr)


    def visitBs_braces(self, ctx):
        expr = self.visit(ctx.expr())
        return '({:s})'.format(expr)


    def visitBraces(self, ctx):
        expr = self.visit(ctx.expr())
        return '({:s})'.format(expr)
        
        
    def visitPower(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        return '{:s}**{:s}'.format(left,right)
        
        
    def visitFactrial(self, ctx):
        expr = self.visit(ctx.expr())       
        return 'factorial({:s})'.format(expr)
        
        
    def visitFunc(self, ctx):
        expr = self.visit(ctx.expr())
        if ctx.func.type == TeX2SymParser.SQRT:
            result='sqrt({:s})'.format(expr)
        elif ctx.func.type == TeX2SymParser.SIN:
            result='sin({:s})'.format(expr)
        elif ctx.func.type == TeX2SymParser.COS:
            result='cos({:s})'.format(expr)
        elif ctx.func.type == TeX2SymParser.TAN:
            result='tan({:s})'.format(expr)
        elif ctx.func.type == TeX2SymParser.LOG:
            result='log({:s})'.format(expr)
        return result
        
        
    def visitSqrtn(self, ctx):
        expr1 = self.visit(ctx.expr(0))
        expr2 = self.visit(ctx.expr(1))     
        return '(({:s})**(({:s})**(-1)))'.format(expr2,expr1)
        
        
    def visitLogub(self, ctx):
        expr0 = self.visit(ctx.expr(0))
        expr1 = self.visit(ctx.expr(1))     
        return 'log({})*(log({})**(-1))'.format(expr1,expr0)
        
        
    def visitAbs(self, ctx):
        expr = self.visit(ctx.expr())
        return 'Abs({})'.format(expr)
        
        
    def visitTrign(self, ctx):
        expr1 = self.visit(ctx.expr(0))
        expr2 = self.visit(ctx.expr(1))        
        if ctx.func.type == TeX2SymParser.SIN:
            result='(sin({:s}))**({:s})'.format(expr2,expr1)
        elif ctx.func.type == TeX2SymParser.COS:
            result='(cos({:s}))**({:s})'.format(expr2,expr1)
        elif ctx.func.type == TeX2SymParser.TAN:
            result='(tan({:s}))**({:s})'.format(expr2,expr1)
        return result
        
        
    def visitFrac(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        return '({:s})*({:s})**(-1)'.format(left, right)


    def visitSum(self, ctx):        
        expr0= self.visit(ctx.expr(0))
        expr1 = self.visit(ctx.expr(1))
        expr2 = self.visit(ctx.expr(2))
        expr3 = self.visit(ctx.expr(3))
        return 'summation({:s},({:s},{:s},{:s}))'.format(expr3,expr0,expr1,expr2)
        
        
    def visitDiff(self, ctx):
        expr = self.visit(ctx.expr())
        if ctx.dxg.type == TeX2SymParser.DX:
            symb = ctx.DX().getText()[1]
        elif ctx.dxg.type == TeX2SymParser.DGREEK:
            symb = ctx.DGREEK().getText()[1:]
        return 'diff({:s},{:s})'.format(expr,symb)
        
        
    def visitDiffn1(self, ctx):
        expr0 = self.visit(ctx.expr(0))
        expr1 = self.visit(ctx.expr(1))
        if ctx.dxg.type == TeX2SymParser.DX:
            symb = ctx.DX().getText()[1]
        elif ctx.dxg.type == TeX2SymParser.DGREEK:
            symb = ctx.DGREEK().getText()[1:]
        return 'diff({:s},{:s},{:s})'.format(expr1,symb,expr0)
        
        
    def visitDiffn2(self, ctx):
        expr0 = self.visit(ctx.expr(0))
        expr1 = self.visit(ctx.expr(1))
        expr2 = self.visit(ctx.expr(2))
        if expr0 != expr1:
            return None
        if ctx.dxg.type == TeX2SymParser.DX:
            symb = ctx.DX().getText()[1]
        elif ctx.dxg.type == TeX2SymParser.DGREEK:
            symb = ctx.DGREEK().getText()[1:]
        return 'diff({:s},{:s},{:s})'.format(expr2,symb,expr0)
        
        
    def visitIntegrate(self, ctx):
        expr = self.visit(ctx.expr())
        if ctx.dxg.type == TeX2SymParser.DX:
            symb = ctx.DX().getText()[1]
        elif ctx.dxg.type == TeX2SymParser.DGREEK:
            symb = ctx.DGREEK().getText()[1:]
        return 'integrate({:s},{:s})'.format(expr,symb)
        
        
    def visitDintegrate(self, ctx):
        expr0 = self.visit(ctx.expr(0))
        expr1 = self.visit(ctx.expr(1))
        expr2 = self.visit(ctx.expr(2))
        if ctx.dxg.type == TeX2SymParser.DX:
            symb = ctx.DX().getText()[1]
        elif ctx.dxg.type == TeX2SymParser.DGREEK:
            symb = ctx.DGREEK().getText()[1:]
        return 'integrate({:s},({:s},{:s},{:s}))'.format(expr2,symb,expr0,expr1)
        
        
    def visitLim(self, ctx):
        expr0 = self.visit(ctx.expr(0))
        expr1 = self.visit(ctx.expr(1))
        expr2 = self.visit(ctx.expr(2))        
        return 'limit({:s}, {:s}, {:s})'.format(expr2,expr0,expr1)
        
        
    def visitCombi_permu(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        if ctx.cp.type == TeX2SymParser.COMBI:
            result='binomial({:s},{:s})'.format(left,right)
        elif ctx.cp.type == TeX2SymParser.PERMU:
            result='ff({:s},{:s})'.format(left,right)
        return result
        
     
    def visitSeqterm(self, ctx):
        expr = self.visit(ctx.expr())       
        return 'F({})'.format(expr)
        
        
    def visitFunction(self, ctx):
        expr = self.visit(ctx.expr())       
        return 'f({})'.format(expr)
        
        
    def visitGammaf_zetaf(self, ctx):
        expr = self.visit(ctx.expr()) 
        if ctx.gz.type == TeX2SymParser.GAMMAF:
            result='gamma({})'.format(expr)
        elif ctx.gz.type == TeX2SymParser.ZETAF:
            result='zeta({})'.format(expr)
        return result
        
        
    def visitPlusExpr(self, ctx):
        expr = self.visit(ctx.expr())       
        return expr
        
        
    def visitMinusExpr(self, ctx):
        expr = self.visit(ctx.expr())       
        return '(-1)*' + expr    
        
        
    def visitMathconst(self, ctx):
        if ctx.const.type == TeX2SymParser.PI:
            result='S.Pi'
        elif ctx.const.type == TeX2SymParser.IMAGINARY_UNIT:
            result='S.ImaginaryUnit'
        elif ctx.const.type == TeX2SymParser.NAPIER_CONSTANT:
            result='S.Exp1'    
        elif ctx.const.type == TeX2SymParser.INFTY:
            result='oo' 
        return result
        
        
    def visitEqual(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        return 'Eq({:s},{:s})'.format(left,right)
        
        
    def visitRelation(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        if ctx.op.type == TeX2SymParser.GT:
            return '{:s}>{:s}'.format(left,right)
        elif ctx.op.type == TeX2SymParser.LT:
            return '{:s}<{:s}'.format(left,right)
        elif ctx.op.type == TeX2SymParser.GEQQ:
            return '{:s}>={:s}'.format(left,right)
        elif ctx.op.type == TeX2SymParser.LEQQ:
            return '{:s}<={:s}'.format(left,right)
            
            
            

greek_list = [['\\alpha', 'aalpha'], ['\\beta', 'bbeta'], ['\\gamma', 'ggamma'], ['\\delta', 'ddelta'], ['\\epsilon', 'eepsilon'], 
    ['\\eta', 'eeta'], ['\\theta', 'ttheta'], ['\\iota', 'iiota'], ['\\kappa', 'kkappa'], ['\\lambda', 'llambda'], ['\\mu', 'mmu'], 
    ['\\nu', 'nnu'], ['\\xi', 'xxi'],    ['\\omicron', 'oomicron'], ['\\pi', 'pppi'], ['\\rho', 'rrho'], ['\\sigma', 'ssigma'],
    ['\\tau', 'ttau'], ['\\upsilon', 'uupsilon'], ['\\phi', 'pphi'], ['\\chi', 'cchi'], ['\\psi', 'ppsi'], ['\\omega', 'oomega']]
    
    

def tex2sym(texexpr):
    if texexpr == '':
        return ''
    replace_list = [['\\!',' '],['\\,',' '],['\\:',' '],['\\;',''],['~',' ']]
    for el in greek_list:
        replace_list.append(el)
    #print(replace_list)
    for le in replace_list:
        texexpr=texexpr.replace(le[0],le[1])
    expr=antlr4.InputStream(texexpr+'\n')
    lexer = TeX2SymLexer(expr)
    token_stream = antlr4.CommonTokenStream(lexer)
    parser = TeX2SymParser(token_stream)
    tree = parser.prog()
    visitor = LaTeX2SymPyVisitor()
    result=visitor.visit(tree)
    return result


def mylatex(sympyexpr):
    texexpr = latex(sympyexpr)
    for le in greek_list:
        texexpr=texexpr.replace(le[1],le[0]+' ') 
    return texexpr

    
def mylatexstyle(texexpr):
    replace_list=[['\\ii',' i '],['\\ee',' e '],['\\ppi','\\pi '],['\\C','\\mathrm{C}'],['\\P','\\mathrm{P}']]
    for le in replace_list:
        texexpr=texexpr.replace(le[0],le[1]) 
    return texexpr


def test(texexpr):
    print(texexpr.replace('\\','\\\\')+' --> '+ tex2sym(texexpr))
    
    
if __name__ == '__main__':
    print('tex2sym: LaTeX math expression --> SymPy form')
    test('-2-3+4')
    test('2\\times3^4')
    test('0.5 \\times 3 \\div 5a\\cdot 4')
    test('2\\times3!')
    test('2ab^2(x+y)^3')
    test('\\sqrt{3x}')
    test('\\frac{2}{3}a')
    test('\\dfrac{2}{3}a')
    test('\\sin {\\ppi x}')
    test('\\log{\\ee^3}')
    test('\\frac{d}{dx}{x^5}')
    test('\\int{\\sin^{2}{\\theta} d\\theta}')
    test('\\sum_{k=1}^{n}{k^3}')       
    test('2x^2+3x+4=0')
    test('3x^2-4x+5 \\geqq 0')
    test('\\frac{d^{2}}{dx^{2}}{f(x)}=-f(x)')
    test('\\alpha\\beta\\gamma\\delta\\epsilon\\eta\\theta\\iota\\kappa\\lambda\\mu\\nu\\xi\\pi\\rho\\sigma\\tau\\upsilon\\phi\\chi\\psi\\omega\\ppi')   
    test('(a\\!aa\\,a\\:a\\;a~a)^3')
    test('\\{\\dfrac{1}{~2~}a-(\\dfrac{1}{~3~}b-\\dfrac{1}{~4~}c)\\}^2')
    test(r'\left\{\dfrac{1}{~2~}a-\left(\dfrac{1}{~3~}b-\dfrac{1}{~4~}c\right)\right\}^2')
    
    