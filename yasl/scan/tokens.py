from enum import Enum, auto


class Tag(Enum):
    """Operators."""
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

    """Delimiters."""
    OPEN_BRACE = auto()
    CLOSE_BRACE = auto()
    OPEN_BRACKET = auto()
    CLOSE_BRACKET = auto()
    OPEN_PAREN = auto()
    CLOSE_PAREN = auto()
    COMMA = auto()
    SEMICOLON = auto()
    QUOTE = auto()

    """Reserved."""
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
    PATTERN = auto()
    SELECTOR = auto()
    AS = auto()
    WHERE = auto()
    WHILE = auto()
    WHEN = auto()

    """General."""
    ID = auto()
    NUM = auto()
    STR = auto()
    EOL_COMMENT = auto()
    OPEN_COMMENT = auto()
    CLOSE_COMMENT = auto()


class Token():
    def __init__(self, tag: Tag, lexeme: str):
        self.tag = tag
        self.lexeme = lexeme

    def __str__(self):
        return "<{},{}>".format(self.tag, self.lexeme)


class Number(Token):
    def __init__(self, lexeme):
        super().__init__(Tag.NUM, lexeme)
        self.value = int(lexeme)
