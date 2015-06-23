	var menu = angular.module('menu', ['ngRoute']);

	menu.config(function($routeProvider, $locationProvider) {
		$routeProvider
			.when('/', {
				controller: 'menuController'
			});

		console.log("test");
		$locationProvider.html5Mode(true);
	});

	menu.controller('menuController', function($scope, $http) {
		console.log("menu controller activated");
		$scope.menu = null;
        $http.get('//vitez.me/rest2/carsons.json')
		  .success(function(data, status, headers, config) {
		    // this callback will be called asynchronously
		    // when the response is available
		    console.log(data);
		    $scope.menu = data;
		  })
		  .error(function(data, status, headers, config) {
		    // called asynchronously if an error occurs
		    // or server returns response with an error status.
		  });
	});
