## Vizard: Circular Graph Visualization & Utilities

Vizard is a Python package for creating, visualizing, and analyzing modular (circular) graphs. It provides advanced tools for graph rendering, color gradients, and text conversion, making it ideal for analytical, educational, and data visualization tasks.

### Features
- **Modular Graph Rendering:** Easily create and display circular (modular) graphs with custom data and advanced SVG rendering.
- **Color Tools:** Generate and interpolate color gradients, convert between color formats, and validate color codes for beautiful graph visualizations.
- **Text Utilities:** Convert and format text for labeling and processing graph data.

### Package Structure
- `circular_graph.modular_graph`: Main class and helpers for modular graph creation and rendering.
- `circular_graph.color_tools`: Subpackage for color conversion and gradient generation.
- `circular_graph.tools`: Subpackage for text conversion utilities.

### Example Usage
```python
from circular_graph.modular_graph import modular_graph
from circular_graph.color_tools.color_conversion import value_to_color

# Create a modular graph instance
mg = modular_graph(graph_json, data, piscines, checkpoints, mandatory)

# Map a value to a color
color = value_to_color(7, 10)
```

### Installation
Install via pip (after cloning or packaging):
```bash
pip install .
```

### Requirements
- Python >= 3.8
- matplotlib, pandas, numpy, plotly, IPython, beautifulsoup4

### License & Authors
See `setup.py` for license and author information.
# vizard