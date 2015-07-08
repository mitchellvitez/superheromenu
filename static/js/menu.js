	var app = angular.module('menu', ['ngRoute']);

	app.config(function($routeProvider, $locationProvider) {
		// $routeProvider
		// 	.when('/', {
		// 		controller: 'menuController'
		// 	});

		$locationProvider.html5Mode(true);
	});



	app.controller('menu', function($scope, $http) {

		load();
		reset();

		$scope.filters = [
        	{"name": "Vegan", "value": false},
        	{"name": "Vegetarian", "value": false},
        	{"name": "Not Spicy", "value": false},
        	{"name": "Gluten free", "value": false},
        	{"name": "No Peanuts", "value": false},
        	{"name": "No Tree Nuts", "value": false},
        	{"name": "No Milk", "value": false},
        	{"name": "No Egg", "value": false},
        	{"name": "No Wheat", "value": false},
        	{"name": "No Soy", "value": false},
        	{"name": "No Fish", "value": false},
        	{"name": "No Shellfish", "value": false}
        ];

        $scope.filterInclude = [
        	{"name": "Vegan", "value": true},
        	{"name": "Vegetarian", "value": true},
        	{"name": "Not Spicy", "value": false},
        	{"name": "Gluten free", "value": true},
        	{"name": "No Peanuts", "value": false},
        	{"name": "No Tree Nuts", "value": false},
        	{"name": "No Milk", "value": false},
        	{"name": "No Egg", "value": false},
        	{"name": "No Wheat", "value": false},
        	{"name": "No Soy", "value": false},
        	{"name": "No Fish", "value": false},
        	{"name": "No Shellfish", "value": false}
        ];

        $scope.shouldShow = function(item) {
        	if (item.filters) {
	        	for (var i = 0; i < item.filters.length; ++i) {
	        		if (JSON.parse(item.filters[i].value)) {
	        			if (JSON.parse($scope.filters[i].value) != JSON.parse($scope.filterInclude[i].value)) {
	        				return false;
	        			}
	        		}
	        		else {
	        			if (JSON.parse($scope.filters[i].value) && JSON.parse($scope.filterInclude[i].value)) {
	        				return false;
	        			}
	        		}
	        	}
	        }
        	return true;
        }

		function load() {
	        $http.get('/api/' + restaurantName).
	        	success(function(data, status, headers, config) {
				    $scope.menu = data;
			  	});
		}

		function reset() {
			$scope.query = '';
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
			// console.log($scope.menu.style);
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
