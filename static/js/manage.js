// 	How to post json data to a url and do something with the result
//	var res = $http.post('/save_json', dataObj);
// 	res.success(function(data, status, headers, config) {
// 		$scope.message = data;
// 	});
// 	res.error(function(data, status, headers, config) {
// 			alert( "failure message: " + JSON.stringify({data: data}));
// 		});

var app = angular.module('manager', ['ngRoute', 'ui.bootstrap']);

app.config(function($routeProvider, $locationProvider) {
	// $routeProvider
	// 	.when('/', {
	// 		controller: 'mainController'
	// 	});

	$locationProvider.html5Mode(true);
});

app.service('sharedItem', function () {
    var item = {};

    return {
        get: function () {
            return item;
        },
        set: function(value) {
            item = value;
        }
    };
});

app.controller('sidebarController', function($scope, $http) {
	$scope.sidebarInstruction = "←";

	$scope.sidebarClick = function() {
		$("#wrapper").toggleClass("toggled");

		if ($scope.sidebarInstruction == "←") {
			$scope.sidebarInstruction = "→";
		}
		else {
			$scope.sidebarInstruction = "←";
		}
	}
});

app.controller('toolbar', function($scope, $http) {

	$scope.embed = function() {
		alert(1);
	}

});

app.controller('sidebar', function($scope, $http) {

	$http.get('/api/' + user.username + '/menus').
	  	success(function(data, status, headers, config) {
	    	$scope.menus = data;
	  	}).
	  	error(function(data, status, headers, config) {
	    	$scope.menus = [];
	  	});
});

app.controller('embed', function($scope, $http) {
	$scope.username = user.username;
});

app.controller('info', function($scope, $http, $rootScope) {

	load();
	reset();

	function load() {
		$http.get('/api/' + user.username + '/info').
	  	success(function(data, status, headers, config) {
	    	$scope.info = data.info;
	  	});
	}

	function reset() {
		$scope.sectionName = '';
	}

	function post(data) {
		$http.post('/api/' + user.username + '/info', data).
			success(function(data, status, headers, config) {
				$scope.info = data.info;
			});
		$rootScope.$broadcast('infoRefresh');
	}

	$scope.isArray = function(array) {
		return Object.prototype.toString.call( array ) === '[object Array]';
	}

	$scope.add = function(item) {
		item.value.push({"name": "", "value": ""});
	}

	$scope.addSection = function() {
		var sectionName = $scope.sectionName;
		$scope.info.push({"name": sectionName, "value": [{"name": "", "value": ""}]});
		reset();
	}

	$scope.save = function() {
		var info = $scope.info;
		post( {"action":"save", "info":{ info }} );
		reset();
	}
	
});

app.controller('iframe', function($scope, $http) {
	$scope.username = user.username;

	function load() {
		$('#iframe').attr('src', $('#iframe').attr('src'));
	}

	$scope.$on('categoryRefresh', function(event, args) {
		load();
	});

	$scope.$on('infoRefresh', function(event, args) {
		load();
	});

	$scope.$on('itemRefresh', function(event, args) {
		load();
	});

	$scope.$on('styleRefresh', function(event, args) {
		load();
	});
});

app.controller('categories', function($scope, $http, $rootScope) {

	load();
	reset();

	function load() {
		$http.get('/api/' + user.username + '/categories').
	  	success(function(data, status, headers, config) {
	    	$scope.categories = data.categories;
	  	});
	}

	function reset() {
		$scope.newCategoryName = '';
	}

	function post(data) {
		$http.post('/api/' + user.username + '/categories', data).
			success(function(data, status, headers, config) {
				$scope.categories = data.categories;
			});
		$rootScope.$broadcast('categoryRefresh');
	}

	$scope.add = function(categoryName) {
        $scope.categories.push({"name": categoryName});
        post( {"action":"save", "category":{"name": categoryName}} );
        reset();
    };

    $scope.remove = function(category) {
    	if (! confirm('Are you sure you want to remove the category ' + category.name + '? This will delete all of the items in it.')) {
    		return;
    	}

    	var index = $scope.categories.indexOf(category);
    	if (index !== -1) {
    		$scope.categories.splice(index, 1);
    	}

    	post({"action":"delete", category});
    };
});

app.controller('additem', function($scope, $http, $rootScope) {

	load();
	reset();

	function load() {
		$http.get('/api/' + user.username + '/categories').
	  	success(function(data, status, headers, config) {
	    	$scope.categories = data.categories;
	  	});
	}

	$scope.$on('categoryRefresh', function(event, args) {
		load();
	});

	function reset() {
    	$scope.item = {};
        $scope.item.options = [];
    }

    function post(data) {
    	$http.post('/api/' + user.username + '/items', data).
			success(function(data, status, headers, config) {

			});
		$rootScope.$broadcast('itemRefresh');
    }

    $scope.addOption = function() {
        $scope.item.options.push({});
    };

    $scope.save = function() {
    	var item = $scope.item;
    	post({"action":"save", item });
        reset();
    };
});

app.controller('edititem', function($scope, $http, $rootScope, sharedItem) {


	categoryLoad();

	var originalItem = {};

	function categoryLoad() {
		$http.get('/api/' + user.username + '/categories').
	  	success(function(data, status, headers, config) {
	    	$scope.categories = data.categories;
	  	});
	}

	$scope.$on('categoryRefresh', function(event, args) {
		categoryLoad();
	});

	function load() {
		$scope.item = sharedItem.get();
		originalItem = JSON.parse(JSON.stringify($scope.item));
		if (!$scope.item.options) {
			$scope.item.options = [];
		}
	}

	$scope.$on('editItem', function(event, args) {
		load();
	});

	function post(data) {
    	$http.post('/api/' + user.username + '/items', data).
			success(function(data, status, headers, config) {

			});
		$rootScope.$broadcast('itemRefresh');
    }

    $scope.addOption = function() {
        $scope.item.options.push({});
    };

    $scope.save = function() {
    	var item = $scope.item;
    	post({"action":"update", item, originalItem });
    };

    $scope.delete = function() {
    	var item = originalItem; // original to avoid lack of delete on changed items
    	post({"action":"delete", item });
    };

});

app.controller('view', function($scope, $http, $rootScope, sharedItem) {

	load();
	reset();

	$scope.$on('categoryRefresh', function(event, args) {
		load();
	});

	$scope.$on('infoRefresh', function(event, args) {
		load();
	});

	$scope.$on('itemRefresh', function(event, args) {
		load();
	});

	$scope.$on('styleRefresh', function(event, args) {
		load();
	});

	function load() {
        $http.get('/api/' + restaurantName).
        	success(function(data, status, headers, config) {
			    $scope.menu = data;
		  	});
	}

	function reset() {
		$scope.query = '';
	}

	$scope.edit = function(item, category, options) {
		item.category = {};
		item.category.name = category.name;
		item.options = options;
		sharedItem.set(item);
		$rootScope.$broadcast('editItem');
		$('#edititem').modal('show');

	}

	$scope.search = function(query) {
		if (query == '') {
			reset();
			load();
		}

		$http.get('/api/' + restaurantName + '/search/' + query).
	  	success(function(data, status, headers, config) {
	    	$scope.menu.categories = data.categories;
	    	$scope.menu.items = data.items;
	  	});
	}

	$scope.isArray = function(array) {
		return Object.prototype.toString.call( array ) === '[object Array]';
	}

	$scope.L = function(component, elementName) {
		return $scope.getElement(component, elementName);
	}

	$scope.getElement = function(component, elementName) {
		if (! $scope.menu)
			return;
		var idx = indexOf($scope.menu.style[component], "name", elementName);
		if (idx == -1) {
			return "null";
		}
		return $scope.menu.style[component][idx].value;
	}

	function indexOf(array, key, value) {

		for (var i = 0; i < array.length; i++) {
			if (array[i][key] == value)
				return i;
		}

		return -1;
	}

});























app.controller('stylegeneral', function($scope, $http, $rootScope) {

	load();

	function load() {
		$http.get('/api/' + user.username + '/style').
		  	success(function(data, status, headers, config) {
		    	$scope.style = data.style.general;
		  	});
	}

	function post(data) {
		$http.post('/api/' + user.username + '/style', data).
			success(function(data, status, headers, config) {
				$scope.style = data.style.general;
			});
		$rootScope.$broadcast('styleRefresh');
	}

	$scope.save = function() {
    	var style = $scope.style;
    	post({"action":"save", "component":"general", style });
    };

});

app.controller('styletitle', function($scope, $http, $rootScope) {

	load();

	function load() {
		$http.get('/api/' + user.username + '/style').
		  	success(function(data, status, headers, config) {
		    	$scope.style = data.style.title;
		  	});
	}

	function post(data) {
		$http.post('/api/' + user.username + '/style', data).
			success(function(data, status, headers, config) {
				$scope.style = data.style.title;
			});
		$rootScope.$broadcast('styleRefresh');
	}

	$scope.save = function() {
    	var style = $scope.style;
    	post({"action":"save", "component":"title", style });
    };

});
app.controller('stylecategory', function($scope, $http, $rootScope) {

	load();

	function load() {
		$http.get('/api/' + user.username + '/style').
		  	success(function(data, status, headers, config) {
		    	$scope.style = data.style.category;
		  	});
	}

	function post(data) {
		$http.post('/api/' + user.username + '/style', data).
			success(function(data, status, headers, config) {
				$scope.style = data.style.category;
			});
		$rootScope.$broadcast('styleRefresh');
	}

	$scope.save = function() {
    	var style = $scope.style;
    	post({"action":"save", "component":"category", style });
    };

});
app.controller('styleitem', function($scope, $http, $rootScope) {

	load();

	function load() {
		$http.get('/api/' + user.username + '/style').
		  	success(function(data, status, headers, config) {
		    	$scope.style = data.style.item;
		  	});
	}

	function post(data) {
		$http.post('/api/' + user.username + '/style', data).
			success(function(data, status, headers, config) {
				$scope.style = data.style.item;
			});
		$rootScope.$broadcast('styleRefresh');
	}

	$scope.save = function() {
    	var style = $scope.style;
    	post({"action":"save", "component":"item", style });
    };

});
app.controller('styleoption', function($scope, $http, $rootScope) {

	load();

	function load() {
		$http.get('/api/' + user.username + '/style').
		  	success(function(data, status, headers, config) {
		    	$scope.style = data.style.option;
		  	});
	}

	function post(data) {
		$http.post('/api/' + user.username + '/style', data).
			success(function(data, status, headers, config) {
				$scope.style = data.style.option;
			});
		$rootScope.$broadcast('styleRefresh');
	}

	$scope.save = function() {
    	var style = $scope.style;
    	post({"action":"save", "component":"option", style });
    };

});
app.controller('styleinfo', function($scope, $http, $rootScope) {

	load();

	function load() {
		$http.get('/api/' + user.username + '/style').
		  	success(function(data, status, headers, config) {
		    	$scope.style = data.style.info;
		  	});
	}

	function post(data) {
		$http.post('/api/' + user.username + '/style', data).
			success(function(data, status, headers, config) {
				$scope.style = data.style.info;
			});
		$rootScope.$broadcast('styleRefresh');
	}

	$scope.save = function() {
    	var style = $scope.style;
    	post({"action":"save", "component":"info", style });
    };

});

