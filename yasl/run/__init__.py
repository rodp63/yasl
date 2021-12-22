import click

from anytree import RenderTree
from yasl.parse import parse_file


def s_fun(node, tokens):
    return stmt_list_fun(node.children[0], tokens)


def stmt_list_fun(node, tokens):
    if len(node.children) == 1:
        return ""

    code = stmt_fun(node.children[2], tokens)
    tokens.pop(0)
    code += stmt_list_fun(node.children[0], tokens)
    return code


def stmt_fun(node, tokens):
    name = node.name[: node.name.find("[")]

    if node.children[0].name.startswith("ASSIGN"):
        return assign_fun(node.children[0], tokens)

    if node.children[0].name.startswith("CRAWL"):
        return crawl_fun(node.children[0], tokens)

    return ""


def assign_fun(node, tokens):
    id_token = tokens.pop(0)
    code = id_token.lexeme + " = "
    tokens.pop(0)
    code += exp_fun(node.children[0], tokens) + "\n"
    return code


def exp_fun(node, tokens):
    if len(node.children) == 1:
        return length_fun(node.children[0], tokens)

    left = obj_fun(node.children[1], tokens)
    right = exp_p_fun(node.children[0], tokens)
    
    if right.startswith(" contains "):
        left, right = right, left
        left = left[10:]
        right = " in " + right

    return left + right


def exp_p_fun(node, tokens):
    if len(node.children) == 1:
        return ""

    return (
        b_op_fun(node.children[2], tokens)
        + obj_fun(node.children[1], tokens)
        + exp_p_fun(node.children[0], tokens)
    )


def length_fun(node, tokens):
    code = "len({})"
    tokens.pop(0)
    return code.format(obj_fun(node.children[0], tokens))


def obj_fun(node, tokens):
    if node.children[0].name.startswith("VALUE"):
        return value_fun(node.children[0], tokens)

    if node.children[0].name.startswith("LIST"):
        return list_fun(node.children[0], tokens)

    code = "("
    tokens.pop(0)
    code += exp_fun(node.children[1], tokens)
    code += ")"
    tokens.pop(0)
    return code


def b_op_fun(node, tokens):
    node = node.children[0]
    name = node.name[: node.name.find("[")]
    b_op = {
        "sum": "+",
        "diff": "-",
        "mult": "*",
        "div": "/",
        "mod": "%",
        "exp": "**",
        "in": "in",
        "contains": "contains",
    }
    tokens.pop(0)
    return " {} ".format(b_op[name])


def list_fun(node, tokens):
    tokens.pop(0)
    return "[" + list_p_fun(node.children[0], tokens)


def list_p_fun(node, tokens):
    if len(node.children) == 1:
        tokens.pop(0)
        return "]"

    code = value_fun(node.children[2], tokens) + ","
    tokens.pop(0)
    code += list_p_fun(node.children[0], tokens)
    return code


def value_fun(node, tokens):
    code = ""
    current_value = tokens.pop(0)
    if node.children[0].name.startswith("str"):
        code += '"'

    code += current_value.lexeme
    if node.children[0].name.startswith("str"):
        code += '"'

    return code


def crawl_fun(node, tokens):
    tokens.pop(0)
    url_list = tokens.pop(0)
    tokens.pop(0)
    results = tokens.pop(0)
    # conditions = where_fun(node.children[0], tokens)

    spider_name = "spider_{}".format(str(hash(url_list.lexeme))[1:9])
    code = (
        "import scrapy\n"
        "from scrapy.crawler import CrawlerProcess\n"
        "{2} = []\n"
        "class {0}(scrapy.Spider):\n"
        "\tname = 'spider_{0}'\n"
        "\tstart_urls = {1}\n"
        "\tdef parse(self, response):\n"
        "\t\tfor item in response.css('span::text'):\n"
        "\t\t\t{2}.append({{'url':response.url, 'text': item.get()}})\n"
    ).format(spider_name, url_list.lexeme, results.lexeme)

    code += (
        "process = CrawlerProcess(settings={{'LOG_ENABLED': False}})\n"
        "process.crawl({})\n"
        "process.start()\n"
    ).format(spider_name)

    code += "print({})".format(results.lexeme)
    return code


# TODO: Terminar reglas gramaticales
def where_fun(node, tokens):
    pass


@click.command(short_help="Execute a YASL file")
@click.argument("filename", type=click.Path(exists=True))
def yasl_command(filename):
    """Execute a YASL file

    FILENAME is the file to parse.
    """

    result = parse_file(filename, output=False, image=False)

    if not result:
        return

    result = s_fun(result[0], result[1])
    print(result)
