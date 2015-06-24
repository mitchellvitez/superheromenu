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

app.controller('addCategory', function($scope, $http) {

	$http.get('/api/' + user.username + '/categories').
	  	success(function(data, status, headers, config) {
	    	console.log(data);
	    	$scope.categories = data;
	  	}).
	  	error(function(data, status, headers, config) {
	    	$scope.categories = [];
	  	});

	function reset() {
		$scope.newCategory = '';
	}

	reset();

	// TODO post this data for the added category to a relevant API endpoint
    // $http.post(url, data); 
	function save(data) {
		// takes in array of categories like: ['Appetizers', 'Salad', 'Dessert']

	}

	$scope.addAndSaveCategory = function() {
        $scope.categories.push($scope.newCategory);
        save($scope.categories);
        reset();
    };

    $scope.remove = function(category) {
    	console.log(category);
    	var index = $scope.categories.indexOf(category);
    	if (index !== -1) {
    		$scope.categories.splice(index, 1);
    	}
    	save($scope.categories);
    };
});

app.controller('addItem', function($scope, $http) {


	$http.get('/api/' + user.username + '/categories').
	  	success(function(data, status, headers, config) {
	    	console.log(data);
	    	$scope.categories = data;
	  	}).
	  	error(function(data, status, headers, config) {
	    	$scope.categories = [];
	  	});

	function reset() {
    	$scope.item = {};
        $scope.options = [];
    }

	reset();

    $scope.addOption = function() {
        $scope.options.push(0);
    };

    $scope.saveItem = function() {
    	var data = $scope.item;
        console.log(data);
        reset();
        // TODO post this data for the added item to a relevant API endpoint
        // $http.post(url, data);  
    };

    
});
