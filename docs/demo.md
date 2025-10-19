# DEMO
---
**classic kind**
```python
from IPython.display import display
from IPython.display import HTML
from circular_graph.modular_graph import modular_graph
from circular_graph.tools.text_conversion import to_slug
import pandas as pd
import warnings

display(HTML("<style>.container { width:100% !important; }</style>"))

warnings.filterwarnings("ignore", category=UserWarning)

start_color_2 = "#FFD700"  # yellow
mid_color_2 = "#32CD32"  # yellow blue
end_color_2 = "#1E90FF"  # blue
FROM = 0
TO = 225
cohort_selector = ["2023-03", "2023-09", "2023-09", "2024-01"]
module_name = 100256
cohort_validation_and_time = pd.read_csv("datasets/cohort.csv")
module_graph = pd.read_csv("datasets/module_graph.csv")
piscines = pd.read_csv("datasets/piscines.csv")
checkpoints = pd.read_csv("datasets/checkpoint.csv")
mandatory_projects = pd.read_csv("datasets/mandatory_projects.csv")
object_path_name = pd.read_csv("datasets/object_path_name.csv")
project_path_dict = object_path_name.set_index("key")["path"].to_dict()
###############################################################################################################################
if FROM >= 0 and TO >= 0 and FROM <= TO:
    data_validation_time = (
        cohort_validation_and_time[
            (cohort_validation_and_time["joined_the_module"].isin(cohort_selector))
        ]
    )[
        (
            (cohort_validation_and_time["weeks"] >= FROM)
            & (cohort_validation_and_time["weeks"] <= TO)
        )
    ]
else:
    data_validation_time = cohort_validation_and_time[
        (cohort_validation_and_time["joined_the_module"].isin(cohort_selector))
    ]
###############################################################################################################################
data_validation_time = data_validation_time[
    (data_validation_time["module_id"] == module_name)
]
graph_json = module_graph[(module_graph["module_id"] == module_name)].iat[0, 4]
###############################################################################################################################
piscines_list = [to_slug(p, project_path_dict) for p in list(piscines["name"])]
checkpoints_list = [to_slug(c, project_path_dict) for c in list(checkpoints["name"])]
mandatory_list = [
    to_slug(p, project_path_dict) for p in list(mandatory_projects["name"])
]
###############################################################################################################################
if data_validation_time.empty:
    graph_object = modular_graph(
        graph_json, {}, piscines_list, checkpoints_list, mandatory_list
    )
    print(
        "NO DATA FOUND FOR COHORT : "
        + " and ".join(cohort_selector)
        + " IN THE MODULE : "
        + str(module_name)
    )
    graph_object.show()

else:
    unique_pairs_2 = data_validation_time.drop_duplicates(
        subset=["ob_key", "userId", "campusDomain"]
    )
    data_validation_time = (
        unique_pairs_2.groupby("ob_key").size().reset_index(name="number_of_users")
    )
    if len(list(module_graph["joined_the_module"])):
        print(
            "THIS CIRCULAR GRAPH IS REPRESENTING DATA FOR COHORT : "
            + " and ".join(list(module_graph["joined_the_module"]))
        )

    mapping_data_vis = data_validation_time.set_index("ob_key")[
        "number_of_users"
    ].to_dict()
    graph_object = modular_graph(
        graph_json, mapping_data_vis, piscines_list, checkpoints_list, mandatory_list
    )
    graph_object.display_gradient_legend(
        start_color_2,
        mid_color_2,
        end_color_2,
        min(mapping_data_vis.values()),
        max(mapping_data_vis.values()),
    )
    graph_object.show()
```
<img src="/images/sc_classic.png">

---
**Distribution kind**
```python
project_stats = pd.read_csv("datasets/project_stats.csv", index_col=[0]).set_index(
    "project_name"
)
project_stats_dict = {}
for i in project_stats.iterrows():
    project_stats_dict[i[0]] = i[1]

path_dict = object_path_name.set_index("key")["path"].to_dict()

graph_obj = modular_graph(
    graph_json,
    data=project_stats_dict,
    piscines_list=piscines_list,
    checkpoints_list=checkpoints_list,
    mandatory_list=mandatory_list,
    kind="distribution",
)
graph_obj.display_gradient_legend(
    start_color_2,
    mid_color_2,
    end_color_2,
    0,  # min value
    graph_obj.max_value,  # max value
)
graph_obj.show()
```
<img src="/images/sc_distribution.png">
