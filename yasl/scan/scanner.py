from yasl.scan.tokens import Token, Number, Tag


class Scanner:
    def __init__(self):
        self.reserved_words = {}
        self.compound_tokens = {}

        self.reserved_words["="] = Tag.ASSIGN
        self.reserved_words[":"] = Tag.RSV_ASSIGN
        self.reserved_words["+"] = Tag.SUM
        self.reserved_words["-"] = Tag.DIFF
        self.reserved_words["*"] = Tag.MULT
        self.reserved_words["/"] = Tag.DIV
        self.reserved_words["%"] = Tag.MOD
        self.reserved_words["^"] = Tag.EXP
        self.reserved_words[">"] = Tag.GT
        self.reserved_words[">="] = Tag.GE
        self.reserved_words["<"] = Tag.LT
        self.reserved_words["<="] = Tag.LE
        self.reserved_words["=="] = Tag.EQ
        self.reserved_words["!="] = Tag.NE
        self.reserved_words["$"] = Tag.POS
        self.reserved_words["{"] = Tag.OPEN_BRACE
        self.reserved_words["}"] = Tag.CLOSE_BRACE
        self.reserved_words["["] = Tag.OPEN_BRACKET
        self.reserved_words["]"] = Tag.CLOSE_BRACKET
        self.reserved_words["("] = Tag.OPEN_PAREN
        self.reserved_words[")"] = Tag.CLOSE_PAREN
        self.reserved_words[","] = Tag.COMMA
        self.reserved_words[";"] = Tag.SEMICOLON
        self.reserved_words["\""] = Tag.QUOTE
        self.reserved_words["crawl"] = Tag.CRAWL
        self.reserved_words["length"] = Tag.LENGTH
        self.reserved_words["contains"] = Tag.CONTAINS
        self.reserved_words["in"] = Tag.IN
        self.reserved_words["store"] = Tag.STORE
        self.reserved_words["load"] = Tag.LOAD
        self.reserved_words["cut"] = Tag.CUT
        self.reserved_words["and"] = Tag.AND
        self.reserved_words["or"] = Tag.OR
        self.reserved_words["not"] = Tag.NOT
        self.reserved_words["drop"] = Tag.DROP
        self.reserved_words["save"] = Tag.SAVE
        self.reserved_words["from"] = Tag.FROM
        self.reserved_words["to"] = Tag.TO
        self.reserved_words["pattern"] = Tag.PATTERN
        self.reserved_words["selector"] = Tag.SELECTOR
        self.reserved_words["as"] = Tag.AS
        self.reserved_words["where"] = Tag.WHERE
        self.reserved_words["while"] = Tag.WHILE
        self.reserved_words["when"] = Tag.WHEN
        self.reserved_words["#"] = Tag.EOL_COMMENT
        self.reserved_words["*{"] = Tag.OPEN_COMMENT
        self.reserved_words["}*"] = Tag.CLOSE_COMMENT

        self.compound_tokens["<"] = "="
        self.compound_tokens[">"] = "="
        self.compound_tokens["="] = "="
        self.compound_tokens["!"] = "="
        self.compound_tokens["*"] = "{"
        self.compound_tokens["}"] = "*"
    
    def open_file(self, filename):
        self.body = open(filename, "r")

    def get_char(self):
        self.current = self.body.read(1)
        return self.current

    def peek_char(self):
        prev = self.body.tell()
        next_char = self.body.read(1)
        self.body.seek(prev)

        return next_char

    def get_str(self):
        lexeme = ""
        while self.current and self.current != "\"":
            if self.current == "\\":
                if self.peek_char() == "\"" or self.peek_char() == "\\":
                    self.get_char()
                else:
                    raise Exception
            lexeme += self.current
            self.get_char()

        return Token(Tag.STR, lexeme)

    def skip_whitespaces(self):
        while(self.current.isspace()):
            self.get_char()

    def skip_comment(self):
        while(True):
            self.get_char()
            if self.current and self.current == "}" and self.peek_char() == "*":
                self.get_char()
                return

    def skip_eol_comment(self):
        while(self.current != "\n"):
            self.get_char()

    def get_token(self):
        self.skip_whitespaces()

        if not self.current: return

        lexeme = self.current

        if lexeme in self.compound_tokens:
            if self.peek_char() == self.compound_tokens[lexeme]:
                self.get_char()
                lexeme += self.current

                if lexeme == "*{":
                    self.skip_comment()
                    return

                return Token(self.reserved_words[lexeme], lexeme)

        if lexeme in self.reserved_words:
            if lexeme == "\"":
                self.get_char()
                return self.get_str()

            if lexeme == "#":
                self.skip_eol_comment()
                return

            return Token(self.reserved_words[lexeme], lexeme)
        
        if lexeme.isnumeric():
            while self.peek_char().isnumeric():
                self.get_char()
                lexeme += self.current

            return Number(lexeme)

        if lexeme.isalpha():
            while self.peek_char().isalnum() or self.peek_char() == "_":
                self.get_char()
                lexeme += self.current

            if lexeme in self.reserved_words:
                return Token(self.reserved_words[lexeme], lexeme)

            return Token(Tag.ID, lexeme)
    
    def get_tokens(self):
        tokens = []

        while self.get_char():
            token = self.get_token()
            if token:
                tokens.append(token)
        
        return tokens
