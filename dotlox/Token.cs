namespace dotlox
{
    public enum TokenType
    {
        // Single Char tokens
        LEFT_PAREN,
        RIGHT_PAREN,
        LEFT_BRACE,
        RIGHT_BRACE,
        COMMA,
        DOT,
        MINUS,
        PLUS,
        SEMICOLON,
        SLASH,
        STAR,

        // One OR Two Char tokens
        BANG,
        BANG_EQUAL,
        EQUAL,
        EQUAL_EQUAL,
        GREATER,
        GREATER_EQUAL,
        LESS,
        LESS_EQUAL,

        // Literals
        IDENT,
        STRING,
        NUMBER,

        // Keywords
        FALSE,
        TRUE,
        AND,
        OR,
        CLASS,
        FUN,
        IF,
        ELSE,
        FOR,
        WHILE,
        NIL,
        RETURN,
        PRINT,
        SUPER,
        THIS,
        VAR,

        EOF
    }

    public class Token
    {
        TokenType type;
        String lexeme;
        Object literal;
        int line;

        public Token(TokenType type, String lexeme, Object literal, int line)
        {
            this.type = type;
            this.lexeme = lexeme;
            this.literal = literal;
            this.line = line;
        }

        public override String ToString()
        {
            return $"{type} {lexeme} {literal}";
        }

    }


    class Keywords: Dictionary<String, TokenType> {}

}
