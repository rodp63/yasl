from collections import OrderedDict
from yasl.scan.tokens import Tag


epsilon = "epsilon"
eof = "$"


tag_dictionary = {
    Tag.ASSIGN: "assign",
    Tag.RSV_ASSIGN: "rsv_assign",
    Tag.SUM: "sum",
    Tag.DIFF: "diff",
    Tag.MULT: "mult",
    Tag.DIV: "div",
    Tag.MOD: "mod",
    Tag.EXP: "exp",
    Tag.GT: "gt",
    Tag.GE: "ge",
    Tag.LT: "lt",
    Tag.LE: "le",
    Tag.EQ: "eq",
    Tag.NE: "ne",
    Tag.POS: "pos",
    Tag.OPEN_BRACE: "open_brace",
    Tag.CLOSE_BRACE: "close_brace",
    Tag.OPEN_BRACKET: "open_bracket",
    Tag.CLOSE_BRACKET: "close_bracket",
    Tag.OPEN_PAREN: "open_paren",
    Tag.CLOSE_PAREN: "close_paren",
    Tag.COMMA: "comma",
    Tag.SEMICOLON: "semicolon",
    Tag.CRAWL: "crawl",
    Tag.LENGTH: "length",
    Tag.CONTAINS: "contains",
    Tag.IN: "in",
    Tag.STORE: "store",
    Tag.LOAD: "load",
    Tag.CUT: "cut",
    Tag.AND: "and",
    Tag.OR: "or",
    Tag.NOT: "not",
    Tag.DROP: "drop",
    Tag.SAVE: "save",
    Tag.FROM: "from",
    Tag.TO: "to",
    Tag.AS: "as",
    Tag.REGEX: "regex",
    Tag.CSS_SELECTOR: "css_selector",
    Tag.XPATH_SELECTOR: "xpath_selector",
    Tag.WHERE: "where",
    Tag.WHILE: "while",
    Tag.WHEN: "when",
    Tag.DO: "do",
    Tag.ID: "id",
    Tag.NUM: "num",
    Tag.STR: "str",
    Tag.EOF: eof,
}


class Rule:
    def __init__(self, head, body):
        self.head = head
        self.body = body

    def is_left_recursive(self):
        return self.body and self.head == self.body[0]

    def __eq__(self, other):
        return self.head == other.head and self.body == other.body

    def __str__(self):
        return "{} -> {}".format(self.head, " ".join(self.body))


def tag_to_symbol(tag):
    return tag_dictionary[tag]
