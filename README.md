# YASL

YASL (acronym of Yet Another Scraping Language) is a domain-specific language for web scraping.

## Installation
It is highly recommended to use a virtual environment.

```bash
$ virtualenv env
$ source env/bin/activate
```

Then, install the YASL command line interface.

```bash
$ python setup.py install
```

Verify that _yasl_ was installed successfully.

```bash
$ yasl
Usage: yasl [OPTIONS] COMMAND [ARGS]...

Options:
  --version   Show the version and exit.
  -h, --help  Show this message and exit.

Commands:
  parse  Parse a YASL file
  scan   Scan a YASL file
```

## Usage

- Scan a `.yasl` file:

  ```bash
  $ yasl scan -h
  Usage: yasl scan [OPTIONS] FILENAME

	Get the file tokens

	FILENAME is the file to scan.

  Options:
    -o, --output  Print the output of the scanner
    -h, --help    Show this message and exit.
  ```
  
- Parse a `.yasl` file:
  
  ```bash
  $ yasl parse -h
  Usage: yasl parse [OPTIONS] FILENAME

	Parse a YASL file

	FILENAME is the file to parse.

  Options:
    -o, --output  Print the output of the parser
    -i, --image   Save the parse tree in PNG format
    -h, --help    Show this message and exit.
  ```

## Examples

### Scanning

``` bash
$ yasl scan -o samples/ok.yasl
...
<Tag.STORE,store>
<Tag.ID,data>
<Tag.AS,as>
<Tag.STR,my_data.txt>
<Tag.SEMICOLON,;>
Ok! Scan completed
```

```bash
$ yasl scan samples/bad_scan.yasl
...
File samples/bad_scan.yasl, line 18, LexicalError: Invalid use of the escape character.
  word == "\e\r\r\o\r";
           ^

File samples/bad_scan.yasl, line 23, LexicalError: Unterminated *{ comment.
  store *{ comment! with no ending :(;
                                      ^
```

### Parsing

```bash
$ yasl parse -o -i samples/ok.yasl # Check the file 'ok_parse_tree.png'
...
    └── STMT[4]
        └── ASSIGN[5]
            ├── EXP[6]
            │   ├── EXP_P[9]
            │   │   └── epsilon[13]
            │   └── OBJ[10]
            │       └── VALUE[11]
            │           └── str[12]
            ├── assign[7]
            └── id[8]
Ok! Parsing completed
```

```bash
$ yasl parse samples/bad_parse.yasl
...
File samples/bad_parse.yasl, line 16, SyntaxError: Unexpected character: '('
  (drop word in data when {
  ^

File samples/bad_parse.yasl, line 18, SyntaxError: Expected character: ')'
  length word < (12 * max_size;
                              ^
...
```
