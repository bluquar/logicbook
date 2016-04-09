from django.db import models
from django.contrib.auth.models import User
from djorm_pgarray.fields import IntegerArrayField

class UserProfile(models.Model):
	""" Additional profile data attached to a User """
	user = models.OneToOneField(User)
	following = models.ManyToManyField(User, related_name='followers')
	bio = models.CharField(max_length=430, null=True)
	profile_picture_url = models.CharField(null=True, max_length=256)

class ModuleDefinition(models.Model):
	"""
	A ModuleDefinition includes
	- user (creator)
	- name
	- node_count
	- svg_path
	- instances
	- wires
	- ports
	"""
	creator = models.ForeignKey(User)
	editors = models.ManyToManyField(User, related_name='editable_definitions')

	description = models.CharField(max_length=1024)
	comments = models.OneToManyField(Comment)

	name = models.CharField(max_length=64)

	# Number of nodes in the definition. Nodes are represented as integers.
	# Nodes are allocated from 0 to (node_count-1), so node_counter
	# is guaranteed not to be referenced by any existing wires or instances.
	# Therefore node_count should be used and then incremented whenever a new
	# node is needed.
	node_count = models.PositiveIntegerField()

	svg_path = models.CharField(max_length=64)

	def dict(self):
		"""
		Get a dictionary representation of the ModuleDefinition
		suitable for JSON serialization
		"""
		return {
		    "id": self.id,
		    "name": self.name,
		    "node_count": self.node_count,
		    "svg_path": self.svg_path,
		    "instances": [instance.dict() for instance in 
		                  ModuleInstance.objecs.filter(parent=self)],
		    "wires": [wire.dict() for wire in 
		              Wire.objects.filter(parent=self)],
		    "ports": [port.dict() for port in
                      Port.objects.filter(parent=self)]
        }


class ModuleInstance(models.Model):
	name = models.CharField(max_length=64)

	# The module definition which this instance is part of
	parent = models.ForeignKey(ModuleDefinition, related_name="children")

	# The module definition that specifies the implementation of this instance
	definition = models.ForeignKey(ModuleDefinition, related_name="instances")

	# `nodes` has the same length as ModuleInstance.definition.ports.
	# It is related to the definition such that nodes[i] is the node ID (within parent)
	# of the input or output port specified by definition.ports[i]
	nodes = IntegerArrayField()

	# Position within the parent definition
	posX = models.FloatField()
	posY = models.FloatField()
	posWidth = models.FloatField()
	posHeight = models.FloatField()

	def dict(self):
		return {
		    "name": self.name,
		    "parent": self.parent.id,
		    "definition": self.definition.id,
		    "nodes": self.nodes,
		    "posX": self.posX,
		    "posY": self.posY,
		    "posWidth": self.posWidth,
		    "posHeight": self.posHeight
		}

class Wire(models.Model):
	name = models.CharField(max_length=32)

	# The module definition which this wire is part of
	parent = models.ForeignKey(ModuleDefinition)

	# The node that drives this wire
	node_in   = models.PositiveIntegerField()

	# The node this wire drives
	node_out  = models.PositiveIntegerField()

	# The number of bits carried by this wire
	width  = models.PositiveIntegerField()

	# If this wire outputs to more than one node (must be inputs to wires),
	# this array contains the node numbers that it splits OR copies to.
	# If the widths of the connecting wires add up to the length of this wire,
	# it is considered a split and bits will be sent in the order specified here.
	# If the width of each wire are equal to this wire's width, it is a copy.
	# Otherwise, it is considered a split. Extra bits are discarded (causes warning)
	# and insufficient bits are wired `undefined` (also causes warning.)
	split_copy_nodes   = IntegerArrayField()
	combine_nodes = IntegerArrayField()

	# Position within the parent definition
	in_posX = models.FloatField()
	in_posY = models.FloatField()
	out_posX = models.FloatField()
	out_posY = models.FloatField()

	def dict(self):
		return {
		    "name": self.name,
		    "parent": self.parent.id,
		    "node_in": self.node_in,
		    "node_out": self.node_out,
		    "width": self.width,
		    "split_copy_nodes": self.split_copy_nodes,
		    "combine_nodes": self.combine_nodes,
		    "posX": self.posX,
		    "posY": self.posY
		}

class PortDirection:
	input =  0
	output = 1

class Port(models.Model):
	name = models.CharField(max_length=32)
	width = models.PositiveIntegerField()

	# The module definition this port is an input or output to
	parent = models.ForeignKey(ModuleDefinition)

	# Whether this is an input or output port. Should be an attribute of PortDirection
	direction = models.PositiveIntegerField()

	# The node ID (within the parent definition)
	node = models.PositiveIntegerField()

	# The position of the port (within the parent)
	posX = models.FloatField()
	posY = models.FloatField()

	def direction_string(self):
		if self.direction == PortDirection.input:
			return "in"
		else:
			return "out"

	def dict(self):
		return {
		    "name": self.name,
		    "width": self.width,
		    "parent": self.parent.id,
		    "direction": self.direction_string(),
		    "nodeNum": self.node,
		    "posX": self.posX,
		    "posY": self.posY
		}


class PortValue(models.Model):
	test_case = models.ForeignKey(TestCase)
	port = models.ForeignKey(Port)
	value = models.PositiveIntegerField()

class TestCase(models.Model):
	name = models.CharField(max_length=100)
	creator = models.ForeignKey(User)
	creation_time = models.DateTimeField(auto_now_add=True)
	definition = models.ForeignKey(ModuleDefinition)
	comments = models.OneToManyField(Comment)

class Comment(models.Model):
	text = models.CharField(max_length=600)
	rating = models.PositiveIntegerField()
	creator = models.ForeignKey(User)
	creation_time = models.DateTimeField(auto_now_add=True)
