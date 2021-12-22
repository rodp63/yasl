from queue import LifoQueue
from collections import OrderedDict
from anytree import Node

from yasl.scan.tokens import Tag, Token
from yasl.utils import tag_to_symbol, symbol_to_lexeme


class Stack(LifoQueue):
    def peek(self):
        if len(self.queue) == 0:
            return None
        return self.queue[len(self.queue) - 1]


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


class Parser:
    def __init__(self, grammar, epsilon, eof):
        try:
            self.productions = OrderedDict()
            self.epsilon = epsilon
            self.eof = eof

            rules = [rule.strip() for rule in grammar.strip().split("\n")]
            self.start = rules[0].split("->")[0].strip()

            for rule in rules:
                head, body = [r.strip() for r in rule.split("->")]
                productions = [p.strip() for p in body.split("|")]
                for p in productions:
                    self.add_rule(Rule(head, tuple(p.split(" "))))
        except:
            raise Exception("Invalid grammar input")

    @property
    def nonterminals(self):
        return self.productions.keys()

    @property
    def terminals(self):
        terminals = OrderedDict()
        for rules in self.productions.values():
            for rule in rules:
                for symbol in rule.body:
                    if symbol not in self.nonterminals:
                        terminals.update({symbol: 1})

        return terminals.keys()

    def add_rule(self, rule):
        try:
            if rule not in self.productions[rule.head]:
                self.productions[rule.head].append(rule)
        except KeyError:
            self.productions[rule.head] = [rule]

    def is_terminal(self, s):
        return s not in self.nonterminals

    def is_start_symbol(self, symbol):
        return self.start == symbol

    def productions_for(self, nonterm):
        return [p.body for p in self.productions[nonterm]]

    def first(self, x):
        f = set()
        if isinstance(x, tuple):
            for symbol in x:
                ft = self.first(symbol)
                f = f.union(ft)
                if self.epsilon not in ft:
                    break
        elif self.is_terminal(x):
            f = {x}
        else:
            for p in self.productions_for(x):
                f = f.union(self.first(p))

        return f

    def follow(self, nonterminal, previous=tuple()):
        previous += (nonterminal,)

        f = set()
        if self.is_start_symbol(nonterminal):
            f.add(self.eof)

        subsets = set()
        for rules in self.productions.values():
            for rule in rules:
                if nonterminal in rule.body:
                    position = rule.body.index(nonterminal)
                    a = rule.body[0:position]
                    b = rule.body[position + 1 :]
                    if b:
                        next_first = set(self.first(b))
                        f = f.union(next_first - {self.epsilon})
                        if self.epsilon in next_first:
                            subsets.add(rule.head)
                    else:
                        subsets.add(rule.head)

        for x in subsets:
            if x not in previous:
                f = f.union(self.follow(x, previous))

        return sorted(f)

    def parsing_table(self):
        table = {}
        ambigous = False
        for rules in self.productions.values():
            for rule in rules:
                terminals = self.first(rule.body)
                if self.epsilon in terminals:
                    terminals = terminals.union(self.follow(rule.head))
                for t in terminals:
                    if t == self.epsilon:
                        continue
                    if table.get((rule.head, t)):
                        ls = []
                        ls.append(table[(rule.head, t)])
                        ls.append(rule)
                        table[(rule.head, t)] = ls
                        ambigous = True
                    else:
                        table[(rule.head, t)] = rule
        return (table, ambigous)

    def format_error(self, message, token):
        return {
            "message": message,
            "line_number": token.line,
            "pointer": token.column,
        }

    def parse_tokens(self, tokens):
        table, ambigous = self.parsing_table()
        if ambigous:
            raise Exception("Ambigous grammar")

        error_list = []

        current_token = tokens.pop(0)
        word = tag_to_symbol(current_token.tag)
        root = Node("{}[0]".format(self.start))
        stack = Stack()
        order = 1

        tokens.append(Token(Tag.EOF, self.eof, -1, -1))
        stack.put((self.eof, None))
        stack.put((self.start, root))

        top_stack = stack.peek()
        while top_stack:
            if top_stack[0] == self.eof and word == self.eof:
                return root, error_list

            if self.is_terminal(top_stack[0]):
                stack.get()
                if top_stack[0] == word:
                    current_token = tokens.pop(0)
                    word = tag_to_symbol(current_token.tag)
                else:
                    error_list.append(
                        self.format_error(
                            "Expected character: '{}'".format(
                                symbol_to_lexeme(top_stack[0])
                            ),
                            current_token,
                        )
                    )
            else:
                rule = table.get((top_stack[0], word))
                if rule:
                    stack.get()
                    symbols = rule.body[::-1]
                    for symbol in symbols:
                        node = Node("{}[{}]".format(symbol, order), parent=top_stack[1])
                        order += 1
                        if symbol != self.epsilon:
                            stack.put((symbol, node))
                else:
                    terminals = self.first(top_stack[0])
                    error_list.append(
                        self.format_error(
                            "Unexpected character: '{}'".format(current_token.lexeme),
                            current_token,
                        )
                    )

                    while word not in terminals:
                        if word == self.eof:
                            return root, error_list
                        current_token = tokens.pop(0)
                        word = tag_to_symbol(current_token.tag)

            top_stack = stack.peek()
