# Exolist Route Documentation

The `/exolist` route in this Flask application fetches and displays a list of exoskeletons from a Neo4j database. The list can be filtered based on various criteria using query parameters.

## Filters

The route accepts the following query parameters as filters:

- **active_passive_filter**: Filters exoskeletons based on whether they are active or passive.
- **manufacturer_filter**: Filters exoskeletons based on the manufacturer(s).
- **material_filter**: Filters exoskeletons based on the material.
- **one_two_sided_filter**: Filters exoskeletons based on whether they are one or two-sided.
- **search_query**: Allows users to search for exoskeletons by name.
- **compact_filter**: Filters exoskeletons based on a property named 'compact' with a specific value.

## Base Query

The base query retrieves exoskeletons along with their main degrees of freedom (DOF) and associated joints. The result is used to build the list of exoskeletons and their joint information.

## Where Conditions

Various `where_conditions` are dynamically constructed based on the provided filters. Each condition corresponds to a specific filter, and these conditions are combined to form the `WHERE` clause in the Neo4j Cypher query.

## Full Query

The complete Cypher query is constructed by combining the base query and the `WHERE` clause. The query fetches exoskeleton details such as ID, name, joints, activity type, manufacturer, material, one/two-sided information, and description. The result is ordered by exoskeleton name.

## Properties Query

A separate query retrieves exoskeleton properties such as 'compact' and their values. The results are used to create a dictionary (`properties_dict`) mapping exoskeleton IDs to their property values.

## Rendering Template

Finally, the route renders the `exolist.html` template, passing the fetched exoskeleton data, properties dictionary, and filter parameters to be displayed to the user.

This documentation provides a comprehensive understanding of how the `/exolist` route works, making it easier for developers to contribute or understand the functionality.
