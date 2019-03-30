# Generated from C:\Users\Akira\Documents\python_code\github\antlr4_tex2sym\TeX2Sym.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .TeX2SymParser import TeX2SymParser
else:
    from TeX2SymParser import TeX2SymParser

# This class defines a complete generic visitor for a parse tree produced by TeX2SymParser.

class TeX2SymVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by TeX2SymParser#prog.
    def visitProg(self, ctx:TeX2SymParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#printExpr.
    def visitPrintExpr(self, ctx:TeX2SymParser.PrintExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#equal.
    def visitEqual(self, ctx:TeX2SymParser.EqualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#relation.
    def visitRelation(self, ctx:TeX2SymParser.RelationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#parens.
    def visitParens(self, ctx:TeX2SymParser.ParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#mult.
    def visitMult(self, ctx:TeX2SymParser.MultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#sqrtn.
    def visitSqrtn(self, ctx:TeX2SymParser.SqrtnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#trign.
    def visitTrign(self, ctx:TeX2SymParser.TrignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#sum.
    def visitSum(self, ctx:TeX2SymParser.SumContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#combi_permu.
    def visitCombi_permu(self, ctx:TeX2SymParser.Combi_permuContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#alphabet.
    def visitAlphabet(self, ctx:TeX2SymParser.AlphabetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#float.
    def visitFloat(self, ctx:TeX2SymParser.FloatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#braces.
    def visitBraces(self, ctx:TeX2SymParser.BracesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#div.
    def visitDiv(self, ctx:TeX2SymParser.DivContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#lim.
    def visitLim(self, ctx:TeX2SymParser.LimContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#PlusExpr.
    def visitPlusExpr(self, ctx:TeX2SymParser.PlusExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#diffn1.
    def visitDiffn1(self, ctx:TeX2SymParser.Diffn1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#diffn2.
    def visitDiffn2(self, ctx:TeX2SymParser.Diffn2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#function.
    def visitFunction(self, ctx:TeX2SymParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#power.
    def visitPower(self, ctx:TeX2SymParser.PowerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#mull.
    def visitMull(self, ctx:TeX2SymParser.MullContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#dintegrate.
    def visitDintegrate(self, ctx:TeX2SymParser.DintegrateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#frac.
    def visitFrac(self, ctx:TeX2SymParser.FracContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#MinusExpr.
    def visitMinusExpr(self, ctx:TeX2SymParser.MinusExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#greek.
    def visitGreek(self, ctx:TeX2SymParser.GreekContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#AddSub.
    def visitAddSub(self, ctx:TeX2SymParser.AddSubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#diff.
    def visitDiff(self, ctx:TeX2SymParser.DiffContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#int.
    def visitInt(self, ctx:TeX2SymParser.IntContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#integrate.
    def visitIntegrate(self, ctx:TeX2SymParser.IntegrateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#factrial.
    def visitFactrial(self, ctx:TeX2SymParser.FactrialContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#abs.
    def visitAbs(self, ctx:TeX2SymParser.AbsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#gammaf_zetaf.
    def visitGammaf_zetaf(self, ctx:TeX2SymParser.Gammaf_zetafContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#func.
    def visitFunc(self, ctx:TeX2SymParser.FuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#logub.
    def visitLogub(self, ctx:TeX2SymParser.LogubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#mathconst.
    def visitMathconst(self, ctx:TeX2SymParser.MathconstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TeX2SymParser#seqterm.
    def visitSeqterm(self, ctx:TeX2SymParser.SeqtermContext):
        return self.visitChildren(ctx)



del TeX2SymParser