# Exoskeleton Search and Filter Application Documentation

This documentation provides an overview of the Python code (`app.py`) and the associated HTML template (`exolist.html`) for an exoskeleton search and filter application built using Flask and Neo4j. The application allows users to search and filter exoskeletons based on various criteria.

## Python Code (`app.py`)

### Filtering in Flask Application

The Python code defines a Flask route `/exolist` that performs filtering operations to retrieve exoskeleton data from a Neo4j database. Here's a breakdown of the code:

```py
@app.route("/exolist"):
```
The Python code is responsible for fetching exoskeleton data based on various filter parameters and rendering the template to display the results. It includes filters for active/passive, manufacturer, material, one/two-sided, and a search query based on the exoskeleton name.

Here's the Python code used for filtering:
```py
# Filters
active_passive_filter = request.args.get("active_passive")
manufacturer_filter = request.args.getlist("manufacturer")
material_filter = request.args.get("material")
one_two_sided_filter = request.args.get("one_two_sided")
search_query = request.args.get("search_query")  # Get the search query from the query string

# Define the base query for fetching exoskeletons
base_query = "MATCH (e:Exo) OPTIONAL MATCH (e)-[r1:HAS_AS_MAIN_DOF]-(d:Dof)-[r2:HAS_DOF]-(j:JointT) WITH e, COLLECT(DISTINCT j.jointTName) AS joints"

where_conditions = []

# Conditionally add the filter conditions
if active_passive_filter:
    where_conditions.append(f"e.exoActivePassive = '{active_passive_filter}'")

# Other filter conditions for manufacturer, material, and one_two_sided_filter

if search_query:
    where_conditions.append(f"toLower(e.exoName) CONTAINS toLower('{search_query}')")

if where_conditions:
    where_clause = " WHERE " + " AND ".join(where_conditions)
else:
    where_clause = ""

# Rest of the query and other property queries

# Fetch data from Neo4j
all_exoskeletons = g.run(base_query).data()
properties_data = g.run(properties_query).data()
features_data = g.run(features_query).data()

# Data processing to determine exoskeleton features

# Template rendering and data passing
return render_template("exolist.html", exoskeletons=all_exoskeletons, active_passive_filter=active_passive_filter, manufacturer_filter=manufacturer_filter, material_filter=material_filter, one_two_sided_filter=one_two_sided_filter)
```

## HTML Template (exolist.html)
Filtering and Display in HTML
The HTML template (exolist.html) is designed for filtering exoskeletons based on the filter parameters and displaying the chosen filter options. Here's a breakdown of the HTML code:
```HTML
<!-- Search Box -->
<div class="w-96 mb-4 text-center">
    <!-- Input field for search query -->
</div>

<!-- Filter Options -->
<div class="flex flex-wrap justify-center space-x-4">
    <!-- Filter options for Type, Fabrikant, Materiaal, and Zijden -->
</div>

<!-- Apply and Reset Buttons -->
<div class="flex space-x-2 my-10">
    <button type="submit" class="btn btn-primary w-1/2">Filter</button>
    <a href="/exolist" class="btn btn-secondary w-1/2">Reset</a>
</div>

<!-- Chosen Filter Options Display -->
<div class="flex flex-wrap justify-center mt-2 -mx-2 my-2">
    <!-- Filter display items in rounded boxes -->

    <!-- Filter Display Styling -->
    <!-- Responsive Layout -->

    <!-- Max Display Limit: A maximum of 6 chosen filter options per row with spacing -->
    <!-- Centered Layout: Filter display and options are centered in the middle of the screen -->
</div>
```

The combination of Python code and HTML template creates a user-friendly web application for searching and filtering exoskeleton data. The provided documentation explains the functionality of the application, filter parameters, and the structure of the HTML template.

Feel free to use this documentation as a reference and enhance it further as needed. If you have any additional questions or require further assistance, please don't hesitate to ask.

