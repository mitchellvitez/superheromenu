// 	How to post json data to a url and do something with the result
//	var res = $http.post('/save_json', dataObj);
// 	res.success(function(data, status, headers, config) {
// 		$scope.message = data;
// 	});
// 	res.error(function(data, status, headers, config) {
// 			alert( "failure message: " + JSON.stringify({data: data}));
// 		});

var app = angular.module('manager', ['ngRoute']);

app.config(function($routeProvider, $locationProvider) {
	// $routeProvider
	// 	.when('/', {
	// 		controller: 'mainController'
	// 	});

	$locationProvider.html5Mode(true);
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

	function load() {
		$http.get('/api/' + user.username + '/info').
	  	success(function(data, status, headers, config) {
	    	$scope.info = data.info;
	  	});
	}

	$scope.isArray = function(array) {
		return Object.prototype.toString.call( array ) === '[object Array]';
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

app.controller('items', function($scope, $http, $rootScope) {

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
        $scope.options = [];
    }

    function post(data) {
    	$http.post('/api/' + user.username + '/items', data).
			success(function(data, status, headers, config) {

			});
		$rootScope.$broadcast('itemRefresh');
    }

    $scope.addOption = function() {
        $scope.options.push(0);
    };

    $scope.save = function() {
    	var item = $scope.item;
    	post({"action":"save", item });
        reset();
    };
});

app.controller('style', function($scope, $http, $rootScope) {

	load();

	function load() {
		$http.get('/api/' + user.username + '/style').
		  	success(function(data, status, headers, config) {
		    	$scope.style = data.style;
		  	});
	}

	function post(data) {
		$http.post('/api/' + user.username + '/style', data).
			success(function(data, status, headers, config) {
				$scope.style = data.style;
			});
		$rootScope.$broadcast('styleRefresh');
	}

	$scope.save = function() {
    	var style = $scope.style;
    	post({"action":"save", style });
    };

});
