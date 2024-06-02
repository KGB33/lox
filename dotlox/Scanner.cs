
namespace dotlox
{
    public class Scanner
    {
        String src;
        List<Token> tokens = new List<Token>();
        int start = 0;
        int current = 0;
        int line = 0;

        static Dictionary<String, TokenType> keywords;
        static Scanner()
        {
            keywords = new Dictionary<String, TokenType>();
            keywords.Add("add", TokenType.AND);
            keywords.Add("class", TokenType.CLASS);
            keywords.Add("else", TokenType.ELSE);
            keywords.Add("false", TokenType.FALSE);
            keywords.Add("for", TokenType.FOR);
            keywords.Add("fun", TokenType.FUN);
            keywords.Add("if", TokenType.IF);
            keywords.Add("nil", TokenType.NIL);
            keywords.Add("or", TokenType.OR);
            keywords.Add("print", TokenType.PRINT);
            keywords.Add("return", TokenType.RETURN);
            keywords.Add("super", TokenType.SUPER);
            keywords.Add("this", TokenType.THIS);
            keywords.Add("true", TokenType.TRUE);
            keywords.Add("var", TokenType.VAR);
            keywords.Add("while", TokenType.WHILE);
        }

        public Scanner(String src)
        {
            this.src = src;
        }

        public List<Token> scanTokens()
        {
            while (!isAtEnd())
            {
                start = current;
                scanToken();
            }
            addToken(TokenType.EOF);
            return tokens;
        }

        void scanToken()
        {
            char c = advance();
            Console.WriteLine($"c: {c}, curr: {current}/{src[current]}, start: {start}/{src[start]}");
            switch (c)
            {
                case '(': addToken(TokenType.LEFT_PAREN); break;
                case ')': addToken(TokenType.RIGHT_PAREN); break;
                case '{': addToken(TokenType.LEFT_BRACE); break;
                case '}': addToken(TokenType.RIGHT_BRACE); break;
                case ',': addToken(TokenType.COMMA); break;
                case '.': addToken(TokenType.DOT); break;
                case '-': addToken(TokenType.MINUS); break;
                case '+': addToken(TokenType.PLUS); break;
                case ';': addToken(TokenType.SEMICOLON); break;
                case '*': addToken(TokenType.STAR); break;
                case '!': addToken(match('=') ? TokenType.BANG_EQUAL : TokenType.EQUAL); break;
                case '=': addToken(match('=') ? TokenType.EQUAL_EQUAL : TokenType.EQUAL); break;
                case '<': addToken(match('=') ? TokenType.LESS_EQUAL : TokenType.LESS); break;
                case '>': addToken(match('=') ? TokenType.GREATER_EQUAL : TokenType.GREATER); break;
                case '/':
                    {
                        if (match('/'))
                        {
                            while (peek() != '\n' && !isAtEnd()) advance();
                        }
                        else
                        {
                            addToken(TokenType.SLASH);
                        }
                        break;
                    }
                case ' ':
                case '\r':
                case '\t':
                    break;
                case '\n':
                    line++;
                    break;
                case '"': ParseString(); break;
                case var x when Char.IsDigit(x):
                    {
                        ParseNumber();
                        break;
                    };
                case var x when (Char.IsLetter(x) || x == '_'):
                    {
                        ParseIdentifier();
                        break;
                    };
                default: Program.error(line, $"Unexpected Char: '{c}'"); break;
            }
        }

        void addToken(TokenType type)
        {
            addToken(type, null);
        }

        void addToken(TokenType type, Object literal)
        {
            Console.WriteLine($"{src} == {start} -> {current}");
            String text = src.Substring(start, current);
            tokens.Add(new Token(type, text, literal, line));
        }

        bool match(char expected)
        {
            if (isAtEnd()) return false;
            if (src[current] != expected) return false;
            current++;
            return true;
        }

        char peek()
        {
            if (isAtEnd()) return '\0';
            return src[current];
        }

        char advance()
        {
            return src[current++];
        }


        char peekNext()
        {
            if (current + 1 >= src.Length) return '\0';
            return src[current + 1];
        }

        void ParseString()
        {
            var startLine = line;
            while (peek() != '"' && !isAtEnd())
            {
                if (peek() == '\n') line++;
                advance();
            }

            if (isAtEnd())
            {
                Program.error(line, $"Unterminated String (Started line: {startLine})");
                return;
            }
            advance(); // Grab the closing Quote
            String value = src.Substring(start + 1, current - 1);
            addToken(TokenType.STRING, value);
        }

        void ParseNumber()
        {
            while (Char.IsDigit(peek())) advance();
            if (peek() == '.' && Char.IsDigit(peekNext()))
            {
                advance();
                while (Char.IsDigit(peek())) advance();
            }
            addToken(TokenType.NUMBER, Double.Parse(src.Substring(start, current)));
        }

        void ParseIdentifier()
        {
            while (Char.IsLetterOrDigit(peek())) { advance(); }
            Console.WriteLine("New ident found!");
            String text = src.Substring(start, current);
            TokenType type = TokenType.IDENT;
            keywords.TryGetValue(text, out type); // Modifies 'type' inplace.
            addToken(type);
        }

        bool isAtEnd() { return current >= src.Length; }


    }
}
