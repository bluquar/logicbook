(function() {
  var app = angular.module('logicbookWorkspace', ['ngSanitize']);

  app.controller('LibraryController', function(){
    this.builtinDefinitions = ModuleDefinition.builtins;
    this.userDefinitions = [];
  });

  app.controller('WorkspaceController', ['$scope', function($scope) {
  	var workspace = this; // For referencing the controller within closures
  	this.scope = $scope;

  	// Array of errors. Each should have these properties:
  	//   text: A string to display with the error
  	//   actionText: A string to display on the button
  	//   action: A function to be called when the button is pressed.
  	// When the button is pressed, the error will also be removed from the list.
  	this.errors = [];

  	// Whether there is a module definition being edited. If true, activeDefinition is
  	// a ModuleDefinition (see logicbook.js) object representing the definition being edited
  	this.isEditing = false;   
    this.activeDefinition = null;

    // Whether the workspace has unsaved changes
    this.hasUnsavedChanges = false;

    // Whether the active definition is being updated by a web request
    this.isLoading = false;

    // The instances (ModuleInstances) within the definition
    this.instances = [];

    this.errorAction = function(error) {
    	var i;
    	for (i = 0; i < workspace.errors.length; i++) {
    		if (error === workspace.errors[i]) {
    			error.action();
    			workspace.errors.splice(i, 1);
    			break;
    		}
    	}
    };

    this.createNew = function() {
    	workspace.isLoading = true;
    	$.ajax({
    		url: "new_definition",
    		type: "POST",
    		dataType: "json",
    		data: {
    			'csrfmiddlewaretoken': $.cookie('csrftoken'),
    		},
    		success: function (json) {
    			if (json.success) {
    				workspace.scope.$apply(function() {
    					workspace.isLoading = false;
    					workspace.isEditing = true;
    					workspace.hasUnsavedChanges = false;
    					workspace.activeDefinition = new ModuleDefinition(
    						json.definition.id,
    						json.definition.name,
    						json.definition.nodeCount,
    						json.definition.svgPath,
    						json.definition.ports
    						);
    					workspace.instances = [];
    				});
				} else {
					workspace.scope.$apply(function() {
						workspace.errors.push({
							text: json.errorMessage,
							actionText: "Try Again",
							action: workspace.createNew
						});
					});
				}
			},
			error: function(xhr, status, err) {
				workspace.scope.$apply(function() {
					workspace.errors.push({
						text: "Network or server error",
						html: xhr.responseText,
						actionText: "Try Again",
						action: workspace.createNew
					})
				});
			}
    	});
    };

    this.isSet = function(tabName){
      return this.tab === tabName;
    };
  }]);
})();