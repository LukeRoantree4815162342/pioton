import re

PIOTON_MULTILINE_IDENTIFIER = "  # PIOTON-MULTI"

def _mark_multiline_strings(lines):
    """Pre-processor to mark lines that fall within multi-line string literals."""
    new_lines = []
    active_quote = None
    for line in lines:
        if active_quote:
            # Already inside a multiline block, mark it and check for the end
            tagged = line.rstrip('\n\r')
            if not tagged.endswith(PIOTON_MULTILINE_IDENTIFIER):
                tagged += PIOTON_MULTILINE_IDENTIFIER
            if line.endswith('\n'): tagged += '\n'
            new_lines.append(tagged)
            if active_quote in line:
                active_quote = None
        else:
            # Check if this line starts a multiline block
            dq_pos, sq_pos = line.find('"""'), line.find("'''")
            quote_type = None
            if dq_pos != -1 and (sq_pos == -1 or dq_pos < sq_pos): quote_type = '"""'
            elif sq_pos != -1: quote_type = "'''"
            
            if quote_type and line.count(quote_type) % 2 != 0:
                active_quote = quote_type
            new_lines.append(line)
    return new_lines


def _unmark_multiline_strings(lines):
    """Pre-processor to unmark lines that fall within multi-line string literals."""
    new_lines = []
    for line in lines:
        if re.search(re.escape(PIOTON_MULTILINE_IDENTIFIER) + r'\s*$', line):
            new_lines.append(line.replace(PIOTON_MULTILINE_IDENTIFIER, ""))
        else:
            new_lines.append(line)
    return new_lines


def _is_in_string(line, index):
    """Checks if a character index in a line is inside a string literal."""
    # Matches single and double quoted strings, including basic escaped quotes
    string_pattern = r'(\"(?:\\.|[^"\n])*\"|\'(?:\\.|[^\'\n])*\')'
    for match in re.finditer(string_pattern, line):
        if match.start() <= index < match.end():
            return True
    return False

def _smart_replace(line, target, replacement, is_regex=False):
    """Replaces target with replacement only if it is not inside a string literal."""
    if re.search(re.escape(PIOTON_MULTILINE_IDENTIFIER) + r'\s*$', line):
        return line
    pattern = target if is_regex else re.escape(target)
    return re.sub(pattern, lambda m: m.group(0) if _is_in_string(line, m.start()) else replacement, line)

def _translate_print(lines):
    new_lines = []
    for line in lines:
        # Replace keywords only if they aren't in strings
        new_line = _smart_replace(line, '^scríobh', 'print', is_regex=True)
        new_line = _smart_replace(new_line, ' scríobh', ' print')
        new_line = _smart_replace(new_line, '\tscríobh', '\tprint')
        new_lines.append(new_line)
    return new_lines


def _translate_for(lines):
    new_lines = []
    for line in lines:
        new_line = _smart_replace(line, '^do achan', 'for', is_regex=True)
        new_line = _smart_replace(new_line, ' do achan ', ' for ')
        new_line = _smart_replace(new_line, ' sa ', ' in ')
        new_lines.append(new_line)
    return new_lines


def _translate_and(lines):
    new_lines = []
    for line in lines:
        new_line = _smart_replace(line, ' agus ', ' and ')
        new_lines.append(new_line)
    return new_lines


def _translate_or(lines):
    new_lines = []
    for line in lines:
        new_line = line.replace(' nó ',' or ')
        new_lines.append(new_line)
    return new_lines


def _translate_bools(lines):
    new_lines = []
    for line in lines:
        new_line = line.replace('Fíor','True').replace('Bréagach','False')
        new_lines.append(new_line)
    return new_lines


def _translate_def(lines):
    new_lines = []
    for line in lines:
        if (re.search(" a sainigh\:$", line)):
            start = len(line) - len(line.lstrip())
            new_line = line[:start]+'def '+line[start:]
            colon = new_line.index(':')
            new_line = new_line[:colon-10]+new_line[colon:]
            new_lines.append(new_line)
        elif (re.search("\scuir amach ", line)):
            new_line = line.replace('cuir amach','return')
            new_lines.append(new_line)
        else:
            new_lines.append(line)
    return new_lines


def _translate_if(lines):
    new_lines = []
    for line in lines:
        new_line = line.replace('seachas dá','elif')
        new_line = new_line.replace('dá','if')
        new_line = new_line.replace('seachas','else')
        new_lines.append(new_line)
    return new_lines


def _translate_with_as(lines):
    new_lines = []
    for line in lines:
        new_line = line.replace(' ag cosiul le ',' as ')
        if (re.search("^glac\s", new_line)):
            new_line = re.sub("^glac", 'with', new_line)
        else:
            new_line = new_line.replace(' glac ', ' with ')
        new_lines.append(new_line)
    return new_lines


def _translate_open_close(lines):
    new_lines = []
    for line in lines:
        new_line = line.replace(' oscail(',' open(').replace('druid(','close(')
        new_lines.append(new_line)
    return new_lines


def _translate_none(lines):
    new_lines = []
    for line in lines:
        new_line = line.replace('Rud Ar Bíth', 'None')
        new_lines.append(new_line)
    return new_lines


def _translate_assert(lines):
    new_lines = []
    for line in lines:
        new_line = line.replace('seiceáil', 'assert')
        new_lines.append(new_line)
    return new_lines


def _translate_imports(lines):
    new_lines = []
    for line in lines:
        if (re.search("^ó\s", line)):
            new_line = re.sub("^ó", 'from', line)
        else:
            new_line = line.replace(' ó ', ' from ')

        if (re.search("^tóg isteach\s", new_line)):
            new_line = re.sub("^tóg isteach", 'import', new_line)
        else:
            new_line = new_line.replace(' tóg isteach ', ' import ')
        new_lines.append(new_line)
    return new_lines


def _translate_await(lines):
    new_lines = []
    for line in lines:
        new_line = line.replace('fanacht go ', 'await ')
        new_lines.append(new_line)
    return new_lines


def _translate_break(lines):
    new_lines = []
    for line in lines:
        new_line = line.replace(' brís ', ' break ')
        new_lines.append(new_line)
    return new_lines


def _translate_del(lines):
    new_lines = []
    for line in lines:
        if (re.search(" a bhaint$", line)):
            start = len(line) - len(line.lstrip())
            new_line = line[:start]+'del '+line[start:]
            new_line = new_line.replace(' a bhaint', '')
            new_lines.append(new_line)
        else:
            new_lines.append(line)
    return new_lines


def _translate_async(lines):
    new_lines = []
    for line in lines:
        new_line = line.replace('aisioncronach ', 'async ')
        new_lines.append(new_line)
    return new_lines


def _translate_class(lines):
    new_lines = []
    for line in lines:
        if (re.search("^\s*rang ", line)):
            start = len(line) - len(line.lstrip())
            new_line = line[:start]+'class'+line[start+4:]
            new_lines.append(new_line)
        else:
            new_lines.append(line)
    return new_lines


def _translate_continue(lines):
    new_lines = []
    for line in lines:
        new_line = line.replace(' lean ort', ' continue')
        new_lines.append(new_line)
    return new_lines


def _translate_raise(lines):
    new_lines = []
    for line in lines:
        if (re.search("^\s*seas ", line)):
            start = len(line) - len(line.lstrip())
            new_line = line[:start]+'raise'+line[start+4:]
        else:
            new_line = line
        new_line = new_line.replace(' seas ', ' raise ')
        new_lines.append(new_line)
    return new_lines


def _translate_try_except_finally(lines):
    new_lines = []
    for line in lines:
        if (re.search("^iarraidh", line)):
            start = len(line) - len(line.lstrip())
            new_line = line[:start]+'try'+line[start+8:]
        else:
            new_line = line
        new_line = new_line.replace(' iarraidh:', ' try:')

        if (re.search("^ach", line)):
            start = len(new_line) - len(new_line.lstrip())
            new_line = new_line[:start]+'except'+new_line[start+3:]
        new_line = new_line.replace(' ach ', ' except ')
        new_line = new_line.replace(' ach:', ' except:')

        if (re.search("^ag an deireadh", line)):
            start = len(new_line) - len(new_line.lstrip())
            new_line = new_line[:start]+'finally'+new_line[start+14:]
        new_line = new_line.replace(' ag an deireadh:', ' finally:')
        new_lines.append(new_line)
    return new_lines


def _translate_global(lines):
    new_lines = []
    for line in lines:
        new_line = line.replace(' domhanda ', ' global ')
        new_lines.append(new_line)
    return new_lines


def _translate_not(lines):
    new_lines = []
    for line in lines:
        new_line = line.replace(' níl ', ' not ')
        new_lines.append(new_line)
    return new_lines


def _translate_is(lines):
    new_lines = []
    for line in lines:
        new_line = line.replace(' céanna ', ' is ')
        new_lines.append(new_line)
    return new_lines


def _translate_pass(lines):
    new_lines = []
    for line in lines:
        new_line = line.replace(' neamhiontas a dhéanamh', ' pass ')
        new_lines.append(new_line)
    return new_lines


def _translate_while(lines):
    new_lines = []
    for line in lines:
        if (re.search("^\s*nuair ", line)):
            start = len(line) - len(line.lstrip())
            new_line = line[:start]+'while'+line[start+5:]
            new_lines.append(new_line)
        else:
            new_lines.append(line)
    return new_lines


def _translate_yield(lines):
    new_lines = []
    for line in lines:
        if (re.search("^\s*tabhair", line)):
            start = len(line) - len(line.lstrip())
            new_line = line[:start]+'yield'+line[start+7:]
            new_lines.append(new_line)
        else:
            new_lines.append(line)
    return new_lines


def show_syntax():
    print("""
print(x)                       --> scríobh(x)

for i in y:                    --> do achan i sa y:

while (condition)              --> nuair (condition):

and                            --> agus

or                             --> nó

True, False                    --> Fíor, Bréagach

not                            --> níl

is                             --> céanna

def func(x):                   --> func(x) a sainigh:

if (condition):                --> dá (condition):

elif (condition):              --> seachas dá (condition):

else:                          --> seachas:

with x() as y:                 --> glac x() ag cosiul le y:

open()                         --> oscail()

f.close()                      --> f.druid()

None                           --> Rud Ar Bíth

assert (cond)                  --> seiceáil (condition)

from x import y                --> ó x tóg isteach y

async def func():              --> aisioncronach func() a sainigh:

await asyncio.sleep(1)         --> fanacht go asyncio.sleep(1)

break                          --> brís

del x,y                        --> x,y a bhaint

class Example(object):         --> rang Example(object):

continue                       --> lean ort

raise Exception()              --> seas Exception()

try:                           --> iarraidh:

except Exception as e:         --> ach Exception ag cosiul le e:

finally:                       --> ag an deireadh:

global var                     --> domhanda var

pass                           --> neamhiontas a dhéanamh

yield x                        --> tabhair x

""")

try:
    ip = get_ipython()
    # ip.input_transformers_cleanup.append(_mark_multiline_strings)
    ip.input_transformers_cleanup.append(_translate_print)
    ip.input_transformers_cleanup.append(_translate_for)
    ip.input_transformers_cleanup.append(_translate_and)
    ip.input_transformers_cleanup.append(_translate_or)
    ip.input_transformers_cleanup.append(_translate_bools)
    ip.input_transformers_cleanup.append(_translate_def)
    ip.input_transformers_cleanup.append(_translate_if)
    ip.input_transformers_cleanup.append(_translate_with_as)
    ip.input_transformers_cleanup.append(_translate_open_close)
    ip.input_transformers_cleanup.append(_translate_none)
    ip.input_transformers_cleanup.append(_translate_assert)
    ip.input_transformers_cleanup.append(_translate_imports)
    ip.input_transformers_cleanup.append(_translate_await)
    ip.input_transformers_cleanup.append(_translate_break)
    ip.input_transformers_cleanup.append(_translate_del)
    ip.input_transformers_cleanup.append(_translate_async)
    ip.input_transformers_cleanup.append(_translate_class)
    ip.input_transformers_cleanup.append(_translate_continue)
    ip.input_transformers_cleanup.append(_translate_raise)
    ip.input_transformers_cleanup.append(_translate_try_except_finally)
    ip.input_transformers_cleanup.append(_translate_global)
    ip.input_transformers_cleanup.append(_translate_not)
    ip.input_transformers_cleanup.append(_translate_is)
    ip.input_transformers_cleanup.append(_translate_pass)
    ip.input_transformers_cleanup.append(_translate_while)
    ip.input_transformers_cleanup.append(_translate_yield)
    print("""UserWarning: 
You're using píotón, a tool to write IPython code as Gaeilge.
Call pioton.show_syntax() to see the new syntax provided.
This wasn't built to be robust, so we don't recommend it for
anything important. If you still want to use it for anything 
important knowing this, go have a wee word with yourself.""")
except Exception as e:
    pass
