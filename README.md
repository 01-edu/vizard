## Vizard: Graph Visualization & Utilities

Vizard is a Python package for creating and visualizing graphs. It provides tools for graph rendering making it ideal custom data visualization tasks.

### Features
- **Modular Graph Rendering:** Easily create and display circular (modular) graphs with custom data and advanced SVG rendering.
- **Color Tools:** Generate and interpolate color gradients, convert between color formats, and validate color codes for beautiful graph visualizations.
- **Text Utilities:** Convert and format text for labeling and processing graph data.
- **Render Utilities:** handle informations displayed in `info_card`

### Package Structure
- `circular_graph.modular_graph`: Main class and helpers for modular graph creation and rendering.
- `circular_graph.color_tools`: Subpackage for color conversion and gradient generation.
- `circular_graph.tools`: Subpackage for utilities.


### Installation
Install via uv pip :
```bash
uv pip install git+https://github.com/01-edu/vizard.git
```
>*ps: must be reinstalled each time kernel is restarted when used in a ipynb notebook*

### License & Authors
See `setup.py` for license and author information.