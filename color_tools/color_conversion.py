
import re 
def hex_to_rgb2(hex_color):
    """Convert a hex color to an RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

def rgb_to_hex2(rgb):
    """Convert an RGB tuple to a hex color."""
    return '#{:02x}{:02x}{:02x}'.format(*rgb)


def is_valid_hex_color_2(color_string):
    """Checks if a string is a valid 3 or 6 digit hex color code."""
    if not isinstance(color_string, str):
        return False
    # Regex for # followed by 3 or 6 hex characters
    match = re.fullmatch(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', color_string)
    return bool(match)


def interpolate_color(value, max_value, start_color, mid_color, end_color):
    from .color_conversion import hex_to_rgb2, rgb_to_hex2
    """
    Interpolate between three colors based on value.

    :param value: The input value to map to a color.
    :param max_value: The maximum possible value.
    :param start_color: Color corresponding to 0% (e.g., red).
    :param mid_color: Color corresponding to 50% (e.g., yellow).
    :param end_color: Color corresponding to 100% (e.g., green).
    :return: A hex color code.
    """
    # Ensure value is within bounds
    value = max(0, min(value, max_value))
    ratio = value / max_value

    # Choose the right range for interpolation (either start->mid or mid->end)
    if ratio <= 0.5:
        # Interpolating between start_color and mid_color
        start = hex_to_rgb2(start_color)
        end = hex_to_rgb2(mid_color)
        interp_ratio = ratio * 2  # Scale to 0-1
    else:
        # Interpolating between mid_color and end_color
        start = hex_to_rgb2(mid_color)
        end = hex_to_rgb2(end_color)
        interp_ratio = (ratio - 0.5) * 2  # Scale to 0-1

    # Calculate interpolated RGB values
    interpolated = tuple(
        int(start[i] + (end[i] - start[i]) * interp_ratio) for i in range(3)
    )

    # Convert back to hex and return
    return rgb_to_hex2(interpolated)


def value_to_color(value, max_value, gradient_colors=None):
    """Map a numeric value to a color on a gradient defined by three colors."""
    start_color = '#FFD700'  #yellow
    mid_color = '#32CD32'    #yellow blue
    end_color = '#1E90FF' 
    if gradient_colors and len(gradient_colors) == 3:
        start_color, mid_color, end_color = gradient_colors    

    return interpolate_color(value,
                               max_value,
                                start_color,
                                  mid_color,
                                    end_color)
