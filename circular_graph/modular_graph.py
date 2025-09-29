from xml.etree import ElementTree as ET2
from typing import Literal
import math
import json 
from circular_graph.color_tools.color_conversion import value_to_color
from circular_graph.color_tools.gradient import create_gradient_html
from IPython.display import display, HTML
from circular_graph.tools.renderer_utils import show_info_card

# __________________________________________________________________________________#
# |                                                                                  |#
# |                               Modular graph object                               |#
# |__________________________________________________________________________________|#


class modular_graph:
    def __init__(
        self,
        graph_json,
        data,
        piscines_list,
        checkpoints_list,
        mandatory_list,
        gradient_colors=None,
        kind: Literal["classic", "distribution"] = "classic",
    ):
        #Kind of graph
        self.kind = kind
        # defs of the svg
        self.svg_defs = ET2.Element("defs")
        # Color Palette
        self.gradient_colors = gradient_colors
        self.COLORS = {
            "neutral": "#808080",  # Grey
            "neutralAlt": "#A9A9A9",  # Dark Grey
            "grey": "#D3D3D3",  # Light Grey
            "grey10": "#1A1A1A",
            "grey50": "rgba(211, 211, 211, 0.5)",
            "grey80": "rgba(128, 128, 128, 0.8)",
            "teal": "#008080",
            "orange": "#FFA500",
            "red": "#FF0000",
            "white": "#FFFFFF",
            "piscine_default_color": "#4682B4",  # SteelBlue for piscines if no color
        }
        # SVG links
        self.SVG_NS = "http://www.w3.org/2000/svg"
        self.XLINK_NS = "http://www.w3.org/1999/xlink"
        ET2.register_namespace("", self.SVG_NS)
        ET2.register_namespace("xlink", self.XLINK_NS)

        # line contstant
        self.LINE_CONSTANTS = {
            "startOffset": 70,
            "startRadius": 220,
            "endRadius": 575,
        }

        # slices constants
        self.SLICE_GAP = 20
        self.SLICE_CONSTANTS = {
            "textCircle": {
                "radius": 210,
                "gap": self.SLICE_GAP,
                "nameColor": self.COLORS["teal"],
                "nameFontSize": 50,
            },
            "centralPointCircle": {"angle": 0, "radius": 0, "contentRadius": 8},
            "entryPointCircle": {
                "radius": 100,
                "gap": self.SLICE_GAP,
                "contentRadius": 8,
                "contentNameOffset": 35,
            },
            "innerCircle": {
                "radius": 360,
                "gap": self.SLICE_GAP,
                "contentRadius": 10,
                "nameFont": "IBM Plex Mono",
                "nameFontSize": 21,
                "nameColor": self.COLORS["neutral"],
                "nameRadiusOffset": 65,
                "contentNameOffset": 40,
                "subContentRadius": 3.25,
                "subContentGap": 2.75,
                "subContentRadiusOffset": 75,
            },
            "outerCircle": {"radius": 570, "gap": self.SLICE_GAP},
            "outerArc": {
                "radius": 570,
                "gap": 10,
                "contentRadius": 5,
                "nameFont": "IBM Plex Mono",
                "nameFontSize": 21,
                "nameColor": self.COLORS["neutral"],
                "nameRadiusOffset": 65,
            },
        }

        # circles constants
        self.MIDDLE_CIRCLE_CONSTANTS = {
            "radius": 815,
            "gap": 8,
            "contentRadius": 5,
            "nameRadiusOffset": 115,
            "nameColor": self.COLORS["neutral"],
            "nameFontSize": 50,
        }

        self.OUTER_CIRCLE_CONSTANTS = {
            "radius": 1075,
            "gap": 12,
            "contentRadius": 5,
            "nameRadiusOffset": 115,
            "nameColor": self.COLORS["neutral"],
            "nameFontSize": 50,
        }

        # content constants
        self.PISCINE_CONSTANTS = {"nameOffset": 50, "radius": 35}
        self.STAR_CONSTANTS = {"width": 24, "subContentWidth": 18}
        self.CHECKPOINT_CONSTANTS = {"width": 22, "subContentWidth": 16}

        # Global center
        self.CURRENT_CENTER = 1000

        self.data = data
        if self.kind == "classic":
            try:
                self.max_value = max(data.values())
            except:
                self.max_value = 0
        self.piscines_list = piscines_list
        self.checkpoints_list = checkpoints_list
        self.mandatory_list = mandatory_list

        self.graph_json = graph_json
        self.graph_dict = {"graph": json.loads(self.graph_json)}

        # create the SVG
        self.root_svg, self.graph_svg_text = self.render_circular_map01(self.graph_dict)

    # *#########################################################################* #
    # *************************************************************************** #
    # *************************************************************************** #
    # ************************** Helper Functions ******************************* #
    # **************************************************************************  #
    # **************************************************************************  #
    # *#########################################################################* #

    # * helper function to convert polar to cartesian cords
    def polar_to_cartesian(self, center_x, center_y, radius, angle_in_degrees):
        """
        This method converts polar coordinates
        (center x, center y, radius, and angle in degrees)
        to Cartesian coordinates (x, y).
        Variables:

            center_x (float): The x-coordinate of the center of the circular graph.
            center_y (float): The y-coordinate of the center of the circular graph.
            radius (float): The radius of the circle.
            angle_in_degrees (float): The angle in degrees from the positive x-axis to the point on the circle.

        Return Value:

            The function returns a dictionary with the following keys:

            x (float): The x-coordinate of the point on the circular graph.
            y (float): The y-coordinate of the point on the circular graph.
            angle (float): The angle in degrees from the positive x-axis to the point on the circle.


        """
        angle_in_radians = (angle_in_degrees - 90) * math.pi / 180.0
        return {
            "x": center_x + (radius * math.cos(angle_in_radians)),
            "y": center_y + (radius * math.sin(angle_in_radians)),
            "angle": angle_in_degrees,
        }

    ###############################################################################################
    ###############################################################################################

    # * helper function to get arc bounding angles
    def get_arc_bounding_angles(self, arcs_types, index, gap, ref_arc, rotate):
        """
        This method calculates the start, end, and mid angles of an arc

        Variables:

            arcs_types (list of strings): A list of arc types, where each type is either 'slice' or 'line'.
            index (int): The index of the arc in the arcs_types list.
            gap (float): The angle gap between arcs in degrees.
            ref_arc (dict): A reference arc object with the following keys:
                startAngle (float): The start angle of the reference arc in degrees.
                endAngle (float): The end angle of the reference arc in degrees.
            rotate (float): The rotation angle of the arc in degrees.

        Return Value:

            The function returns a dictionary with the following keys:

            startAngle (float): The start angle of the arc in degrees.
            endAngle (float): The end angle of the arc in degrees.
            midAngle (float): The mid angle of the arc in degrees.
        """
        arcs_count = len(arcs_types)
        single_arc = arcs_count == 1
        slices_count = arcs_types.count(
            "slice"
        )  # Assumes 'line' takes 0 space for length calculation

        ref_arc_is_circle = ref_arc["startAngle"] == 0 and ref_arc["endAngle"] == 360
        ref_arc_length = ref_arc["endAngle"] - ref_arc["startAngle"]

        gaps_total_angle = gap * (arcs_count if ref_arc_is_circle else arcs_count - 1)
        gaps_angle = 0 if single_arc else gaps_total_angle

        slice_length = (
            (ref_arc_length - gaps_angle) / slices_count if slices_count > 0 else 0
        )
        arcs_lengths = [
            slice_length if arc_type == "slice" else 0 for arc_type in arcs_types
        ]

        base_start_angle = (
            rotate - (arcs_lengths[0] / 2 if arcs_lengths else 0)
            if ref_arc_is_circle and not single_arc
            else ref_arc["startAngle"] + rotate
        )

        previous_arcs_length = sum(arcs_lengths[:index]) + base_start_angle

        start_angle = previous_arcs_length + index * gap
        end_angle = start_angle + arcs_lengths[index]
        mid_angle = start_angle + (end_angle - start_angle) / 2

        return {"startAngle": start_angle, "endAngle": end_angle, "midAngle": mid_angle}

    ###############################################################################################
    ###############################################################################################

    # * helper function to get arc cartesian cords
    def get_arc_coords(
        self,
        center_coords,
        radius,
        arcs_types,
        index,
        reverse=False,
        gap=0,
        rotate=0,
        ref_arc=None,
    ):
        """
        This method generates the coordinates for an arc based on the bounding angles
        calculated by the get_arc_bounding_angles function.

        Variables:

            center_coords (dict): A dictionary with the coordinates of the circular graph center, where 'x' and 'y' are the x and y coordinates respectively.
            radius (float): The radius of the arc.
            arcs_types (list of strings): A list of arc types, where each type is either 'slice' or 'line'.
            index (int): The index of the arc in the arcs_types list.
            reverse (bool): A boolean indicating whether to reverse the arc.
            gap (float): The angle gap between arcs in degrees.
            rotate (float): The rotation angle of the arc in degrees.
            ref_arc (dict): A reference arc object with the following keys:
                startAngle (float): The start angle of the reference arc in degrees.
                endAngle (float): The end angle of the reference arc in degrees.

        Return Value:


            The function returns a dictionary with the following keys:

            path (str): The SVG path string for the arc.
            start (dict): A dictionary with the coordinates of the arc's start point, where 'x' and 'y' are the x and y coordinates respectively.
            end (dict): A dictionary with the coordinates of the arc's end point, where 'x' and 'y' are the x and y coordinates respectively.
            middle (dict): A dictionary with the coordinates of the arc's mid point, where 'x' and 'y' are the x and y coordinates respectively.
            fullCircle (bool): A boolean indicating whether the arc is a full circle.

        """

        if ref_arc is None:
            ref_arc = {"startAngle": 0, "endAngle": 360}

        angles = self.get_arc_bounding_angles(arcs_types, index, gap, ref_arc, rotate)
        start_angle, end_angle, mid_angle = (
            angles["startAngle"],
            angles["endAngle"],
            angles["midAngle"],
        )

        full_circle = round(end_angle) - round(start_angle) == 360
        end_command = " Z" if full_circle else ""

        on_circle_lower_edge = reverse and 90 < mid_angle < 270
        large_arc_flag = (
            1 if on_circle_lower_edge or (end_angle - start_angle > 180) else 0
        )
        sweep_flag = 0 if not full_circle and on_circle_lower_edge else 1

        flip_angle = 180 if reverse and on_circle_lower_edge else 0
        start_angle_flipped = start_angle + flip_angle
        end_angle_flipped = end_angle - (0.01 if full_circle else 0) + flip_angle
        mid_angle_flipped = mid_angle + flip_angle

        start = self.polar_to_cartesian(
            center_coords["x"], center_coords["y"], radius, start_angle_flipped
        )
        end = self.polar_to_cartesian(
            center_coords["x"], center_coords["y"], radius, end_angle_flipped
        )
        middle = self.polar_to_cartesian(
            center_coords["x"], center_coords["y"], radius, mid_angle_flipped
        )

        d_str = f"M {start['x']} {start['y']} A {radius} {radius} 0 {large_arc_flag} {sweep_flag} {end['x']} {end['y']}{end_command}"
        return {
            "path": d_str,
            "start": start,
            "end": end,
            "middle": middle,
            "fullCircle": full_circle,
        }

    ###############################################################################################
    ###############################################################################################

    # * helper function extract content name
    def get_content_name(self, content):
        """
        get the content name

        as the content is either a text (single project) or dict (project with sub projects)

        variables:
            content (dict or string): the content object

        Return Value:
            string value indecating the content name
        """
        if isinstance(content, dict):
            return list(content.keys())[0]
        return str(content)

    ###############################################################################################
    ###############################################################################################

    # * helper function create SVG element
    def create_element(self, tag, attributes=None, text_content=None, ns=None):
        """
        This  method creates an SVG element using the xml.etree.ElementTree (ET) module.

        variables:

                tag (str): The name of the SVG element to create.
                attributes (dict): A dictionary of attributes to set on the element.
                text_content (str): The text content of the element.
                ns (str): The namespace of the element.

        Return Value:

                The function returns an ET.Element object representing the created SVG element.
        """
        if ns is None:
            ns = self.SVG_NS
        if ":" in tag:  # Handle xlink:href
            prefix, local_name = tag.split(":", 1)
            if prefix == "xlink":
                tag = f"{{{self.XLINK_NS}}}{local_name}"
        else:
            tag = f"{{{ns}}}{tag}"

        element = ET2.Element(tag)
        if attributes:
            for k, v in attributes.items():
                if ":" in k:
                    prefix, local_name = k.split(":", 1)
                    if prefix == "xlink":
                        k = f"{{{self.XLINK_NS}}}{local_name}"
                element.set(k, str(v))
        if text_content:
            element.text = text_content
        return element

    ###############################################################################################
    ###############################################################################################

    # * icon rendering function star icon
    def render_star_icon(self, x, y, fill, width, name, content_name, value):
        """
        This method generates an SVG element representing a star icon.

        variables:

            x (int): The x-coordinate of the icon.
            y (int): The y-coordinate of the icon.
            fill (str): The fill color of the icon.
            width (int): The width of the icon.

        return value:

            The function returns an SVG element representing the star icon.
        """
        g = self.create_element(
            "g",
            {
                "transform": f"translate({x - width / 2}, {y - width / 2}) scale({width/130})"
            },
        )
        title = self.create_element("title", text_content="Star icon")
        path = self.create_element(
            "path",
            {
                "fill": fill,
                "d": "M65 11l18 35 39 6-28 28 6 39-35-18-35 18 6-39L8 52l39-6 18-35z",
                "cx": str(x),
                "cy": str(y),
                "id": name,
                "project-name": content_name,
                "data-tooltip": str(value),
                "onpointerenter": show_info_card(self.kind),            
                "onpointerleave": 'document.getElementById("info_card").style.visibility = "hidden";',
            },
        )
        g.append(title)
        g.append(path)
        return g

    ###############################################################################################
    ###############################################################################################

    # icon rendering function checkpoint icon
    def render_checkpoint_icon(self, x, y, fill, width):
        """
        This method generates an SVG element representing a checkpoint icon (flag).

        variables:

            x (int): The x-coordinate of the icon.
            y (int): The y-coordinate of the icon.
            fill (str): The fill color of the icon.
            width (int): The width of the icon.

        return value:

            The function returns an SVG element representing the checkpoint icon.
        """
        height_factor = width / 18 * 22
        g = self.create_element(
            "g",
            {
                "transform": f"translate({x - width / 2}, {y - height_factor / 2}) scale({width/18})"
            },
        )
        title = self.create_element("title", text_content="Checkpoint icon")
        path = self.create_element(
            "path",
            {
                "fill": fill,
                "fill-rule": "evenodd",
                "clip-rule": "evenodd",
                "d": "M0 22V0h1.645v1.427C3.29.468 6.129-.256 9.355 1.45c3.187 1.686 6.174.687 7.198.037L18 .569v11.178l-.418.255c-1.451.884-5.19 2.036-9.129.035-3.134-1.593-5.677-.338-6.497.398l-.311.278V22H0ZM6.408 9.605V6.826c-2.247-.354-3.982.556-4.666 1.17l-.097-.094v2.61a7.78 7.78 0 0 1 4.763-.907Zm4.884-1.138a9.66 9.66 0 0 0 4.857-.36v2.674c-.99.454-2.794.908-4.857.449V8.467Zm0-1.175a8.57 8.57 0 0 1-2.1-.747 8.595 8.595 0 0 0-2.784-.882V2.236c.638.11 1.32.334 2.032.71a9.9 9.9 0 0 0 2.852.998v3.348Z",
            },
        )
        g.append(title)
        g.append(path)
        return g

    ###############################################################################################
    ###############################################################################################

    # component rendering function text path (as an arc shape)
    def render_text_path(self, parent_group, text, id_str, index, circle_params):
        """
        render an SVG text path to a parent group.

        Variables:
            parent_group (SVG element): The parent group to which the text path will be appended.
            text (str): The text to be rendered.
            id_str (str): The id of the text path.
            index (int): The index of the text path.
            circle_params (dict): A dictionary containing the circle parameters.


        """
        radius = circle_params["radius"] - (circle_params.get("nameRadiusOffset", 0))

        arc_path_data = self.get_arc_coords(
            center_coords={"x": self.CURRENT_CENTER, "y": self.CURRENT_CENTER},
            radius=radius,
            arcs_types=circle_params["arcs"],
            index=index,
            reverse=True,
            gap=circle_params.get("gap", 0),
            rotate=circle_params.get("rotate", 0),
            ref_arc=circle_params.get("refArc"),
        )

        g_text_path = self.create_element("g", {"id": f"g-{id_str}"})

        path_el = self.create_element(
            "path", {"d": arc_path_data["path"], "id": id_str, "fill": "none"}
        )
        g_text_path.append(path_el)

        text_el = self.create_element(
            "text",
            {
                "fill": circle_params.get("nameColor", self.COLORS["neutral"]),
                "text-anchor": "middle",
                "dominant-baseline": "middle",
                "font-size": str(circle_params.get("nameFontSize", 50)),
                "font-family": circle_params.get("nameFont", "IBM Plex Sans"),
            },
        )
        text_path_el = self.create_element(
            "textPath",
            {
                "startOffset": f"{50}%",
                "xlink:href": f"#{id_str}",
                "style": "letter-spacing: 0.75px;",
            },
            text_content=text,
        )
        text_el.append(text_path_el)
        g_text_path.append(text_el)
        parent_group.append(g_text_path)

    ###############################################################################################
    ###############################################################################################

    # component rendering function for content
    def render_content(
        self,
        parent_group,
        content_item_data,
        circle_props_from_parent,
        object_attrs=None,
        is_sub_content=False,
        content_name=None,
    ):
        """
        render an SVG elements for a graphical representation of content items, such as projects, exams, or piscines in the parent group

        Variables:

            parent_group (SVG element): The parent group to which the content item will be appended.
            content_item_data (dict): A dictionary containing the content item data.
            circle_props_from_parent (dict): A dictionary containing the circle properties from the parent.
            object_attrs (dict): A dictionary containing the object attributes.
            is_sub_content (bool): A boolean indicating whether the content item is a sub-content.
        """

        if object_attrs is None:
            object_attrs = {}

        name = self.get_content_name(content_item_data)
        value = self.data.get(name, 0)

        coords = self.polar_to_cartesian(
            self.CURRENT_CENTER,
            self.CURRENT_CENTER,
            circle_props_from_parent["radius"],
            circle_props_from_parent["angle"],
        )
        x, y = coords["x"], coords["y"]

        has_sub_contents = isinstance(content_item_data, dict)

        content_group = self.create_element("g", {"id": name})
        parent_group.append(content_group)

        # obj_type = object_attrs.get("type", "project")
        obj_mandatory = name in self.mandatory_list
        is_piscine = name in self.piscines_list
        fill_color = ""
        if self.kind == "classic":
            fill_color = (
            self.COLORS["neutral"]
            if value == 0
            else value_to_color(value, self.max_value, self.gradient_colors)
        )
        elif self.kind == "distribution":
            fill_color = (
                self.COLORS["neutral"]
                if value == 0
                else "teal"
            )

        icon_radius = (
            self.PISCINE_CONSTANTS["radius"]
            if is_piscine
            else circle_props_from_parent.get("contentRadius", 4)
        )

        if name in self.checkpoints_list:
            icon = self.render_checkpoint_icon(
                x,
                y,
                fill_color,
                (
                    self.CHECKPOINT_CONSTANTS["subContentWidth"]
                    if is_sub_content
                    else self.CHECKPOINT_CONSTANTS["width"]
                ),
            )
            content_group.append(icon)
        elif obj_mandatory:
            icon = self.render_star_icon(
                x,
                y,
                fill_color,
                (
                    self.STAR_CONSTANTS["subContentWidth"]
                    if is_sub_content
                    else self.STAR_CONSTANTS["width"]
                ),
                name,
                name if not content_name else content_name,
                value,
            )
            content_group.append(icon)
        else:
            if is_piscine:
                gradient = self.create_element(
                    "radialGradient",
                    attributes={
                        "id": content_item_data + "_gradient",
                        "cx": "50%",
                        "cy": "50%",
                        "r": "50%",
                        "fx": "50%",
                        "fy": "50%",
                    },
                )
                gradient.append(
                    self.create_element(
                        "stop",
                        attributes={
                            "offset": "0%",
                            "stop-color": fill_color,
                            "stop-opacity": "1",
                        },
                    )
                )
                gradient.append(
                    self.create_element(
                        "stop",
                        attributes={
                            "offset": "40%",
                            "stop-color": fill_color,
                            "stop-opacity": "0.5",
                        },
                    )
                )
                gradient.append(
                    self.create_element(
                        "stop",
                        attributes={
                            "offset": "100%",
                            "stop-color": fill_color,
                            "stop-opacity": "0",
                        },
                    )
                )
                self.defs.append(gradient)

            circle_el = self.create_element(
                "circle",
                {
                    "fill": (
                        fill_color
                        if not is_piscine
                        else f"url(#{content_item_data}_gradient)"
                    ),
                    "r": str(icon_radius),
                    "cx": str(x),
                    "cy": str(y),
                    "id": name,
                    "project-name": name if not content_name else content_name,
                    "data-tooltip": str(value),
                   "onpointerenter": show_info_card(self.kind),
                   "onpointerleave": 'document.getElementById("info_card").style.visibility = "hidden";',
                },
            )
            content_group.append(circle_el)

        # Content name text
        name_offset = (
            self.PISCINE_CONSTANTS["nameOffset"]
            if is_piscine
            else circle_props_from_parent.get("contentNameOffset", 34)
        )
        if not is_sub_content:
            text_el = self.create_element(
                "text",
                {
                    "x": str(x),
                    "y": str(y + name_offset),
                    "font-size": "12px",
                    "text-anchor": "middle",
                    "fill": self.COLORS["neutral"],
                    "font-family": "IBM Plex Mono",
                    "style": "text-transform: uppercase;",
                },
                text_content=name,
            )
            content_group.append(text_el)

        if has_sub_contents:
            self.render_sub_contents(
                content_group, content_item_data, circle_props_from_parent
            )

    ################################################################################################
    ################################################################################################

    # component rendering function for sub_content
    def render_sub_contents(
        self, parent_g, content_data_with_subs, parent_circle_props
    ):
        """
        render an SVG elements for a graphical representation of sub_content items.

        Variables:
            parent_g (SVG element): The parent group element that will contain the rendered sub-contents.
            content_data_with_subs (dict): A dictionary containing the sub-content items, where each key is a sub-content item's name and the value is a list of its sub-content items (if any).
            parent_circle_props (dict): A dictionary containing properties of the parent circle (e.g., radius, angle).

        """
        name, sub_contents_list = list(content_data_with_subs.items())[0]
        ##print("### -> ",sub_contents_list)
        if not sub_contents_list:
            return

        sub_radius = (
            parent_circle_props["radius"]
            + self.SLICE_CONSTANTS["innerCircle"]["subContentRadiusOffset"]
        )

        start_coords = self.polar_to_cartesian(
            self.CURRENT_CENTER,
            self.CURRENT_CENTER,
            parent_circle_props["radius"],
            parent_circle_props["angle"],
        )
        end_coords = self.polar_to_cartesian(
            self.CURRENT_CENTER,
            self.CURRENT_CENTER,
            sub_radius,
            parent_circle_props["angle"],
        )

        # Line connecting to sub-contents
        line_el = self.create_element(
            "line",
            {
                "x1": str(start_coords["x"]),
                "y1": str(start_coords["y"]),
                "x2": str(end_coords["x"]),
                "y2": str(end_coords["y"]),
                "stroke": self.COLORS["neutral"],
                "stroke-width": "1",
                "opacity": "0.5",
                # Simplified: no gradient
            },
        )
        parent_g.append(line_el)

        total_gap_offset = (
            len(sub_contents_list) - (len(sub_contents_list) % 2)
        ) * self.SLICE_CONSTANTS["innerCircle"]["subContentGap"]

        for i, sub_name in enumerate(sub_contents_list):
            gap_offset = self.SLICE_CONSTANTS["innerCircle"]["subContentGap"] * i
            angle_offset = gap_offset - total_gap_offset / 2
            sub_angle = parent_circle_props["angle"] + angle_offset
            sub_circle_props = {
                **parent_circle_props,
                "radius": sub_radius,
                "angle": sub_angle,
                "contentRadius": parent_circle_props.get(
                    "subContentRadius",
                    self.SLICE_CONSTANTS["innerCircle"]["subContentRadius"],
                ),
            }

            self.render_content(
                parent_g,
                sub_name,
                sub_circle_props,
                is_sub_content=True,
                content_name=None,
            )

    #####################################################################################################################################################
    #####################################################################################################################################################

    # component rendering function for arc
    def render_arc(
        self, parent_group, section_data, circle_config_from_parent, index, id_prefix
    ):
        """
        render an SVG elements for a graphical representation of an arc.

        Variables:
            parent_group (SVG element): The parent group element that will contain the rendered arc.
            section_data (dict): A dictionary containing the arc's data, where each key is a property
            circle_config_from_parent (dict): A dictionary containing properties of the parent circle
            index (int): The index of the arc in the parent circle's arcs list
            id_prefix (str): A prefix for the arc's id.
        """

        arc_id = f"{id_prefix}-arc-{index + 1}"
        arc_g = self.create_element("g", {"id": arc_id})
        parent_group.append(arc_g)

        arc_coords_data = self.get_arc_coords(
            center_coords={"x": self.CURRENT_CENTER, "y": self.CURRENT_CENTER},
            radius=circle_config_from_parent["radius"],
            arcs_types=circle_config_from_parent["arcs"],  # list of 'slice' or 'line'
            index=index,
            gap=circle_config_from_parent.get("gap", 0),
            ref_arc=circle_config_from_parent.get("refArc"),
        )

        contents = section_data.get("contents", [])
        single_content = len(contents) == 1

        if not single_content:
            path_el = self.create_element(
                "path",
                {
                    "d": arc_coords_data["path"],
                    "fill": "none",
                    "stroke": self.COLORS["grey"],
                    "stroke-width": "0.25",
                },
            )
            arc_g.append(path_el)

        section_name_data = section_data.get("name", {})
        if not section_name_data.get("hidden", False) and section_name_data.get("text"):
            text_path_id = f"{arc_id}-text-path"
            # Pass necessary config for TextPath from circle_config_from_parent
            text_path_circle_params = {
                **circle_config_from_parent,
            }
            self.render_text_path(
                arc_g,
                section_name_data["text"],
                text_path_id,
                index,
                text_path_circle_params,
            )

        # Distribute contents
        chunk_divider = len(contents) - (0 if arc_coords_data["fullCircle"] else 1)
        if chunk_divider <= 0:
            chunk_divider = 1  # Avoid division by zero for single items

        # Ensure angles are within a consistent range (e.g. 0-360 or -180 to 180) for proper calculation
        start_angle_norm = arc_coords_data["start"]["angle"] % 360
        end_angle_norm = arc_coords_data["end"]["angle"] % 360
        if (
            end_angle_norm < start_angle_norm and not arc_coords_data["fullCircle"]
        ):  # handles wrap around 360
            # this happens if arc crosses the 0/360 degree line
            if (
                abs(end_angle_norm - start_angle_norm) > 180
            ):  # Large arc likely means it crossed 0
                end_angle_norm += 360

        arc_angle_length = end_angle_norm - start_angle_norm
        if arc_coords_data["fullCircle"]:
            arc_angle_length = 360

        chunk_angle = arc_angle_length / chunk_divider if chunk_divider > 0 else 0

        for i, content_item in enumerate(contents):
            content_angle = (
                arc_coords_data["middle"]["angle"]
                if single_content
                else (start_angle_norm + chunk_angle * i)
            )

            content_circle_props = {
                "radius": circle_config_from_parent[
                    "radius"
                ],  # Content sits on the main arc radius
                "angle": content_angle,
                "contentRadius": circle_config_from_parent.get("contentRadius", 5),
                "contentNameOffset": circle_config_from_parent.get(
                    "contentNameOffset", 34
                ),
                # Potentially more from circle_config_from_parent if needed by render_content
            }
            # Pass object_attrs if available for content_item
            self.render_content(arc_g, content_item, content_circle_props)

    ###############################################################################################################################
    ###############################################################################################################################

    # component rendering function for slice
    def render_slice(self, parent_group, slice_data, index, all_sections_types):
        """
        render an SVG elements for a graphical representation of a slice.
        variables:

        """
        # slice_data: { name, innerArc, outerArcs, entryPoint }

        slice_id = f"slice-{index + 1}"
        slice_g = self.create_element("g", {"id": slice_id})
        parent_group.append(slice_g)

        slice_name_data = slice_data.get("name", {})
        if not slice_name_data.get("hidden", False) and slice_name_data.get("text"):
            text_path_id = f"{slice_id}-text-path"
            # For slice name, use SLICE_CONSTANTS.textCircle
            text_circle_params = {
                **self.SLICE_CONSTANTS["textCircle"],
                "arcs": all_sections_types,
            }
            self.render_text_path(
                slice_g,
                slice_name_data["text"],
                text_path_id,
                index,
                text_circle_params,
            )

        # Entry Point
        entry_point_key = slice_data.get("entryPoint")
        if entry_point_key:
            # Calculate outerArcCoords for entry point angle
            outer_arc_coords_for_entry = self.get_arc_coords(
                center_coords={"x": self.CURRENT_CENTER, "y": self.CURRENT_CENTER},
                radius=self.SLICE_CONSTANTS["outerCircle"][
                    "radius"
                ],  # JS uses SLICE.outerCircle.radius
                arcs_types=all_sections_types,
                gap=self.SLICE_CONSTANTS["outerCircle"]["gap"],
                index=index,
            )
            entry_point_circle_props = {
                **self.SLICE_CONSTANTS["entryPointCircle"],
                "angle": outer_arc_coords_for_entry["middle"]["angle"],
            }
            self.render_content(
                slice_g,
                entry_point_key,
                entry_point_circle_props,
                object_attrs={"type": "piscine"},
            )

        # Inner Arc
        inner_arc_data = slice_data.get("innerArc")
        if inner_arc_data:
            inner_arc_circle_config = {
                **self.SLICE_CONSTANTS["innerCircle"],
                "arcs": all_sections_types,
            }
            # The 'index' for this arc within the slice is effectively the slice's index itself
            self.render_arc(
                slice_g,
                inner_arc_data,
                inner_arc_circle_config,
                index,
                f"{slice_id}-inner",
            )

        # Outer Arcs
        outer_arcs_data = slice_data.get("outerArcs", [])
        if outer_arcs_data:
            outer_arcs_types = ["slice"] * len(
                outer_arcs_data
            )  # Outer arcs within a slice are always 'slice' type relative to each other

            # Calculate reference arc for these outer arcs based on the slice's position
            slice_outer_coords = self.get_arc_coords(
                center_coords={"x": self.CURRENT_CENTER, "y": self.CURRENT_CENTER},
                radius=self.SLICE_CONSTANTS["outerArc"]["radius"],
                arcs_types=all_sections_types,
                gap=self.SLICE_CONSTANTS["textCircle"]["gap"],
                index=index,
            )

            ref_arc_for_outer_arcs = {
                "startAngle": slice_outer_coords["start"]["angle"],
                "endAngle": slice_outer_coords["end"]["angle"],
            }
            # Adjust refArc if only one main section (full circle span for slice)
            if len(all_sections_types) == 1:
                ref_arc_for_outer_arcs = {
                    "startAngle": self.SLICE_CONSTANTS["outerArc"]["gap"] / 2,
                    "endAngle": 360 - self.SLICE_CONSTANTS["outerArc"]["gap"] / 2,
                }

            for arc_idx, arc_data in enumerate(outer_arcs_data):
                outer_arc_circle_config = {
                    **self.SLICE_CONSTANTS["outerArc"],
                    "arcs": outer_arcs_types,
                    "refArc": ref_arc_for_outer_arcs,
                }
                self.render_arc(
                    slice_g,
                    arc_data,
                    outer_arc_circle_config,
                    arc_idx,
                    f"{slice_id}-outer",
                )

    ########################################################################################################################################################################
    ########################################################################################################################################################################

    def render_line_section(self, parent_group, line_data, index, all_sections_types):
        # line_data: { name, contents }
        line_id = f"line-{index + 1}"
        line_g = self.create_element("g", {"id": line_id})
        parent_group.append(line_g)

        # Determine line's angle based on its position among all sections
        arc_coords_for_line_angle = self.get_arc_coords(
            center_coords={"x": self.CURRENT_CENTER, "y": self.CURRENT_CENTER},
            radius=self.SLICE_CONSTANTS["innerCircle"][
                "radius"
            ],  # Radius reference from JS for angle
            arcs_types=all_sections_types,
            gap=self.SLICE_CONSTANTS["innerCircle"]["gap"],
            index=index,
        )
        line_angle = arc_coords_for_line_angle["start"][
            "angle"
        ]  # Use start angle for line orientation

        start_coords = self.polar_to_cartesian(
            self.CURRENT_CENTER,
            self.CURRENT_CENTER,
            self.LINE_CONSTANTS["startRadius"],
            line_angle,
        )
        end_coords = self.polar_to_cartesian(
            self.CURRENT_CENTER,
            self.CURRENT_CENTER,
            self.LINE_CONSTANTS["endRadius"],
            line_angle,
        )

        # Line element (simplified, no gradient for now)
        line_el = self.create_element(
            "line",
            {
                "x1": str(start_coords["x"]),
                "y1": str(start_coords["y"]),
                "x2": str(end_coords["x"]),
                "y2": str(end_coords["y"]),
                "stroke": self.COLORS["neutral"],
                "stroke-width": "1",
                "opacity": "0.5",
            },
        )
        line_g.append(line_el)

        # Text title
        line_name_data = line_data.get("name", {})
        if not line_name_data.get("hidden", False) and line_name_data.get("text"):
            on_circle_right_side = 0 <= line_angle < 180
            text_rotation = line_angle + (-90 if on_circle_right_side else 90)
            text_anchor = "end" if on_circle_right_side else "start"

            text_el = self.create_element(
                "text",
                {
                    "x": str(start_coords["x"]),
                    "y": str(start_coords["y"]),
                    "font-size": "21px",
                    "fill": self.COLORS["neutral"],
                    "font-family": "IBM Plex Mono",
                    "alignment-baseline": "middle",
                    "text-anchor": text_anchor,
                    "transform": f"rotate({text_rotation} {start_coords['x']} {start_coords['y']})",
                },
                text_content=line_name_data["text"],
            )
            line_g.append(text_el)

        # Contents along the line
        contents = line_data.get("contents", [])
        line_offset_for_content = (
            0
            if line_name_data.get("hidden", True)
            else self.LINE_CONSTANTS["startOffset"]
        )
        line_length_for_content = (
            self.LINE_CONSTANTS["endRadius"]
            - self.LINE_CONSTANTS["startRadius"]
            - line_offset_for_content
        )

        num_contents = len(contents)
        chunk_length = (
            line_length_for_content / (num_contents - 1) if num_contents > 1 else 0
        )

        for i, content_item in enumerate(contents):
            radius_for_content = (
                self.LINE_CONSTANTS["endRadius"]
                if num_contents == 1
                else self.LINE_CONSTANTS["startRadius"]
                + line_offset_for_content
                + chunk_length * i
            )
            content_circle_props = {
                "radius": radius_for_content,
                "angle": line_angle,
                "contentRadius": self.SLICE_CONSTANTS["innerCircle"][
                    "contentRadius"
                ],  # Example from inner circle
                "contentNameOffset": self.SLICE_CONSTANTS["innerCircle"][
                    "contentNameOffset"
                ],
            }
            self.render_content(line_g, content_item, content_circle_props)

    ###############################################################################################################################
    ###############################################################################################################################

    # main rendering function for circular map 01
    def render_circular_map01(self, graph_data):    

        graph_attr = graph_data.get("graph", {})
        if not graph_attr:
            return None
        # Determine SVG_SIZE and CENTER
        svg_size = 2300 if graph_attr.get("outerCircle") else 2000
        self.CURRENT_CENTER = svg_size / 2

        # CORRECTED: Removed explicit xmlns and xmlns:xlink from attributes here
        root = self.create_element(
            "svg",
            {
                "style": "max-width: 1500px; display: block; margin: 0 auto; ",  # Added bg for visibility
                # "xmlns": SVG_NS, # REMOVED
                # "xmlns:xlink": XLINK_NS, # REMOVED - create_element handles namespacing the tag, ET.tostring handles declaring the namespace
                "viewBox": f"0 0 {svg_size} {svg_size}",
                "fill": "none",
            },
        )
        root.append(self.create_element("title", text_content="Module graph"))
        self.defs = self.create_element("defs")
        root.append(self.defs)

        # Central Point
        central_point_key = graph_attr.get("centralPoint")
        if central_point_key:
            # Ensure object_attrs for central_point_key if its type needs to be specific
            # Based on PDF, central point for "01 curriculums" is a "repeating checkpoint"
            # Based on JS, this would be type: 'exam'
            cp_attrs = {
                "type": "exam"
            }  # Defaulting to exam type as per JS 'Checkpoint' icon
            # Ensure the central point's circle properties are passed correctly
            cp_circle_props = {
                "radius": self.SLICE_CONSTANTS["centralPointCircle"]["radius"],
                "angle": self.SLICE_CONSTANTS["centralPointCircle"]["angle"],
                "contentRadius": self.SLICE_CONSTANTS["centralPointCircle"][
                    "contentRadius"
                ],
                # Add other necessary props if render_content expects them, e.g., contentNameOffset
                "contentNameOffset": self.SLICE_CONSTANTS["centralPointCircle"].get(
                    "contentNameOffset", 34
                ),
            }
            self.render_content(
                root, central_point_key, cp_circle_props, object_attrs=cp_attrs
            )

        # Inner Circle
        inner_circle_sections = graph_attr.get("innerCircle", [])
        if inner_circle_sections:
            inner_g = self.create_element("g", {"id": "inner-circle"})
            root.append(inner_g)
            sections_types = [s.get("type", "slice") for s in inner_circle_sections]
            for i, section in enumerate(inner_circle_sections):
                if section.get("type") == "slice":
                    self.render_slice(inner_g, section, i, sections_types)
                elif section.get("type") == "line":
                    self.render_line_section(inner_g, section, i, sections_types)

        # Middle Circle
        middle_circle_sections = graph_attr.get("middleCircle", [])
        if middle_circle_sections:
            middle_g = self.create_element("g", {"id": "middle-circle"})
            root.append(middle_g)
            middle_sections_types = ["slice"] * len(middle_circle_sections)
            middle_circle_config = {
                **self.MIDDLE_CIRCLE_CONSTANTS,
                "arcs": middle_sections_types,
            }
            for i, section in enumerate(middle_circle_sections):
                self.render_arc(
                    middle_g, section, middle_circle_config, i, "middle-circle"
                )

        # Outer Circle
        outer_circle_sections = graph_attr.get("outerCircle", [])
        if outer_circle_sections:
            outer_g = self.create_element("g", {"id": "outer-circle"})
            root.append(outer_g)
            outer_sections_types = ["slice"] * len(outer_circle_sections)
            outer_circle_config = {
                **self.OUTER_CIRCLE_CONSTANTS,
                "arcs": outer_sections_types,
            }
            for i, section in enumerate(outer_circle_sections):
                self.render_arc(
                    outer_g, section, outer_circle_config, i, "outer-circle"
                )

        # Info Card
        root.append(self.generate_info_card())

        #Add filter
        """
        <filter color-interpolation-filters="sRGB" filterunits="userSpaceOnUse" height="63" id="filter7_f_1_272"
                width="65" x="855" y="994">
                <feflood flood-opacity="0" result="BackgroundImageFix"></feflood>
                <feblend in="SourceGraphic" in2="BackgroundImageFix" mode="normal" result="shape"></feblend>
                <fegaussianblur result="effect1_foregroundBlur_1_272" stddeviation="8.5"></fegaussianblur>
            </filter>"""
        filter = self.create_element(
            "filter",
            {
                "color-interpolation-filters": "sRGB",
                "filterunits": "userSpaceOnUse",
                "height": "63",
                "id": "filter7_f_1_272",
                "width": "65",
                "x": "855",
                "y": "994",
            },
        )

        self.defs.append(filter)
        filter.append(
            self.create_element(
                "feflood", {"flood-opacity": "0", "result": "BackgroundImageFix"}
            )
        )
        filter.append(
            self.create_element(
                "feblend",
                {
                    "in": "SourceGraphic",
                    "in2": "BackgroundImageFix",
                    "mode": "normal",
                    "result": "shape",
                },
            )
        )
        filter.append(
            self.create_element(
                "fegaussianblur",
                {"result": "effect1_foregroundBlur_1_272", "stddeviation": "8.5"},
            )
        )
        return root, ET2.tostring(root, encoding="unicode")
    
    ###############################################################################################################################
    ###############################################################################################################################
    # main function to generate info card
    def generate_info_card(self) -> ET2.Element:
        if self.kind == "distribution":
            return self.generate_distribution_info_card()
        elif self.kind == "classic":
            return self.generate_classic_info_card()
        else:
            print(f"Unknown kind '{self.kind}' for info card generation.")
            return None

    ###############################################################################################################################
    ###############################################################################################################################
    # component generation function for info card (type=classic)
    def generate_classic_info_card(self) -> ET2.Element:
                
        """<g id="info_card">
            <g filter="url(#filter8_d_1_272)" id="card">
                <rect fill="#9C9797" height="69" id="card_a" rx="5" width="110" x="722" y="651"></rect>
                <rect height="card_heiht" id="card_b" rx="4.5" stroke="#656464" width="card_width" x="722.5" y="651.5"></rect>
            </g> 
            
            <text fill="white" font-family="Inter" font-size="12" font-weight="800" letter-spacing="0em" style="white-space: pre" xml:space="preserve">
                <tspan id="project_name_card" x="737.535" y="666.864">project name</tspan>
            </text> 
            <text fill="white" font-family="Inter" font-size="12" font-weight="800" letter-spacing="0em" style="white-space: pre" xml:space="preserve">
                <tspan id="data_card" x="753.35" y="699.364">number</tspan>
            </text>
        </g>"""
        card_width = 150
        card_height = 100
        info_card = self.create_element(
            "g",
            {
                "id": "info_card",
                "filter": "url(#filter8_d_1_272)",
                "style": "visibility: hidden;",
            },
        )
        card = self.create_element("g", {"id": "card"})
        info_card.append(card)
        card_a = self.create_element(
            "rect",
            {
                "fill": "#66696992",
                "height": card_height,
                "id": "card_a",
                "rx": "5",
                "width": card_width,
                "x": "722.5",
                "y": "651.5",
            },
        )
        card.append(card_a)
        card_b = self.create_element(
            "rect",
            {
                "fill": "#21212188",
                "height": card_height,
                "id": "card_b",
                "rx": "4.5",
                "stroke": "#656464",
                "width": card_width,
                "x": "722.5",
                "y": "651.5",
            },
        )
        card.append(card_b)
        text1 = self.create_element(
            "text",
            {
                "fill": "white",
                "font-family": "Inter",
                "font-size": "20",
                "font-weight": "800",
                "letter-spacing": "0em",
                "style": "white-space: pre",
                "xml:space": "preserve",
            },
        )
        info_card.append(text1)
        project_name_card = self.create_element(
            "tspan",
            {"id": "project_name_card", "x": "737.535", "y": "666.864"},
            text_content="project name",
        )
        text1.append(project_name_card)
        text2 = self.create_element(
            "text",
            {
                "fill": "white",
                "font-family": "Inter",
                "font-size": "24",
                "font-weight": "800",
                "letter-spacing": "0em",
                "style": "white-space: pre",
                "xml:space": "preserve",
            },
        )
        info_card.append(text2)
        data_card = self.create_element(
            "tspan", {"id": "data_card", "x": "753.35", "y": "699.364"}
        )
        text2.append(data_card)

        return info_card

    ###############################################################################################################################
    ###############################################################################################################################
    # component generation function for info card (type=distribution)
    def generate_distribution_info_card(self) -> ET2.Element:

        card_width = 200
        card_height = 290
        info_card = self.create_element(
            "g",
            {
                "id": "info_card",
                "filter": "url(#filter8_d_1_272)",
                "style": "visibility: hidden;",
            },
        )
        #root.append(info_card)
        card = self.create_element("g", {"id": "card"})
        info_card.append(card)
        card_a = self.create_element(
            "rect",
            {
                "fill": "#66696992",
                "height": card_height,
                "id": "card_a",
                "rx": "5",
                "width": card_width,
                "x": "722.5",
                "y": "651.5",
            },
        )
        card.append(card_a)
        card_b = self.create_element(
            "rect",
            {
                "fill": "#21212188",
                "height": card_height,
                "id": "card_b",
                "rx": "4.5",
                "stroke": "#656464",
                "width": card_width,
                "x": "722.5",
                "y": "651.5",
            },
        )
        card.append(card_b)
        text1 = self.create_element(
            "text",
            {
                "fill": "white",
                "font-family": "Inter",
                "font-size": "20",
                "font-weight": "800",
                "letter-spacing": "0em",
                "style": "white-space: pre",
                "xml:space": "preserve",
            },
        )
        info_card.append(text1)
        project_name_card = self.create_element(
            "tspan",
            {"id": "project_name_card", "x": "737.535", "y": "666.864"},
            text_content="project name",
        )
        text1.append(project_name_card)
        text2 = self.create_element(
            "text",
            {
                "fill": "white",
                "font-family": "Inter",
                "font-size": "24",
                "font-weight": "800",
                "letter-spacing": "0em",
                "style": "white-space: pre",
                "xml:space": "preserve",
            },
        )
        info_card.append(text2)
        data_card = self.create_element(
            "tspan", {"id": "data_card", "x": "753.35", "y": "699.364"}
        )
        text2.append(data_card)

        return info_card


    ###############################################################################################################################
    ###############################################################################################################################
    # component rendering gradient legend
    def display_gradient_legend(
        self, start_color_hex, mid_color_hex, end_color_hex, min_val, max_val
    ):
        """
        Display a gradient legend .

        Variables:
            start_color_hex (str): Hex code for the start color of the gradient.
            mid_color_hex (str): Hex code for the middle color of the gradient.
            end_color_hex (str): Hex code for the end color of the gradient.
            min_val (int or float): Minimum value for the gradient scale.
            max_val (int or float): Maximum value for the gradient scale.
        """
        create_gradient_html(
            start_color_hex, mid_color_hex, end_color_hex, min_val, max_val
        )

    ###############################################################################################################################
    ###############################################################################################################################
    # component display graph visualization
    def show(self):
        """
        Display the SVG graph visualization.
        """
        if not self.graph_svg_text:
            print("No SVG data to display.")
            return
        display(HTML(self.graph_svg_text))
