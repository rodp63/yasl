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

  ```
  $ yasl scan <FILE>
  ```

## Examples

``` bash
$ yasl scan samples/ok.yasl -o
...
<Tag.STORE,store>
<Tag.ID,data>
<Tag.AS,as>
<Tag.STR,my_data.txt>
<Tag.SEMICOLON,;>
Ok! Scan completed
```

```bash
$ yasl scan samples/bad.yasl
...
File samples/bad.yasl, line 18, SyntaxError: Invalid use of the escape character.
  word == "\e\r\r\o\r";
           ^

File samples/bad.yasl, line 23, SyntaxError: Unterminated *{ comment.
  store *{ comment! with no ending :(;
                                      ^
```
