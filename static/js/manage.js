// 	How to post json data to a url and do something with the result
//	var res = $http.post('/save_json', dataObj);
// 	res.success(function(data, status, headers, config) {
// 		$scope.message = data;
// 	});
// 	res.error(function(data, status, headers, config) {
// 			alert( "failure message: " + JSON.stringify({data: data}));
// 		});

var app = angular.module('manager', ['ngRoute']);

console.log(user.username);
user.username = 'carsons';

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
	    	console.log(data);
	    	$scope.menus = data;
	  	}).
	  	error(function(data, status, headers, config) {
	    	$scope.menus = [];
	  	});
});

app.controller('categories', function($scope, $http) {

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
	}

	$scope.add = function(categoryName) {
        $scope.categories.push({"name": categoryName});
        post( {"action":"save", "category":{"name": categoryName}} );
        reset();
    };

    $scope.remove = function(category) {
    	if (! confirm('Are you sure you want to remove the category ' + category.name + '? This may alter or even delete the items in it.')) {
    		return;
    	}

    	var index = $scope.categories.indexOf(category);
    	if (index !== -1) {
    		$scope.categories.splice(index, 1);
    	}

    	post({"action":"delete", category});
    };
});

app.controller('items', function($scope, $http) {

	load();
	reset();

	function load() {
		$http.get('/api/' + user.username + '/categories').
	  	success(function(data, status, headers, config) {
	    	$scope.categories = data.categories;
	  	});
	}

	function reset() {
    	$scope.item = {};
        $scope.options = [];
    }

    function post(data) {
    	console.log(data);
    	$http.post('/api/' + user.username + '/items', data).
			success(function(data, status, headers, config) {
				console.log(data);
			});
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
