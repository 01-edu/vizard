# Circular_graph — Documentation

This module provides tools to generate circular SVG maps representing modules, projects, "piscines" and checkpoints, with support for "classic" (single value) and "distribution" (statistics) visualizations.

---
## Overview

- Main module: `circular_graph.modular_graph` — the `modular_graph` class that builds and renders a circular SVG map.
- Color utilities: `circular_graph.color_tools` — functions for interpolation and hex/RGB conversion, and generation of a gradient HTML block.
- Utilities: `circular_graph.tools` — helper functions for rendering (info cards, text conversion, SVG helpers).

---
## Important structure

- `circular_graph/`
  - `modular_graph.py` — `modular_graph` class (main API).
  - `color_tools/`
    - `color_conversion.py` — color conversions and value → color mapping.
    - `gradient.py` — generates an HTML/CSS/JS block for a gradient legend.
  - `tools/`
    - `renderer_utils.py` — JS strings for info-cards.
    - `text_conversion.py` — slugification utilities and key replacement.

---
## Quick installation

```bash
pip install git+https://github.com/01-edu/vizard.git
```

---
## Usage example (notebook)

```python
from circular_graph.modular_graph import modular_graph
from circular_graph.color_tools.color_conversion import value_to_color

# graph_json: string containing the structural description (see examples)
data_map = {"project-a": 10, "project-b": 3, "project-c": 7}
piscines = ["piscine-1"]
checkpoints = ["checkpoint-1"]
mandatory = ["project-a"]

g = modular_graph(graph_json, data_map, piscines, checkpoints, mandatory, kind="classic")
g.show()  # displays the SVG in Jupyter
```

For "distribution" visualization, provide `data` values as pandas.Series containing the expected statistical keys (`min`, `q1`, `median`, `q3`, `max`, `outliers`).

---
## API summary

- class `modular_graph(graph_json: str, data: dict|pd.Series, piscines_list: list, checkpoints_list: list, mandatory_list: list, gradient_colors: list[str]=None, kind: "classic"|"distribution"="classic")`
  - Renders the map and exposes `graph_svg_text` (SVG string).
  - Notable methods:
    - `show()` — displays the SVG in Jupyter.
    - `display_gradient_legend(start_color_hex, mid_color_hex, end_color_hex, min_val, max_val)` — injects the legend.

- `tools.text_conversion`
  - `to_slug(text, mapping)` — slugifies or uses a mapping.
  - `replace_keys(dict, mapping)` — replaces dict keys with slugs.

---
## Example graph_json (schema)

The expected JSON describes sections / arcs / contents. See `circular_graph/documentation.md` for a concrete example and the full structure.

[see reference here](modular_graph.md)
<br/>
[see Demo here](demo.md)
## License
01 Data Science Team (DTF)

