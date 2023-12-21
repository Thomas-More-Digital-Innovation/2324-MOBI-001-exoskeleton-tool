# Define a route for the '/exolist' endpoint
@app.route("/exolist")
def exolist():

    # Retrieve filter values from the session
    active_passive_filter = session.get('active_passive_filter')
    joint_filter = session.get('joint_filter')
    manufacturer_filter = session.get('manufacturer_filter')
    material_filter = session.get('material_filter')
    one_two_sided_filter = session.get('one_two_sided_filter')
    compact_filter = session.get('compact_filter')
    water_filter = session.get('water_filter')
    stof_filter = session.get('stof_filter')
    joint_filter = session.get('joint_filter')

    # Retrieve filter values from the request parameters
    active_passive_filter = request.args.get("active_passive")
    manufacturer_filter = request.args.getlist("manufacturer")
    material_filter = request.args.get("material")
    one_two_sided_filter = request.args.get("one_two_sided")
    search_query = request.args.get("search_query")
    compact_filter = request.args.get("compact")
    water_filter = request.args.get("waterbestendig")
    stof_filter = request.args.get("stofbestendig")
    joint_filter = request.args.getlist("joint")

    # Neo4j base query for exoskeleton data retrieval
    base_query = """
    MATCH (e:Exo)
    OPTIONAL MATCH (e)-[r1:HAS_AS_MAIN_DOF]-(d:Dof)-[r2:HAS_DOF]-(j:JointT)
    OPTIONAL MATCH (e)-[r:HAS_PROPERTY]-(ep:ExoProperty)
    WITH e, COLLECT(DISTINCT j.jointTName) AS joints, j, ep, r
    """

    # List to store WHERE conditions for the Neo4j query
    where_conditions = []
    # Add filter conditions to the query
    if active_passive_filter:
        where_conditions.append(f"e.exoActivePassive = '{active_passive_filter}'")
    if joint_filter:
        joint_conditions = [f"j.jointTName = '{joint}'" for joint in joint_filter]
        where_conditions.append("(" + " OR ".join(joint_conditions) + ")")
    if manufacturer_filter:
        manufacturer_conditions = [f"e.exoManufacturer = '{mf}'" for mf in manufacturer_filter]
        where_conditions.append("(" + " OR ".join(manufacturer_conditions) + ")")
    if one_two_sided_filter:
        where_conditions.append(f"e.exoOneTwoSided = '{one_two_sided_filter}'")
    if compact_filter:  
        where_conditions.append(f"ep.exoPropertyName = 'compact' and r.exoPropertyValue = '{compact_filter}'")
    if water_filter:  
        where_conditions.append(f"ep.exoPropertyName = 'waterbestendig' and r.exoPropertyValue = '{water_filter}'")
    if stof_filter:  
        where_conditions.append(f"ep.exoPropertyName = 'stofbestendig' and r.exoPropertyValue = '{stof_filter}'")        
    if search_query:
        where_conditions.append(f"toLower(e.exoName) CONTAINS toLower('{search_query}')")

    # Construct the WHERE clause for the Neo4j query
    where_clause = " WHERE " + " AND ".join(where_conditions) if where_conditions else ""

    # Final Neo4j query for exoskeleton data retrieval
    full_query = f"{base_query}{where_clause} RETURN e.exoId AS id, e.exoName AS Name, joints AS Joint, " \
            f"e.exoActivePassive AS ActivePassive, e.exoManufacturer AS Manufacturer, e.exoMaterial AS Material, " \
            f"e.exoOneTwoSided AS OneTwoSided, e.exoDescription AS Description ORDER BY Name"
    
    # Neo4j query to fetch property values
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
    
    # Remove duplicate exoskeletons based on 'id'
    new_all_exo  = []
    for exo in all_exoskeletons:
        if not exo["id"] in [ i["id"] for i in new_all_exo]:
            new_all_exo.append(exo)

     # Update the all_exoskeletons variable
    all_exoskeletons = new_all_exo

    # Store filter values in the session for future use
    session['active_passive_filter'] = active_passive_filter
    session['manufacturer_filter'] = manufacturer_filter
    session['material_filter'] = material_filter
    session['one_two_sided_filter'] = one_two_sided_filter
    session['compact_filter'] = compact_filter
    session['water_filter'] = water_filter
    session['stof_filter'] = stof_filter
    session['joint_filter'] = joint_filter
    
    # Render the template and pass the data
    return render_template(
        "exolist.html",
        exoskeletons=new_all_exo,
        properties_dict=properties_dict,
        active_passive_filter=active_passive_filter,
        manufacturer_filter=manufacturer_filter,
        material_filter=material_filter,
        one_two_sided_filter=one_two_sided_filter,
        compact_filter=compact_filter,
        water_filter=water_filter,
        stof_filter=stof_filter,
        joint_filter=joint_filter,
    )