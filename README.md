# Píotón - Write Python code in Irish
---
### Installation:

pip: 

`pip install pioton` 

github: 

clone the repo, run `python -m build`, then `pip install` the `.whl` file produced in the `dist/` folder.

---
#### USAGE Transpiled:
write your píotón code in one or more scripts with a '.pag' (Python as Gaeilge) extension, and run 

`tiomsaitheoir file.pag [file2.pag [...]]`

which will transpile the píotón scripts into pure Python '.py' files. Running 

`tiomsaitheoir -h`

will provide further details and examples, and running 

`tiomsaitheoir -s`

will show an overview of the syntax for píotón code 

#### USAGE IPython:
There are two modes of operation in IPython/Jupyter Notebooks:

  * 'magic' mode: interpret a single cell as Píotón.
  * 'notebook' mode: interpret all cells as Píotón.

Setup: 

```python
from pioton import píotón_magic, píotón_notebook
píotón_magic() # activate the magic command
píotón_notebook() # activate the notebook command
```

Magic Usage:
```python
%% píotón
scríobh('this cell will be interpreted as píotón code')
```

Syntax:
Call `pioton.show_syntax()` to print a full description of the Píotón syntax.

---

### Limitations
Currently, there is no import system in place to import (un-transpiled) Píotón code into other scripts / notebooks.

---

### Syntax

```python
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
```