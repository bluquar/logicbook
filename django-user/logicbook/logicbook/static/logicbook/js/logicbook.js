var LOGIC_0 = 0;
var LOGIC_1 = 1;
var LOGIC_X = 2;
var LOGIC_Z = 3;

var logic = {
	// Perform a logical operation on an array of input logic values.
	and: function(inputs) {
		var ret = LOGIC_1;
		var i, val;
		for (i = 0; i < inputs.length; i++) {
			val = inputs[i];
			if (val === LOGIC_X || ret === LOGIC_X) {
				ret = LOGIC_X;
				break;
			} else if (val === LOGIC_Z) {
				continue;
			} else if (ret === LOGIC_Z) {
				ret = val;
				continue;
			} else {
				ret = (val === ret === LOGIC_1) ? LOGIC_1 : LOGIC_0;
			}
		}
		return ret;
	},
	or: function(inputs) {
		var ret = LOGIC_0;
		var i, val;
		for (i = 0; i < inputs.length; i++) {
			val = inputs[i];
			if (val === LOGIC_X || ret === LOGIC_X) {
				ret = LOGIC_X;
				break;
			} else if (val === LOGIC_Z) {
				continue;
			} else if (ret === LOGIC_Z) {
				ret = val;
				continue;
			} else {
				ret = (val === ret === LOGIC_1) ? LOGIC_1 : LOGIC_0;
			}
		}
		return ret;	
	}
}

function Port(name, width, parent, direction, nodeNum, posX, posY) {
	this.name = name;
	this.width = width;
	this.parent = parent;
	this.direction = direction; // "in" or "out"
	this.nodeNum = nodeNum;
	this.posX = posX;
	this.posY = posY;
}
Port.prototype = {
	isInput: function() {
		return this.direction === "in";
	},
	isOutput: function() {
		return this.direction === "out";
	}
}

function ModuleDefinition(id, name, description, nodeCount, svgPath, ports, evalFn) {
	var defn = this;

	this.id = id;
	this.name = name || "New Module";
	this.nodeCount = nodeCount || 0;
	this.svgPath = svgPath || "/static/images/box.svg";
	this.ports = ports || [];
	if (evalFn !== undefined) {
		this.evaluate = evalFn;
	}

	this.inputPorts = [];
	this.outputPorts = [];

	$.each(this.ports, function(index, port) {
		port.parent = defn;
		if (port.isInput()) {
			defn.inputPorts.push(port);
		}
		else if (port.isOutput()) {
			defn.outputPorts.push(port);
		} else {
			console.log("Unrecognized port direction: " + port.direction);
			console.log(port);
			console.log(defn);
		}
	});
}

ModuleDefinition.prototype.evaluate = function(instance, parentDefinition) {
	// TODO

}

function ModuleInstance(id, name, definition, parent, nodes) {
	this.id = id;
	this.name = name;
	this.definition = definition; // Instance of ModuleDefinition
	this.parent = parent; // Instance of ModuleDefinition
	this.nodes = nodes;
}


