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
			    console.log(data);
			    $scope.menu = data;
		  	});
	});
