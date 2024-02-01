from sly import Parser
from calc_lex import CalcLexer
import math

MAX_NUM = 1234577

def inversion(a, mod):
    i = 0
    b = 0
    while(b != 1):
        b += a
        b %= mod
        i += 1
    
    return i % mod

    
def divide(a, b, mod):
    b1 = inversion(b, mod)
    return (a * b1) % mod


class CalcParser(Parser):
    rpn = ""
    error_flag = 0
    
    tokens = CalcLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ('right', UMINUS),
        ('left', POW),   
    )

    
    @_('expr PLUS expr')
    def expr(self, p):
        self.rpn += "+ "
        return ((p.expr0)% MAX_NUM + (p.expr1)% MAX_NUM) % MAX_NUM


    @_('expr MINUS expr')
    def expr(self, p):
        self.rpn += "- "
        return ((p.expr0)% MAX_NUM - (p.expr1)% MAX_NUM) % MAX_NUM


    @_('expr TIMES expr')
    def expr(self, p):
        self.rpn += "* "
        return ((p.expr0)% MAX_NUM * (p.expr1) % MAX_NUM) % MAX_NUM


    @_('expr DIVIDE expr')
    def expr(self, p):
        self.rpn += "/ "
        
        if(math.gcd(p.expr1, MAX_NUM) != 1):
            print("Error: ", p.expr1, "nie jest odwracalne modulo", MAX_NUM)
            self.error_flag = 1
            return -1
        return divide(p.expr0 % MAX_NUM, p.expr1 % MAX_NUM, MAX_NUM) % MAX_NUM
    
    
    @_('expr POW pow_expr')
    def expr(self, p):
        self.rpn += "^ "
        return pow(p.expr % MAX_NUM, p.pow_expr % MAX_NUM, MAX_NUM) % MAX_NUM


    @_('NUMBER')
    def expr(self, p):
        self.rpn += p.NUMBER + " "
        return int(p.NUMBER) % MAX_NUM
    
    # POWER ->
    
    @_('pow_expr PLUS pow_expr')
    def pow_expr(self, p):
        self.rpn += "+ "
        return (p.pow_expr0 % (MAX_NUM - 1) + p.pow_expr1 % (MAX_NUM - 1)) % (MAX_NUM - 1)


    @_('pow_expr MINUS pow_expr')
    def pow_expr(self, p):
        self.rpn += "- "
        return ((p.pow_expr0 % MAX_NUM - 1) - (p.pow_expr1 % MAX_NUM - 1)) % (MAX_NUM - 1)


    @_('pow_expr TIMES pow_expr')
    def pow_expr(self, p):
        self.rpn += "* "
        return ((p.pow_expr0 % MAX_NUM - 1) * (p.pow_expr1 % MAX_NUM - 1)) % (MAX_NUM - 1)


    @_('pow_expr DIVIDE pow_expr')
    def pow_expr(self, p):
        self.rpn += "/ "
        if(math.gcd(p.pow_expr1, MAX_NUM - 1) != 1):
            print("Error: ", p.pow_expr1, "nie jest odwracalne modulo ", MAX_NUM)
            # raise SystemExit("Exit")
        return divide(p.pow_expr0 % (MAX_NUM - 1), p.pow_expr1 % (MAX_NUM - 1), MAX_NUM - 1) % (MAX_NUM - 1)
    
    
    @_('MINUS pow_expr %prec UMINUS')
    def pow_expr(self, p):
        self.rpn += "- "
        return MAX_NUM - 1 - p.pow_expr
    
    
    @_('NUMBER')
    def pow_expr(self, p):
        self.rpn += p.NUMBER + " "
        return int(p.NUMBER) % (MAX_NUM - 1) 
    
    
    @_('LPAREN pow_expr RPAREN')
    def pow_expr(self, p):
        self.rpn += "^ "
        return p.pow_expr


    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr
    
    
    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        self.rpn += "(-)"
        return MAX_NUM - p.expr


if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()

    while True:
        try:
            text = input(">")
            parser.rpn = ""
            result = parser.parse(lexer.tokenize(text))
            if(parser.error_flag == 0):
                print(parser.rpn)
                print("=", result)
            parser.error_flag = 0
        except EOFError:
            break