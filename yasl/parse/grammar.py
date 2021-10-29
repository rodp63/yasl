yasl_grammar = """
S -> STMT_LIST
STMT_LIST -> STMT semicolon STMT_LIST | epsilon
STMT -> ASSIGN | CRAWL | WHILE | WHEN_DO | DROP | SAVE | STORE | LOAD | CUT
ASSIGN -> id assign EXP
EXP -> OBJ EXP_P | LENGTH
EXP_P -> B_OP OBJ EXP_P | epsilon
LENGTH -> length OBJ
OBJ -> VALUE | LIST | open_paren EXP close_paren
B_OP -> sum | diff | mult | div | mod | exp | pos | contains | in
LIST -> open_bracket LIST_P
LIST_P -> close_bracket | VALUE comma LIST_P
VALUE -> num | str | id
CRAWL -> crawl id to id WHERE
WHERE -> epsilon | where open_brace WHERE_P
WHERE_P -> close_brace | RSV_ASSIGN WHERE_P
RSV_ASSIGN -> RSV_WORD rsv_assign EXP semicolon
RSV_WORD -> regex | css_selector | xpath_selector
WHILE -> while CONDITION do DO
CONDITION -> open_brace CMP semicolon CONDITION_P
CONDITION_P -> close_brace | CMP semicolon CONDITION_P
CMP -> EXP CMP_P | LOGIC
CMP_P -> C_OP EXP | epsilon
LOGIC -> and CONDITION | or CONDITION | not S_CONDITION
S_CONDITION -> open_brace CMP semicolon close_brace
C_OP ->  gt | ge | lt | le | eq | ne
DO -> open_brace STMT_LIST close_brace
WHEN_DO -> when CONDITION do DO
DROP -> drop id in ITER WHEN
ITER -> id | str | LIST
WHEN -> when CONDITION
SAVE -> save id in ITER WHEN
STORE -> store id as str
LOAD -> load str as id
CUT -> cut ITER from num to num
"""
