# Code Documentation for '/exolist'

## Overview
The provided Flask code defines a route for the `/exolist` endpoint, which displays a list of exoskeletons based on various filters and a search query. The code interacts with a Neo4j database to retrieve and filter exoskeleton data.

## Function: exolist()
This function is the main route handler for displaying the exoskeleton list.

### Request Parameters
- **active_passive_filter**: Filter for exoskeleton active/passive status.
- **joint_filter**: Filter for exoskeleton joints.
- **manufacturer_filter**: Filter for exoskeleton manufacturers.
- **material_filter**: Filter for exoskeleton materials.
- **one_two_sided_filter**: Filter for one/two-sided exoskeletons.
- **compact_filter, water_filter, stof_filter**: Filters for specific properties.
- **search_query**: Search query for exoskeleton names.

### Neo4j Queries
The code constructs Neo4j queries to retrieve exoskeleton data and property values. The base query includes optional matches for joints and properties.

### Where Conditions
Filter conditions are dynamically added to the Neo4j query based on the request parameters. Conditions include active/passive status, joints, manufacturers, materials, and specific property values.

### Data Processing
- Retrieved exoskeleton data is processed to remove duplicates based on the 'id' field.
- Property values are fetched separately from the Neo4j database.

### Session Storage
Filter values are stored in the Flask session for user persistence across requests.

### Debugging
The WHERE clause and conditions are printed for debugging purposes.

### Rendering
The processed data is passed to the 'exolist.html' template for rendering.

## Template Rendering
The `exolist.html` template is rendered with the following data:
- `exoskeletons`: Processed exoskeleton data.
- `properties_dict`: Dictionary of property values for each exoskeleton.
- Filter values for active_passive, manufacturer, material, etc.

## Conclusion
This Flask route provides a dynamic and filtered view of exoskeleton data based on user input. It leverages Neo4j queries to fetch and process data, and the results are presented in an HTML template.
