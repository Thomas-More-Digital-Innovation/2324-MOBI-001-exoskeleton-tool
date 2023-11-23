@app.route("/exolist")
def exolist():
    # Filters
    active_passive_filter = request.args.get("active_passive")
    manufacturer_filter = request.args.getlist("manufacturer")
    material_filter = request.args.get("material")
    one_two_sided_filter = request.args.get("one_two_sided")
    search_query = request.args.get("search_query")
    compact_filter = request.args.get("compact")
    print(compact_filter)

    # Base query for fetching exoskeletons
    base_query = """
    MATCH (e:Exo)
    OPTIONAL MATCH (e)-[r1:HAS_AS_MAIN_DOF]-(d:Dof)-[r2:HAS_DOF]-(j:JointT)
    WITH e, COLLECT(DISTINCT j.jointTName) AS joints
    """

    where_conditions = []

    # Add filter conditions to the query
    if active_passive_filter:
        where_conditions.append(f"e.exoActivePassive = '{active_passive_filter}'")

    if manufacturer_filter:
        manufacturer_conditions = [f"e.exoManufacturer = '{mf}'" for mf in manufacturer_filter]
        where_conditions.append("(" + " OR ".join(manufacturer_conditions) + ")")

    if material_filter:
        where_conditions.append(f"e.exoMaterial = '{material_filter}'")

    if one_two_sided_filter:
        where_conditions.append(f"e.exoOneTwoSided = '{one_two_sided_filter}'")

    if search_query:
        where_conditions.append(f"toLower(e.exoName) CONTAINS toLower('{search_query}')")

    if compact_filter:
        where_conditions.append(f"(e)-[:HAS_PROPERTY {{property: 'compact', value: '{compact_filter}'}}]-()")

    # Construct the WHERE clause
    where_clause = " WHERE " + " AND ".join(where_conditions) if where_conditions else ""

    # Build the complete query for fetching exoskeletons
    full_query = f"{base_query}{where_clause} RETURN e.exoId AS id, e.exoName AS Name, joints AS Joint, " \
                f"e.exoActivePassive AS ActivePassive, e.exoManufacturer AS Manufacturer, e.exoMaterial AS Material, " \
                f"e.exoOneTwoSided AS OneTwoSided, e.exoDescription AS Description ORDER BY Name"

    # Properties query for fetching property values
    properties_query = """
        MATCH (ep:ExoProperty)-[r:HAS_PROPERTY]-(e:Exo)
        WHERE r.exoPropertyValue IN ['ja', 'nee']
        RETURN e.exoId AS exoId, COLLECT({property: ep.exoPropertyName, value: r.exoPropertyValue}) AS propertyValues
    """

    # Fetch data from Neo4j
    all_exoskeletons = g.run(full_query).data()
    properties_data = g.run(properties_query).data()

    # Create a dictionary to store properties for each exoskeleton
    properties_dict = {data['exoId']: data['propertyValues'] for data in properties_data}

    # Render the template and pass the data
    return render_template(
        "exolist.html",
        exoskeletons=all_exoskeletons,
        properties_dict=properties_dict,
        active_passive_filter=active_passive_filter,
        manufacturer_filter=manufacturer_filter,
        material_filter=material_filter,
        one_two_sided_filter=one_two_sided_filter,
        compact_filter = compact_filter,
    )