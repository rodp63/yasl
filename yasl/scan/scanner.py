from yasl.scan.tokens import Reserved, Tag, Token, Number


class Scanner:
    def __init__(self):
        self.line = 1
        self.previous_line = ""
        self.current_line = ""
        self.hash_table = {}
        self.compound_tokens = {}

        self.hash_table[Reserved.ASSIGN] = Tag.ASSIGN
        self.hash_table[Reserved.RSV_ASSIGN] = Tag.RSV_ASSIGN
        self.hash_table[Reserved.SUM] = Tag.SUM
        self.hash_table[Reserved.DIFF] = Tag.DIFF
        self.hash_table[Reserved.MULT] = Tag.MULT
        self.hash_table[Reserved.DIV] = Tag.DIV
        self.hash_table[Reserved.MOD] = Tag.MOD
        self.hash_table[Reserved.EXP] = Tag.EXP
        self.hash_table[Reserved.GT] = Tag.GT
        self.hash_table[Reserved.GE] = Tag.GE
        self.hash_table[Reserved.LT] = Tag.LT
        self.hash_table[Reserved.LE] = Tag.LE
        self.hash_table[Reserved.EQ] = Tag.EQ
        self.hash_table[Reserved.NE] = Tag.NE
        self.hash_table[Reserved.POS] = Tag.POS
        self.hash_table[Reserved.OPEN_BRACE] = Tag.OPEN_BRACE
        self.hash_table[Reserved.CLOSE_BRACE] = Tag.CLOSE_BRACE
        self.hash_table[Reserved.OPEN_BRACKET] = Tag.OPEN_BRACKET
        self.hash_table[Reserved.CLOSE_BRACKET] = Tag.CLOSE_BRACKET
        self.hash_table[Reserved.OPEN_PAREN] = Tag.OPEN_PAREN
        self.hash_table[Reserved.CLOSE_PAREN] = Tag.CLOSE_PAREN
        self.hash_table[Reserved.COMMA] = Tag.COMMA
        self.hash_table[Reserved.SEMICOLON] = Tag.SEMICOLON
        self.hash_table[Reserved.CRAWL] = Tag.CRAWL
        self.hash_table[Reserved.LENGTH] = Tag.LENGTH
        self.hash_table[Reserved.CONTAINS] = Tag.CONTAINS
        self.hash_table[Reserved.IN] = Tag.IN
        self.hash_table[Reserved.STORE] = Tag.STORE
        self.hash_table[Reserved.LOAD] = Tag.LOAD
        self.hash_table[Reserved.CUT] = Tag.CUT
        self.hash_table[Reserved.AND] = Tag.AND
        self.hash_table[Reserved.OR] = Tag.OR
        self.hash_table[Reserved.NOT] = Tag.NOT
        self.hash_table[Reserved.DROP] = Tag.DROP
        self.hash_table[Reserved.SAVE] = Tag.SAVE
        self.hash_table[Reserved.FROM] = Tag.FROM
        self.hash_table[Reserved.TO] = Tag.TO
        self.hash_table[Reserved.AS] = Tag.AS
        self.hash_table[Reserved.REGEX] = Tag.REGEX
        self.hash_table[Reserved.CSS_SELECTOR] = Tag.CSS_SELECTOR
        self.hash_table[Reserved.XPATH_SELECTOR] = Tag.XPATH_SELECTOR
        self.hash_table[Reserved.WHERE] = Tag.WHERE
        self.hash_table[Reserved.WHILE] = Tag.WHILE
        self.hash_table[Reserved.WHEN] = Tag.WHEN
        self.hash_table[Reserved.DO] = Tag.DO

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
        self.current_line += self.current
        return self.current

    def peek_char(self):
        prev = self.body.tell()
        next_char = self.body.read(1)
        self.body.seek(prev)

        return next_char

    def get_str(self):
        lexeme = ""
        special_escaped = {"n": "\n", "t": "\t"}
        while self.current and self.current != Reserved.QUOTE:
            take = True
            if self.current == Reserved.ESCAPE:
                if (
                    self.peek_char() == Reserved.QUOTE
                    or self.peek_char() == Reserved.ESCAPE
                ):
                    self.get_char()
                elif self.peek_char() in special_escaped:
                    self.get_char()
                    lexeme += special_escaped[self.current]
                    take = False
                else:
                    raise SyntaxError("Invalid use of the escape character.")

            if self.current == "\n":
                raise SyntaxError("EOL while scanning string literal.")

            if take:
                lexeme += self.current
            self.get_char()

        if not self.current:
            raise SyntaxError("EOF while scanning string literal.")

        return Token(Tag.STR, lexeme)

    def reset_line(self):
        self.line += 1
        self.previous_line = self.current_line

        if self.current_line[-1] == "\n":
            self.previous_line = self.previous_line[:-1]

        self.current_line = ""

    def go_to_next_line(self):
        while self.current and self.current != "\n":
            self.get_char()

        self.reset_line()

    def skip_whitespaces(self):
        while self.current.isspace():
            if self.current == "\n":
                self.reset_line()

            self.get_char()

    def skip_comment(self):
        while True:
            self.get_char()
            if not self.current:
                raise SyntaxError(
                    "Unterminated {} comment.".format(Reserved.OPEN_COMMENT)
                )
            if (
                self.current == Reserved.CLOSE_COMMENT[0]
                and self.peek_char() == Reserved.CLOSE_COMMENT[1]
            ):
                self.get_char()
                return

    def get_token(self):
        self.skip_whitespaces()

        if not self.current:
            return

        lexeme = self.current

        if lexeme in self.compound_tokens:
            if self.peek_char() == self.compound_tokens[lexeme]:
                self.get_char()
                lexeme += self.current

                if lexeme == Reserved.OPEN_COMMENT:
                    self.skip_comment()
                    return

                return Token(self.hash_table[lexeme], lexeme)

        if lexeme == Reserved.QUOTE:
            self.get_char()
            return self.get_str()

        if lexeme == Reserved.EOL_COMMENT:
            self.go_to_next_line()
            return

        if lexeme in self.hash_table:
            return Token(self.hash_table[lexeme], lexeme)

        if lexeme.isnumeric():
            flag = lexeme == "0"

            while self.peek_char().isnumeric():
                if flag and self.current != "0":
                    raise SyntaxError(
                        "Leading zeros in integer literals are not permitted."
                    )

                self.get_char()
                lexeme += self.current

            return Number(lexeme)

        if lexeme.isalpha():
            while self.peek_char().isalnum() or self.peek_char() == "_":
                self.get_char()
                lexeme += self.current

            if lexeme in self.hash_table:
                return Token(self.hash_table[lexeme], lexeme)

            return Token(Tag.ID, lexeme)

        raise SyntaxError("Unkown character.")

    def get_tokens(self):
        tokens = []
        errors = []

        while self.get_char():
            try:
                token = self.get_token()
                if token:
                    tokens.append(token)
            except Exception as ex:
                character = len(self.current_line)
                self.go_to_next_line()
                errors.append(
                    {
                        "message": str(ex),
                        "line_number": self.line - 1,
                        "line": self.previous_line,
                        "pointer": character,
                    }
                )

        return tokens, errors
