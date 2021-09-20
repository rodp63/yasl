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
    REGEX = "regex"
    CSS_SELECTOR = "css_selector"
    XPATH_SELECTOR = "xpath_selector"
    AS = "as"
    WHERE = "where"
    WHILE = "while"
    WHEN = "when"
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
    REGEX = auto()
    CSS_SELECTOR = auto()
    XPATH_SELECTOR = auto()
    AS = auto()
    WHERE = auto()
    WHILE = auto()
    WHEN = auto()
    ID = auto()
    NUM = auto()
    STR = auto()


class Token:
    def __init__(self, tag: Tag, lexeme: str):
        self.tag = tag
        self.lexeme = lexeme

    def __str__(self):
        return "<{},{}>".format(self.tag, self.lexeme)


class Number(Token):
    def __init__(self, lexeme):
        super().__init__(Tag.NUM, lexeme)
        self.value = int(lexeme)
