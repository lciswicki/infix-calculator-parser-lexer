from sly import Lexer

class CalcLexer(Lexer):
    tokens = { NUMBER, PLUS, MINUS, TIMES,
               DIVIDE, LPAREN, RPAREN, POW}

    ignore = ' \t'
    ignore_comment = r'\#.*'

    NUMBER  = r'[1-9][0-9]*|0'
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    LPAREN  = r'\('
    RPAREN  = r'\)'
    POW     = r'\^'


if __name__ == '__main__':
    data = '01 + 22324 + 2^'
    lexer = CalcLexer()
    for tok in lexer.tokenize(data):
        print('type=%r, value=%r' % (tok.type, tok.value))