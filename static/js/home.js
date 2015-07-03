var app = angular.module('home', ['ngRoute']);

	app.config(function($routeProvider, $locationProvider) {
		// $routeProvider
		// 	.when('/', {
		// 		controller: 'menuController'
		// 	});

		$locationProvider.html5Mode(true);
	});

	app.controller('home', function($scope, $http) {

	});