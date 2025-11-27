# pyscript

## Deploy

<img width="1131" height="559" alt="image" src="https://github.com/user-attachments/assets/f52f7efe-5fa4-468d-95c7-196071190500" />

## How does this app work?
This app performs basic analysis (GC%, complement) for a user defined sequence like the webR and other examples. The files speak to each other as follows:
* `index.html` lays out the page and imports the pyscript runtime, essentially a interpreter from python to WASM.
* `main.py` defines the functions used to modify input. The pyscript library is also used to annotate some function with reactivity, like runnin on-click.
* `pyscript.toml` provides information on the applike a title, and a list of libraries to be imported (Biopython in this case)

## How is python executed as WASM?
`index.html` imported the pyscript runtime in the following line:
```html
  <script type="module"
          src="https://pyscript.net/releases/2025.11.1/core.js"></script>
```

At the bottom, it then points to where the python code should be found that substitutes the usual JavaScript functionality:
```html
  <!-- Tell PyScript where to find Python code and config -->
  <script type="py" src="./main.py" config="./pyscript.toml"></script>
```

If you then look in `main.py`, you see functions defined, including the `on_run()` function that executes when you hit the Analyze button. The function is annotated for pyscript, so the runtime knows when to execute it:
```python
    @when("click", "#run")
    def on_run(event) -> None:
        btn.disabled = True
        status_el.textContent = "Running…"
    #... and so on
```

Looking at the top of `main.py`, you will see pyscript imported with the document class too, which selects html elements in the same way as the conventional html querySelector that navigates the DOM to find corresponding elements.
```python
from pyscript import when, document
from Bio.Seq import Seq
from Bio.SeqUtils import gc_fraction

status_el = document.querySelector("#status")
output_el = document.querySelector("#output")
btn = document.querySelector("#run")

# At this point PyScript has already applied pyscript.toml,
# so Biopython is available.
status_el.textContent = "Python + Biopython ready."
btn.disabled = False
#... and so on
```

## How do the data exit WASM?
In pyscript, the python code executes in WASM and behaves like JavaScript, so these is no explicit step of handing the data back to the DOM like for the webR example. 

## Questions
1. Is it essential to import css just for pyscript? If so, is this because the html elements are bespoke for pyscript?
```html
  <script type="module"
          src="https://pyscript.net/releases/2025.11.1/core.js"></script>

```

2. What are the key things that make pyscript different from pyodide?

3. Would you use pyscript to build out an entire client side tool with complex functionality and different displays? Does it allow for lower level control than shiny?
