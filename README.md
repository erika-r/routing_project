# Uni-directional Router

This project simulates a uni-directional router

This project was created in 5 parts
- creating a Graph class which manages all routers, and a Router class which calculates the shortest path and cost of travelling to any other given router
- implementing the ability to display the cost and shortest path between the given router and all other routers in a table using the Pandas dataframe.
- implementing a function to safely remove a "dead" router from the graph, allowing the routing table to be recalculated correctly
- allowing multiple routers to share a graph and so affecting each other's paths between other routers
- creating a unit test using PyUnit
