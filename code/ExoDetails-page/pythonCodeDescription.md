# Exoskeleton Details Flask Application

## `get_exoskeleton_by_id` Function

This function retrieves exoskeleton data by its unique identifier (`exo_id`).

### Parameters:
- **exo_id (int):** The unique identifier of the exoskeleton.

### Returns:
- **dict or None:** Exoskeleton data as a dictionary or `None` if not found.

### Code:

```python
def get_exoskeleton_by_id(exo_id):
    query = """
    MATCH (e:Exo {exoId: $exo_id})
    OPTIONAL MATCH (e)-[r1:HAS_AS_MAIN_DOF]-(d:Dof)-[r2:HAS_DOF]-(j:JointT)
    RETURN e, COLLECT(DISTINCT j.jointTName) AS joints
    """

    exoskeleton_data = g.run(query, exo_id=exo_id).data()

    if exoskeleton_data:
        exoskeleton = exoskeleton_data[0]['e']
        exoskeleton['joints'] = exoskeleton_data[0]['joints']
        return exoskeleton
    else:
        return None
```

## `exoskeleton_details` Route Handler
This route handler displays detailed information about a specific exoskeleton.

### parameters
* exo_id (int): The unique identifier of the exoskeleton.

### Returns: 
* HTML template rendering exoskeleton details.

### Code
```python 
@app.route("/exoskeleton/<int:exo_id>")
def exoskeleton_details(exo_id):
    exoskeleton = get_exoskeleton_by_id(exo_id)

    if exoskeleton:
        # Query for the joints of the exoskeleton
        joints_query = """
        MATCH (e:Exo {exoId: $exo_id})-[:HAS_AS_MAIN_DOF]-(d:Dof)-[:HAS_DOF]-(j:JointT)
        RETURN COLLECT(DISTINCT j.jointTName) AS joints
        """
        # Fetch data from Neo4j for joints
        joints_data = g.run(joints_query, exo_id=exo_id).data()
        # Extract the joints from the data
        joints = joints_data[0]['joints'] if joints_data else []

        # ... (similarly document other queries)

        return render_template(
            "exoskeleton_details.html",
            exoskeleton=exoskeleton,
            joints=joints,
            properties=properties,
            maingoals=maingoals,
            sidegoals=sidegoals,
            contraindications=contraindications,
            main_activities=main_activities,
            side_activities=side_activities,
            houdingsondersteuning_bij=houdingsondersteuning_bij,
            houdingsondersteuning_door=houdingsondersteuning_door,
            limiteert=limiteert,
            vergemakkelijkt=vergemakkelijkt,
            fromPart=fromPart,
            toPart=toPart,
            weerstand_bij=weerstand_bij,
            hindert=hindert,
        )
    else:
        return "Exoskeleton not found", 404
```

This Flask application uses Neo4j queries to fetch detailed information about exoskeletons and renders the data in an HTML template.

