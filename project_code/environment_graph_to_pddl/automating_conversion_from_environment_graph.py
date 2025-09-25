def envgraph_to_pddl(env_graph, problem_name="env_problem"):
    """
    Convert a VirtualHome EnvironmentGraph into a PDDL problem definition
    fully compatible with the 'household' domain. Guaranteed to avoid type recursion.

    Args:
        env_graph (dict): A VirtualHome environment graph containing 'nodes' and 'edges'.
            - nodes: list of objects in the environment, each with id, class_name, category, and states.
            - edges: list of relationships between objects, each with from_id, to_id, and relation_type.
        problem_name (str): Name of the generated PDDL problem.

    Returns:
        str: A string representing the PDDL problem definition.
    """
    nodes = env_graph["nodes"]
    edges = env_graph["edges"]

    # Safe mapping of categories to domain types
    category_map = {
        "character": "character",
        "person": "character",
        "room": "room",
        "object": "object",
        "container": "container",
        "furniture": "furniture"
    }

    objects = []
    init = []

    # Keep track of object names to avoid name/type conflicts
    used_names = set()

    def make_safe_name(name, id_):
        """Generate a safe object name that cannot conflict with type names"""
        safe_name = f"{name.lower()}_{id_}"
        while safe_name in used_names:
            safe_name += "_x"
        used_names.add(safe_name)
        return safe_name

    # Process nodes
    for node in nodes:
        raw_category = node.get("category", "object").strip().lower()
        obj_type = category_map.get(raw_category, "object")
        obj_name = make_safe_name(node.get("class_name", "obj"), node["id"])
        objects.append(f"{obj_name} - {obj_type}")

        # Add states
        for state in node.get("states", []):
            state_upper = state.upper()
            if state_upper == "OPEN":
                init.append(f"(open {obj_name})")
            elif state_upper == "CLOSED":
                init.append(f"(closed {obj_name})")
            elif state_upper == "ON":
                init.append(f"(on_state {obj_name})")
            elif state_upper == "OFF":
                init.append(f"(off_state {obj_name})")

    # Process edges
    for edge in edges:
        from_node = next(n for n in nodes if n["id"] == edge["from_id"])
        to_node = next(n for n in nodes if n["id"] == edge["to_id"])

        from_name = make_safe_name(from_node.get("class_name", "obj"), from_node["id"])
        to_name = make_safe_name(to_node.get("class_name", "obj"), to_node["id"])

        from_type = category_map.get(from_node.get("category", "object").strip().lower(), "object")
        to_type = category_map.get(to_node.get("category", "object").strip().lower(), "object")
        rel_type = edge["relation_type"].lower()

        if rel_type == "inside":
            if to_type == "room":
                init.append(f"(in {from_name} {to_name})")
            else:
                init.append(f"(at {from_name} {to_name})")
        elif rel_type == "on" and to_type in ["object", "container", "furniture"]:
            init.append(f"(on {from_name} {to_name})")
        elif rel_type == "close" and from_type == "character" and to_type in ["object", "container", "furniture"]:
            init.append(f"(close_char_object {from_name} {to_name})")
        elif rel_type == "facing":
            init.append(f"(facing {from_name} {to_name})")
        elif rel_type == "sitting" and from_type == "character" and to_type in ["object", "container", "furniture"]:
            init.append(f"(sitting {from_name} {to_name})")
        elif rel_type == "holds_rh" and to_type in ["object", "container", "furniture"]:
            init.append(f"(holding_rh {from_name} {to_name})")
        elif rel_type == "holds_lh" and to_type in ["object", "container", "furniture"]:
            init.append(f"(holding_lh {from_name} {to_name})")

    # Assemble PDDL
    objects_str = "\n    ".join(objects)
    init_str = "\n    ".join(init)

    pddl_problem = f"""
(define (problem {problem_name})
  (:domain household)

  (:objects
    {objects_str}
  )

  (:init
    {init_str}
  )

  (:goal
    ;; Define your goal here; update as needed
      (inside apple_3 fridge_2)
  )
)
"""
    return pddl_problem



# Example usage
def main():
    example_env = {
        "nodes": [
            {"id": 1, "class_name": "character", "category": "Person", "states": []},
            {"id": 2, "class_name": "kitchen", "category": "Room", "states": []},
            {"id": 3, "class_name": "fridge", "category": "Container", "states": ["CLOSED"]},
            {"id": 4, "class_name": "cup", "category": "Object", "states": []}
        ],
        "edges": [
            {"from_id": 1, "to_id": 2, "relation_type": "INSIDE"},
            {"from_id": 4, "to_id": 3, "relation_type": "INSIDE"},
            {"from_id": 1, "to_id": 4, "relation_type": "CLOSE"},
        ]
    }

    pddl_output = envgraph_to_pddl(example_env, problem_name="example_env_problem")
    print(pddl_output)


if __name__ == "__main__":
    main()


def main():
    """
    Example usage of envgraph_to_pddl function.
    Creates a small environment graph and converts it to PDDL.
    """

    # Example EnvironmentGraph
    example_env = {
        "nodes": [
            {"id": 1, "class_name": "character", "category": "Person", "states": []},
            {"id": 2, "class_name": "kitchen", "category": "Room", "states": []},
            {"id": 3, "class_name": "fridge", "category": "Container", "states": ["CLOSED"]},
            {"id": 4, "class_name": "cup", "category": "Object", "states": []}
        ],
        "edges": [
            {"from_id": 1, "to_id": 2, "relation_type": "INSIDE"},
            {"from_id": 4, "to_id": 3, "relation_type": "INSIDE"},
        ]
    }

    # Convert environment to PDDL
    pddl_output = envgraph_to_pddl(example_env, problem_name="example_env_problem")

    # Print the generated PDDL
    print(pddl_output)


if __name__ == "__main__":
    main()
