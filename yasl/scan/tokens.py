from enum import Enum, auto


class Reserved:
    """Language Reserved Lexemes."""

    ASSIGN = "="
    RSV_ASSIGN = ":"
    SUM = "+"
    DIFF = "-"
    MULT = "*"
    DIV = "/"
    MOD = "%"
    EXP = "^"
    GT = ">"
    GE = ">="
    LT = "<"
    LE = "<="
    EQ = "=="
    NE = "!="
    POS = "$"
    OPEN_BRACE = "{"
    CLOSE_BRACE = "}"
    OPEN_BRACKET = "["
    CLOSE_BRACKET = "]"
    OPEN_PAREN = "("
    CLOSE_PAREN = ")"
    COMMA = ","
    SEMICOLON = ";"
    CRAWL = "crawl"
    LENGTH = "length"
    CONTAINS = "contains"
    IN = "in"
    STORE = "store"
    LOAD = "load"
    CUT = "cut"
    AND = "and"
    OR = "or"
    NOT = "not"
    DROP = "drop"
    SAVE = "save"
    FROM = "from"
    TO = "to"
    AS = "as"
    REGEX = "regex"
    CSS_SELECTOR = "css_selector"
    XPATH_SELECTOR = "xpath_selector"
    WHERE = "where"
    WHILE = "while"
    WHEN = "when"
    DO = "do"
    EOL_COMMENT = "#"
    OPEN_COMMENT = "*{"
    CLOSE_COMMENT = "}*"
    QUOTE = '"'
    ESCAPE = "\\"


class Tag(Enum):
    """Language Token's Tags."""

    ASSIGN = auto()
    RSV_ASSIGN = auto()
    SUM = auto()
    DIFF = auto()
    MULT = auto()
    DIV = auto()
    MOD = auto()
    EXP = auto()
    GT = auto()
    GE = auto()
    LT = auto()
    LE = auto()
    EQ = auto()
    NE = auto()
    POS = auto()
    OPEN_BRACE = auto()
    CLOSE_BRACE = auto()
    OPEN_BRACKET = auto()
    CLOSE_BRACKET = auto()
    OPEN_PAREN = auto()
    CLOSE_PAREN = auto()
    COMMA = auto()
    SEMICOLON = auto()
    CRAWL = auto()
    LENGTH = auto()
    CONTAINS = auto()
    IN = auto()
    STORE = auto()
    LOAD = auto()
    CUT = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    DROP = auto()
    SAVE = auto()
    FROM = auto()
    TO = auto()
    AS = auto()
    REGEX = auto()
    CSS_SELECTOR = auto()
    XPATH_SELECTOR = auto()
    WHERE = auto()
    WHILE = auto()
    WHEN = auto()
    DO = auto()
    ID = auto()
    NUM = auto()
    STR = auto()
    EOF = auto()
    WILDCARD = auto()


class Token:
    def __init__(self, tag, lexeme, line, rigth_wall):
        self.tag = tag
        self.lexeme = lexeme
        self.line = line
        self.column = rigth_wall - len(lexeme) + 1

    def __str__(self):
        return "<{},{}>".format(self.tag, self.lexeme)


class Number(Token):
    def __init__(self, lexeme, line, rigth_wall):
        super().__init__(Tag.NUM, lexeme, line, rigth_wall)
        self.value = int(lexeme)
