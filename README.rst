# Píotón - Write Python code in Irish
---
### Installation:

pip: 

    pip install pioton 

github: 

clone the repo, move the contents of the pioton/ folder somewhere accessible by your PythonPATH

---
### Try it online:

[run it in your browser](https://replite.vercel.app/repl/index.html)

select 'pyolite' kernel, then copy and paste the following into the cell at the bottom, and press shift-enter to start
```
import micropip
await micropip.install('pioton')
import pioton
```

---
#### USAGE Transpiled:
write your píotón code in one or more scripts with a '.pag' (Python as Gaeilge) extension, and run 

    tiomsaitheoir file.pag [file2.pag [...]]

which will transpile the píotón scripts into pure Python '.py' files. Running 

    tiomsaitheoir -h

will provide further details and examples, and running 

    tiomsaitheoir -s

will show an overview of the syntax for píotón code 

#### USAGE IPython:
simply import píotón in any IPython environment (including Jupyter Notebooks) and start writing your code as Gaeilge.
Call `pioton.show_syntax()` to print a full description of the new irish syntax.

#### THIS IS FOR FUN - DO NOT USE THIS FOR ANYTHING IMPORTANT
I can't stress that enough, I really didn't make sure it's robust at all, it's against Python standards, any code written in it will be completely unmaintainable, etc.

---
