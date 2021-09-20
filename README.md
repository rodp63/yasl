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

## Usage

- Scan a `.yasl` file:

  ```
  $ yasl scan <FILE>
  ```

## Examples

``` bash
$ yasl scan samples/ok.yasl
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
