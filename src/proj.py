import manager as m
g = m.Manager()
g.set_Configuration(layerNum = 4,layerNodeNum = [20,500,1250,3600], outputPath = "../connection_data/", 
conPara = {"1,1": 150,"1,2": 230,"2,2": 350,"2,3": 60,"3,3":60,"3,4":10,"4,4":16},
conDisPara= {"1,1": 1.5,"1,2": 1.5,"2,2": 1.5,"2,3": 1.5,"3,3":1.5,"3,4":1.5,"4,4":1.5},
graphName = "2018-5-30-10000nodes")
g.generate_Graph()
g.print_Configuration()
print("Success")
