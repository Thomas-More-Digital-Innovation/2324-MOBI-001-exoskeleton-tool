# Exoskeleton list with filter options


### 1. HTML Template Code for a Homepage:
   This HTML template is designed for the homepage of a web application. It extends a base template and includes a navigation bar. It presents three distinct cards, each with an image and a call-to-action button. The buttons link to an "exolist" page. Additionally, there's a "Go back" button at the top for returning to the main tool page.

### 2. HTML Template Code for Filtering and Displaying Data:
   This HTML template is used for displaying data and filtering options. It features a filter form with options to filter exoskeletons by type, manufacturer, material, and the number of sides. Users can apply filters and reset them with dedicated buttons. Below the filter form, the code iterates through a list of exoskeletons, displaying information about each one in a card format. Each card includes an image, exoskeleton details, and a "More Information" button. The template is designed with the Tailwind CSS framework for styling.

### 3. More detailed explanation:
```py
@app.route("/exolist")
def exolist():
    active_passive_filter = request.args.get("active_passive")  # Get the active/passive filter from the query string
    manufacturer_filter = request args.get("manufacturer")  # Get the manufacturer filter from the query string
    material_filter = request.args.get("material")  # Get the material filter from the query string
    one_two_sided_filter = request.args.get("one_two_sided")  # Get the OneTwoSided filter from the query string
```
This Flask route /exolist is responsible for fetching and displaying exoskeleton data based on user filters.
It retrieves filter values (active_passive, manufacturer, material, and one_two_sided) from the query string, which is part of the URL.

```py
    # Define the base query for fetching exoskeletons
    base_query = "MATCH (e:Exo) OPTIONAL MATCH (e)-[r1:HAS_AS_MAIN_DOF]-(d:Dof) OPTIONAL MATCH (d)-[r2:HAS_DOF]-(j:JointT) WITH e, COLLECT(DISTINCT j.jointTName) AS joints"
```
This part sets up the base query to fetch exoskeleton data from a Neo4J database.
It uses Cypher query language to match exoskeleton nodes and optionally match related nodes for joints and degrees of freedom (DOF)

```py   
where_conditions = []
```
* It initializes an empty list to store conditions for filtering the query.

```py
    # Conditionally add the filter conditions
    if active_passive_filter:
        where_conditions.append(f"e.exoActivePassive = '{active_passive_filter}'")

    if manufacturer_filter:
        where_conditions.append(f"e.exoManufacturer = '{manufacturer_filter}'")

    if material_filter:
        where_conditions.append(f"e.exoMaterial = '{material_filter}'")

    if one_two_sided_filter:
        where_conditions.append(f"e.exoOneTwoSided = '{one_two_sided_filter}'")
```
* This section adds filter conditions to the where_conditions list based on the filter values obtained from the query string.

```py
    if where_conditions:
        where_clause = " WHERE " + " AND ".join(where_conditions)
    else:
        where_clause = ""
```
* It creates a `WHERE` clause based on the conditions stored in where_conditions. If there are no conditions, it sets where_clause as an empty string.

```py
    # Rest of the query
    base_query += f"{where_clause} RETURN e.exoName AS Name, joints AS Joint, e.exoActivePassive AS ActivePassive, e.exoManufacturer AS Manufacturer, e.exoMaterial AS Material, e.exoOneTwoSided AS OneTwoSided, e.exoDescription AS Description ORDER BY Name"
```
* The rest of the query appends the WHERE clause, then retrieves specific attributes of the exoskeleton nodes and joints and assigns aliases. It also orders the results by the name of exoskeletons.

```py
    # Use the filters in your query
    all_exoskeletons = g.run(base_query).data()
    exoskeleton_count = len(all_exoskeletons)
    return render_template("exolist.html", exoskeletons=all_exoskeletons, active_passive_filter=active_passive_filter, manufacturer_filter=manufacturer_filter, material_filter=material_filter, one_two_sided_filter=one_two_sided_filter)
```
* This section executes the query and passes the results to the HTML template for rendering. It also includes the filter values in the response for displaying and retaining filter selections.