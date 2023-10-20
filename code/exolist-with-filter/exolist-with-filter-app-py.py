@app.route("/exolist")
def exolist():
    # Get filter options from the query string
    active_passive_filter = request.args.get("active_passive")  # Get the active/passive filter
    manufacturer_filter = request.args.get("manufacturer")  # Get the manufacturer filter
    material_filter = request.args.get("material")  # Get the material filter
    one_two_sided_filter = request.args.get("one_two_sided")  # Get the OneTwoSided filter

    # Define the base query for fetching exoskeletons
    base_query = "MATCH (e:Exo) OPTIONAL MATCH (e)-[r1:HAS_AS_MAIN_DOF]-(d:Dof) OPTIONAL MATCH (d)-[r2:HAS_DOF]-(j:JointT) WITH e, COLLECT(DISTINCT j.jointTName) AS joints"

    where_conditions = []

    # Conditionally add the filter conditions
    if active_passive_filter:
        where_conditions.append(f"e.exoActivePassive = '{active_passive_filter}'")

    if manufacturer_filter:
        where_conditions.append(f"e.exoManufacturer = '{manufacturer_filter}'")

    if material_filter:
        where_conditions.append(f"e.exoMaterial = '{material_filter}'")

    if one_two_sided_filter:
        where_conditions.append(f"e.exoOneTwoSided = '{one_two_sided_filter}'")

    if where_conditions:
        where_clause = " WHERE " + " AND ".join(where_conditions)
    else:
        where_clause = ""

    # Complete the query with filter conditions and return fields
    base_query += f"{where_clause} RETURN e.exoName AS Name, joints AS Joint, e.exoActivePassive AS ActivePassive, e.exoManufacturer AS Manufacturer, e.exoMaterial AS Material, e.exoOneTwoSided AS OneTwoSided, e.exoDescription AS Description ORDER BY Name"

    # Execute the query with filters
    all_exoskeletons = g.run(base_query).data()
    exoskeleton_count = len(all_exoskeletons)

    # Render the HTML template with filter options and query results
    return render_template("exolist.html", exoskeletons=all_exoskeletons, active_passive_filter=active_passive_filter, manufacturer_filter=manufacturer_filter, material_filter=material_filter, one_two_sided_filter=one_two_sided_filter)
