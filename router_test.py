import unittest
from router import *


class Testing(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        self.graph.add_edge("a", "b", 7)
        self.graph.add_edge("a", "c", 9)
        self.graph.add_edge("a", "f", 14)
        self.graph.add_edge("b", "c", 10)
        self.graph.add_edge("b", "d", 15)
        self.graph.add_edge("c", "d", 11)
        self.graph.add_edge("c", "f", 2)
        self.graph.add_edge("d", "e", 6)
        self.graph.add_edge("e", "f", 9)

        #create routers
        self.router = Router("a",self.graph)
        self.router_two = Router("b",self.graph)

    #confirm graph is created
    def test_graph(self):
        self.assertIsInstance(self.graph,Graph)     #check graph has been created

    def test_add_edge(self):
        self.assertEqual(9,len(self.graph.edges))      #confirm there are 9 nodes in the beginning
        self.graph.add_edge("x", "z", 7)   
        self.assertEqual(10,len(self.graph.edges))    #confirms 1 is added
        self.assertNotEqual(11,len(self.graph.edges))     #confirms not more than 1 is added

    #confirm they are created
    def test_router(self):
        self.assertIsInstance(self.router,Router)
        self.assertIsInstance(self.router_two,Router)

    def test_dijkstra(self):    #test dijkstra as get_path returns None
        #test for correct answer and incorrect answer
        self.assertEqual(("b->c",10),self.router_two.graph.dijkstra(self.router_two.name,"c"))
        self.assertNotEqual(("b->f->c",12),self.router_two.graph.dijkstra(self.router_two.name,"c"))

    #confirm that it removes from shared graph
    def test_remove_router(self):
        self.assertEqual(("b->c->f",12),self.router_two.graph.dijkstra(self.router_two.name,"f"))   #before c is removed
        self.router.remove_router("c")  #remove from first router
        self.assertEqual(("b->d->e->f",30),self.router_two.graph.dijkstra(self.router_two.name,"f"))

if __name__ == "__main__":
    unittest.main()
