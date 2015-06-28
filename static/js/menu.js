	var app = angular.module('menu', ['ngRoute']);

	app.config(function($routeProvider, $locationProvider) {
		// $routeProvider
		// 	.when('/', {
		// 		controller: 'menuController'
		// 	});

		$locationProvider.html5Mode(true);
	});

	app.controller('menu', function($scope, $http) {
        $http.get('/api/' + restaurantName).
        	success(function(data, status, headers, config) {
			    $scope.menu = data;
		  	});

		$scope.getElement = function(elementName) {
			var idx = indexOf($scope.menu.style, "name", elementName);
			if (idx == -1) {
				return "null";
			}
			return $scope.menu.style[idx].value;
		}

		function indexOf(array, key, value) {
 
			for (var i = 0; i < array.length; i++) {
				if (array[i][key] == value)
					return i;
			}

			return -1;
		}

	});
