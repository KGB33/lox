use std::{iter::Peekable, str::Chars};

use phf::{phf_map, phf_set};

pub struct Lexer<'a> {
    input: Peekable<Chars<'a>>,
}

#[derive(Debug, PartialEq, Clone)]
pub enum LexToken {
    // Kwords
    Let,

    // Delimiters
    Colon,
    SemiColon,
    LParam,
    RParam,

    // Vars & Literals
    Ident(String),
    StrLiteral(String),
    IntLiteral(i64),
    FloatLiteral(f64),

    // Operators
    Equals,
    Plus,

    // Meta
    Error(String),
}

static KEYWORDS: phf::Map<&'static str, LexToken> = phf_map! {
    "let" => LexToken::Let,
};

static DELIMITERS: phf::Set<char> = phf_set! {
    '(', ')', ';', ':', '"',
};

impl<'a> Lexer<'a> {
    pub fn new(src: Peekable<Chars<'a>>) -> Self {
        Lexer { input: src }
    }
}

impl Iterator for Lexer<'_> {
    type Item = LexToken;
    fn next(&mut self) -> Option<LexToken> {
        match self.input.peek() {
            Some('=') => {
                self.input.next();
                Some(LexToken::Equals)
            }
            Some(';') => {
                self.input.next();
                Some(LexToken::SemiColon)
            }
            Some(':') => {
                self.input.next();
                Some(LexToken::Colon)
            }
            Some('+') => {
                self.input.next();
                Some(LexToken::Plus)
            }
            Some('(') => {
                self.input.next();
                Some(LexToken::LParam)
            }
            Some(')') => {
                self.input.next();
                Some(LexToken::RParam)
            }
            Some('"') => {
                self.input.next(); // Eat opening quote
                Some(read_string(self).unwrap_or_else(LexToken::Error))
            }
            Some(c) if c.is_alphabetic() => {
                Some(read_to_ident_or_keyword(self).unwrap_or_else(LexToken::Error))
            }
            Some(c) if c.is_whitespace() => {
                self.input.next();
                self.next()
            }
            Some(c) if c.is_numeric() => Some(read_numeric(self).unwrap_or_else(LexToken::Error)),
            _ => None,
        }
    }
}

fn is_delimiter(c: char) -> bool {
    c.is_whitespace() || DELIMITERS.contains(&c)
}

fn read_to_delimiter(lexer: &mut Lexer) -> Result<String, String> {
    let mut buf = String::new();
    while let Some(c) = lexer.input.peek() {
        if is_delimiter(*c) {
            break;
        }
        buf.push(lexer.input.next().unwrap())
    }
    if buf.is_empty() {
        return Err("Read empty identifier".to_string());
    }
    Ok(buf)
}

fn read_to_ident_or_keyword(lexer: &mut Lexer) -> Result<LexToken, String> {
    let ident = read_to_delimiter(lexer)?;

    KEYWORDS
        .get(&ident)
        .map_or_else(|| Ok(LexToken::Ident(ident)), |s| Ok(s.clone()))
}

fn read_string(lexer: &mut Lexer) -> Result<LexToken, String> {
    let mut buf = String::new();
    while let Some(c) = lexer.input.peek() {
        if *c == '"' {
            break;
        }
        buf.push(lexer.input.next().unwrap());
    }
    // Eat closing quote,
    // And check to make sure the quotes were paired.
    if lexer.input.next().is_none() {
        return Err("Read a string to EOF".into());
    }
    Ok(LexToken::StrLiteral(buf))
}

fn read_numeric(lexer: &mut Lexer) -> Result<LexToken, String> {
    let ident = read_to_delimiter(lexer)?;
    if let Ok(token) = ident.parse::<i64>() {
        return Ok(LexToken::IntLiteral(token));
    };
    if let Ok(token) = ident.parse::<f64>() {
        return Ok(LexToken::FloatLiteral(token));
    };
    Err("Could not parse '{}' to Numeric Literal.".to_string())
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn str_at_eof_parses_correctly() {
        let src = "\"Some str\"";

        let mut lexer = Lexer::new(src.chars().peekable());

        assert_eq!(Some(LexToken::StrLiteral("Some str".into())), lexer.next());
        assert_eq!(None, lexer.next());
    }

    #[test]
    fn it_works() {
        let src = "let bar: int = 10 + 15.0; let foo: fx = print(\"hello world\");";

        let mut lexer = Lexer::new(src.chars().peekable());

        // 1st Stmt
        assert_eq!(Some(LexToken::Let), lexer.next());
        assert_eq!(Some(LexToken::Ident("bar".into())), lexer.next());
        assert_eq!(Some(LexToken::Colon), lexer.next());
        assert_eq!(Some(LexToken::Ident("int".into())), lexer.next());
        assert_eq!(Some(LexToken::Equals), lexer.next());
        assert_eq!(Some(LexToken::IntLiteral(10)), lexer.next());
        assert_eq!(Some(LexToken::Plus), lexer.next());
        assert_eq!(Some(LexToken::FloatLiteral(15.0)), lexer.next());
        assert_eq!(Some(LexToken::SemiColon), lexer.next());

        // 2nd Stmt
        assert_eq!(Some(LexToken::Let), lexer.next());
        assert_eq!(Some(LexToken::Ident("foo".into())), lexer.next());
        assert_eq!(Some(LexToken::Colon), lexer.next());
        assert_eq!(Some(LexToken::Ident("fx".into())), lexer.next());
        assert_eq!(Some(LexToken::Equals), lexer.next());
        assert_eq!(Some(LexToken::Ident("print".into())), lexer.next());
        assert_eq!(Some(LexToken::LParam), lexer.next());
        assert_eq!(
            Some(LexToken::StrLiteral("hello world".into())),
            lexer.next()
        );
        assert_eq!(Some(LexToken::RParam), lexer.next());
        assert_eq!(Some(LexToken::SemiColon), lexer.next());

        // Done!
        assert_eq!(None, lexer.next());
    }
}
