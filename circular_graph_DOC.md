# circular_graph Module Documentation

This documentation covers the `circular_graph` module and its submodules, providing detailed explanations and usage examples for each function.

---

## Table of Contents
- [Overview](#overview)
- [modular_graph](#modular_graph)
- [color_tools.color_conversion](#colortoolscolor_conversion)
- [color_tools.gradient](#colortoolsgradient)
- [tools.text_conversion](#toolstext_conversion)

---

## Overview

The `circular_graph` package is a Python library for creating, visualizing, and manipulating modular (circular) graphs, with additional utilities for color gradients and text conversion. It is designed for analytical and educational purposes, supporting advanced graph rendering and color mapping.

---

## modular_graph

### Class: `modular_graph`
Implements a modular (circular) graph object with advanced rendering and helper functions.

#### Constructor
```python
modular_graph(graph_json, data, piscines_list, checkpoints_list, mandatory_list, gradient_colors=None)
```
- **graph_json**: Graph structure in JSON format.
- **data**: Associated data for the graph.
- **piscines_list**: List of piscine nodes.
- **checkpoints_list**: List of checkpoint nodes.
- **mandatory_list**: List of mandatory nodes.
- **gradient_colors**: Optional list of three hex colors for gradients.

#### Methods
- `polar_to_cartesian(center_x, center_y, radius, angle_in_degrees)`
  - Converts polar coordinates to cartesian.
- `get_arc_bounding_angles(arcs_types, index, gap, ref_arc, rotate)`
  - Computes bounding angles for an arc.
- `get_arc_coords(center_coords, radius, arcs_types, index, reverse=False, gap=0, rotate=0, ref_arc=None)`
  - Gets cartesian coordinates for an arc.
- `get_content_name(content)`
  - Extracts the name from a content object.
- `create_element(tag, attributes=None, text_content=None, ns=None)`
  - Creates an SVG element.
- `render_star_icon(x, y, fill, width, name, content_name, value)`
  - Renders a star icon at given coordinates.
- `render_checkpoint_icon(x, y, fill, width)`
  - Renders a checkpoint icon.
- `render_text_path(parent_group, text, id_str, index, circle_params)`
  - Renders text along an arc path.
- `render_content(parent_group, content_item_data, circle_props_from_parent, object_attrs=None, is_sub_content=False, content_name=None)`
  - Renders a content item.
- `render_sub_contents(parent_g, content_data_with_subs, parent_circle_props)`
  - Renders sub-content items.
- `render_arc(parent_group, section_data, circle_config_from_parent, index, id_prefix)`
  - Renders an arc section.
- `render_slice(parent_group, slice_data, index, all_sections_types)`
  - Renders a slice of the graph.

**Usage Example:**
```python
from circular_graph.modular_graph import modular_graph
mg = modular_graph(graph_json, data, piscines, checkpoints, mandatory)
mg.render_slice(...)
```

---

## color_tools.color_conversion

### Functions

- `hex_to_rgb2(hex_color)`
  - Converts a hex color string (e.g., '#FF0000') to an RGB tuple.
  - **Example:** `hex_to_rgb2('#FF0000')  # (255, 0, 0)`

- `rgb_to_hex2(rgb)`
  - Converts an RGB tuple to a hex color string.
  - **Example:** `rgb_to_hex2((255, 0, 0))  # '#ff0000'`

- `is_valid_hex_color_2(color_string)`
  - Checks if a string is a valid 3- or 6-digit hex color code.
  - **Example:** `is_valid_hex_color_2('#FFF')  # True`

- `interpolate_color(value, max_value, start_color, mid_color, end_color)`
  - Interpolates between three colors based on a value and maximum value.
  - **Example:** `interpolate_color(5, 10, '#FF0000', '#FFFF00', '#00FF00')`

- `value_to_color(value, max_value, gradient_colors=None)`
  - Maps a numeric value to a color on a gradient defined by three colors.
  - **Example:** `value_to_color(7, 10, ['#FFD700', '#32CD32', '#1E90FF'])`

---

## color_tools.gradient

### Function: `create_gradient_html`
Generates and displays an HTML file showing a color gradient using three hex color codes.

**Signature:**
```python
def create_gradient_html(start_color_hex, mid_color_hex, end_color_hex, min_val, max_val):
    """
    Generates and optionally displays an HTML file displaying a color gradient.
    Args:
        start_color_hex (str): Hex code for the start color.
        mid_color_hex (str): Hex code for the middle color.
        end_color_hex (str): Hex code for the end color.
        min_val (float or int): The minimum value for the gradient scale.
        max_val (float or int): The maximum value for the gradient scale.
    Returns:
        str: The generated HTML content as a string.
    """
```

**Usage Example:**
```python
from circular_graph.color_tools.gradient import create_gradient_html
html = create_gradient_html('#FFD700', '#32CD32', '#1E90FF', 0, 100)
```

---

## tools.text_conversion

### Functions

- `to_slug(text: str, project_path_dict: dict) -> str`
  - Converts a string into a slug (lowercase, hyphens for non-alphanumerics, strips hyphens).
  - **Example:** `to_slug('Hello World!', {})  # 'hello-world'`

- `replace_keys(input_dict, project_path_dict: dict) -> str`
  - Replaces the keys of a dictionary with their slugified versions.
  - **Example:** `replace_keys({'Hello World!': 1}, {})  # {'hello-world': 1}`

---

## License
See `setup.py` for license and author information.
