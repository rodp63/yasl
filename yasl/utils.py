import os
import click

from collections import OrderedDict
from yasl.scan.tokens import Tag, Reserved


tag_to_symbol_dict = {
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
    Tag.EOF: "$",
}

symbol_to_lexeme_dict = {
    "assign": Reserved.ASSIGN,
    "rsv_assign": Reserved.RSV_ASSIGN,
    "sum": Reserved.SUM,
    "diff": Reserved.DIFF,
    "mult": Reserved.MULT,
    "div": Reserved.DIV,
    "mod": Reserved.MOD,
    "exp": Reserved.EXP,
    "gt": Reserved.GT,
    "ge": Reserved.GE,
    "lt": Reserved.LT,
    "le": Reserved.LE,
    "eq": Reserved.EQ,
    "ne": Reserved.NE,
    "pos": Reserved.POS,
    "open_brace": Reserved.OPEN_BRACE,
    "close_brace": Reserved.CLOSE_BRACE,
    "open_bracket": Reserved.OPEN_BRACKET,
    "close_bracket": Reserved.CLOSE_BRACKET,
    "open_paren": Reserved.OPEN_PAREN,
    "close_paren": Reserved.CLOSE_PAREN,
    "comma": Reserved.COMMA,
    "semicolon": Reserved.SEMICOLON,
    "crawl": Reserved.CRAWL,
    "length": Reserved.LENGTH,
    "contains": Reserved.CONTAINS,
    "in": Reserved.IN,
    "store": Reserved.STORE,
    "load": Reserved.LOAD,
    "cut": Reserved.CUT,
    "and": Reserved.AND,
    "or": Reserved.OR,
    "not": Reserved.NOT,
    "drop": Reserved.DROP,
    "save": Reserved.SAVE,
    "from": Reserved.FROM,
    "to": Reserved.TO,
    "as": Reserved.AS,
    "regex": Reserved.REGEX,
    "css_selector": Reserved.CSS_SELECTOR,
    "xpath_selector": Reserved.XPATH_SELECTOR,
    "where": Reserved.WHERE,
    "while": Reserved.WHILE,
    "when": Reserved.WHEN,
    "do": Reserved.DO,
}

lexeme_to_tag_dict = {
    Reserved.ASSIGN: Tag.ASSIGN,
    Reserved.RSV_ASSIGN: Tag.RSV_ASSIGN,
    Reserved.SUM: Tag.SUM,
    Reserved.DIFF: Tag.DIFF,
    Reserved.MULT: Tag.MULT,
    Reserved.DIV: Tag.DIV,
    Reserved.MOD: Tag.MOD,
    Reserved.EXP: Tag.EXP,
    Reserved.GT: Tag.GT,
    Reserved.GE: Tag.GE,
    Reserved.LT: Tag.LT,
    Reserved.LE: Tag.LE,
    Reserved.EQ: Tag.EQ,
    Reserved.NE: Tag.NE,
    Reserved.POS: Tag.POS,
    Reserved.OPEN_BRACE: Tag.OPEN_BRACE,
    Reserved.CLOSE_BRACE: Tag.CLOSE_BRACE,
    Reserved.OPEN_BRACKET: Tag.OPEN_BRACKET,
    Reserved.CLOSE_BRACKET: Tag.CLOSE_BRACKET,
    Reserved.OPEN_PAREN: Tag.OPEN_PAREN,
    Reserved.CLOSE_PAREN: Tag.CLOSE_PAREN,
    Reserved.COMMA: Tag.COMMA,
    Reserved.SEMICOLON: Tag.SEMICOLON,
    Reserved.CRAWL: Tag.CRAWL,
    Reserved.LENGTH: Tag.LENGTH,
    Reserved.CONTAINS: Tag.CONTAINS,
    Reserved.IN: Tag.IN,
    Reserved.STORE: Tag.STORE,
    Reserved.LOAD: Tag.LOAD,
    Reserved.CUT: Tag.CUT,
    Reserved.AND: Tag.AND,
    Reserved.OR: Tag.OR,
    Reserved.NOT: Tag.NOT,
    Reserved.DROP: Tag.DROP,
    Reserved.SAVE: Tag.SAVE,
    Reserved.FROM: Tag.FROM,
    Reserved.TO: Tag.TO,
    Reserved.AS: Tag.AS,
    Reserved.REGEX: Tag.REGEX,
    Reserved.CSS_SELECTOR: Tag.CSS_SELECTOR,
    Reserved.XPATH_SELECTOR: Tag.XPATH_SELECTOR,
    Reserved.WHERE: Tag.WHERE,
    Reserved.WHILE: Tag.WHILE,
    Reserved.WHEN: Tag.WHEN,
    Reserved.DO: Tag.DO,
}


def tag_to_symbol(tag):
    return tag_to_symbol_dict.get(tag, None)


def symbol_to_lexeme(symbol):
    return symbol_to_lexeme_dict.get(symbol, symbol)


def lexeme_to_tag(lexeme):
    return lexeme_to_tag_dict.get(lexeme, None)


def path_of_tree_file(filename):
    filename = os.path.basename(filename).split(".")[0]
    filename = filename + "_parse_tree.png"
    return os.path.join(os.path.abspath("."), filename)


def strip_code(code):
    counter = 0
    for c in code:
        if c.isspace():
            counter += 1
        else:
            break
    return "  " + code.strip(), counter - 1


def echo_error(error, filename, error_type, ending="\n"):
    line = "File {}, line {}, ".format(
        click.format_filename(filename), error["line_number"]
    )
    code, count = strip_code(error["line"])
    pointer = " " * (error["pointer"] - count) + "^"
    click.secho(line, bold=True, nl=False, err=True)
    click.secho("{}: ".format(error_type), nl=False, fg="red", bold=True, err=True)
    click.secho(error["message"], bold=True, err=True)
    click.echo("{}\n{}{}".format(code, pointer, ending), err=True)
