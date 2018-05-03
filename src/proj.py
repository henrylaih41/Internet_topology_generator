import manager as m
g = m.Manager()
g.set_Configuration(layerNum = 4,layerNodeNum = [20,100,100,100], outputPath = "../connection_data/", 
graphName = "2018-5-2-test5", conPara = {"1,1": 75,"1,2": 6,"2,2": 10,"2,3": 30,"3,3": 10,"3,4": 20,"4,4": 10})
g.generate_Graph()
g.print_Configuration()
print("Success")
