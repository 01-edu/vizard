from typing import Literal


# Function to return the appropriate JS function based on the type of info card
def show_info_card(type: Literal["classic", "distribution"] = "classic") -> str:
    """
    Returns the appropriate JS function to display info cards based on the visualization type.

    Args:
        type (Literal["classic", "distribution"], optional): Type of visualization. Defaults to
        "classic".

    Returns:
        str: JavaScript function as a string.

    """

    if type == "classic":
        return show_classic_info_card()
    elif type == "distribution":
        return show_distribution_info_card()
    else:
        print("Invalid visualization type")


# JS function to display 'classic' informations dynamically (project name -> number)
def show_classic_info_card() -> str:
    """
    Returns a JavaScript function as a string to display classic info cards dynamically.
    The function updates the info card's position and content based on the element's attributes.
        Args:
            None
        Returns:
           str: JavaScript function as a string.
    """

    return """
    (function showInfoCard(el) { 
    el.style.cursor= "pointer";
    const infoCard = document.getElementById("info_card");
    const cardA = document.getElementById("card_a");
    const cardB = document.getElementById("card_b");
    const projectText = document.getElementById("project_name_card");
    const dataText = document.getElementById("data_card");
    const dataNumber = el.getAttribute("data-tooltip") || "0";
    /************************************************************/
    const card_a_x_shift = -54.0;
    const card_a_y_shift = -127.0;

    const card_b_x_shift = -53.5;
    const card_b_y_shift = -126.5;

    const project_text_x_shift = -38.46500000000003;
    const project_text_y_shift = -101.13599999999997;

    const data_text_x_shift = -22.649999999999977;
    const data_text_y_shift = -68.63599999999997;
    /************************************************************/
    const x = parseFloat(el.getAttribute("cx"));
    const y = parseFloat(el.getAttribute("cy"));
    const projectName = el.getAttribute("project-name") || el.getAttribute("id").toLowerCase();
    /***********************************************************/
    projectText.textContent = projectName;
    dataText.textContent = dataNumber;

    const projectTextWidth = projectText.getBBox().width; // width after rendering
    const card_width = parseFloat(cardA.getAttribute("data-width")) + projectTextWidth;
    const cardX = x + card_a_x_shift;
    const centeredX = cardX + (card_width - projectTextWidth) / 2;
    /***********************************************************/
    cardA.setAttribute("x", x + card_a_x_shift);
    cardA.setAttribute("y", y + card_a_y_shift);
    cardA.setAttribute("width", card_width + projectTextWidth) // calculation made to adapt on HEX

    cardB.setAttribute("x", x + card_b_x_shift);
    cardB.setAttribute("y", y + card_b_y_shift);
    cardB.setAttribute("width", card_width + projectTextWidth) // calculation made to adpat on HEX
    /***********************************************************/
    projectText.setAttribute("x", centeredX);
    projectText.setAttribute("y", y + project_text_y_shift);

    dataText.setAttribute("x", centeredX);
    dataText.setAttribute("y", y + data_text_y_shift);
    infoCard.style.visibility = "visible";
    })(this)
    """


# JS function to display distributions informations dynamically (project name -> min, q1, median, q3, max, outliers)
def show_distribution_info_card() -> str:
    """
    Returns a JavaScript function as a string to display distribution info cards dynamically.
    The function updates the info card's position and content based on the element's attributes.

    Args:
        None

    Returns:
        str: JavaScript function as a string.
    """

    return """
    (function showInfoCard(el) { 
    el.style.cursor= "pointer";
    const infoCard = document.getElementById("info_card");
    const cardA = document.getElementById("card_a");
    const cardB = document.getElementById("card_b");

    const projectText = document.getElementById("project_name_card");
    const dataText = document.getElementById("data_card");

    const datajson = el.getAttribute("data-tooltip") || "0";
    const data = datajson == "0" ? "N/A": JSON.parse(datajson);
    const sep = document.getElementById("separator");

    /*****************************/
    const card_a_x_shift = 1.0;
    const card_a_y_shift = -295.0;
    const card_b_x_shift = 1.5;
    const card_b_y_shift = -295.5;
    /***********************************************************/
    const project_text_x_shift = 60.46500000000003;
    const project_text_y_shift = -270.13599999999997;
    const text_x_shift = 10.649999999999977;
    const text_y_shift = -215.63599999999997;
    const text_y_margin = 28;

    /*******************************************/
    const x = parseFloat(el.getAttribute("cx"));
    const y = parseFloat(el.getAttribute("cy"));
    const projectName = el.getAttribute("project-name") || el.getAttribute("id").toLowerCase();
    console.log(x);
    console.log(y);
    /*********************************************/
    projectText.textContent = projectName;

    /*********************************************/
    const projectTextWidth = projectText.getBBox().width; // width after rendering
    const card_width = parseFloat(cardA.getAttribute("data-width")) + projectTextWidth
    const cardX = x + card_a_x_shift;
    const centeredX = cardX + (card_width - projectTextWidth) / 2;
 
    //*-------- Adding Statistical Data
    const ids  = ["max", "upperfence", "q3", "median", "q1", "lowerfence", "min", "outliers"];
    ids.forEach((value, index) => {
       const el = document.getElementById(value);
       el.textContent = data && data[value] !== undefined 
        ? `${value.charAt(0).toUpperCase() + value.slice(1)} : ${data[value]}` 
        : `${value.charAt(0).toUpperCase() + value.slice(1)} : N/A`;
 
        el.setAttribute("x", x + text_x_shift);
        el.setAttribute("y", y + text_y_shift + text_y_margin * index);

    });

    
    /***********************************************************/
    cardA.setAttribute("x", x + card_a_x_shift);
    cardA.setAttribute("y", y + card_a_y_shift);
    cardA.setAttribute("width", card_width + projectTextWidth) // calculation made to adapt on HEX

        
    cardB.setAttribute("x", x + card_b_x_shift);
    cardB.setAttribute("y", y + card_b_y_shift);
    cardB.setAttribute("width", card_width + projectTextWidth) // calculation made to adapt on HEX

    /***********************************************/
    projectText.setAttribute("x", centeredX);
    projectText.setAttribute("y", y + project_text_y_shift);

    sep.setAttribute("x1", x + 5);
    sep.setAttribute("y1", y + text_y_shift -30);
    sep.setAttribute("x2", x + cardA.getBBox().width);
    sep.setAttribute("y2", y + text_y_shift - 30);

    infoCard.style.visibility = "visible";
    })(this)
    """
