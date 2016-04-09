ModuleDefinition.builtins = [
//  ModuleDefinition(id, name, description, nodeCount, svgPath, ports, evalFn)
new ModuleDefinition(1, "AND", "Logical AND of 2 values", 3, "/static/images/and.svg",
	[ 
	//  Port(name, width, parent, direction, nodeNum, posX, posY, evaluate);
	new Port("in1", 1, null, "in", 0, 0, 0.3),
	new Port("in2", 1, null, "in", 1, 0, 0.7),
	new Port("out", 1, null, "out", 2, 1, 0.5),
	],
	function(instance, parentDefinition) {
		var outNode = instance.nodes[2];
		var input1 = parentDefinition.valAtNode(instance.nodes[0]);
		var input2 = parentDefinition.valAtNode(instance.nodes[1]);
		parentDefinition.updateNode(instance.timeDelay, logic.and(input1, input2));
	}
	),
new ModuleDefinition(1, "OR", "Logical OR of 2 values", 3, "/static/images/or.svg",
	[ 
	//  Port(name, width, parent, direction, nodeNum, posX, posY, evaluate);
	new Port("in1", 1, null, "in", 0, 0, 0.3),
	new Port("in2", 1, null, "in", 1, 0, 0.7),
	new Port("out", 1, null, "out", 2, 1, 0.5),
	],
	function(instance, parentDefinition) {
		var outNode = instance.nodes[2];
		var input1 = parentDefinition.valAtNode(instance.nodes[0]);
		var input2 = parentDefinition.valAtNode(instance.nodes[1]);
		parentDefinition.updateNode(instance.timeDelay, logic.or(input1, input2));
	}
	),
]