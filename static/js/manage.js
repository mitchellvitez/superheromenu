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
	$scope.menus = ['Main Menu', 'Wine List', 'Dessert Menu'];
});

app.controller('addItem', function($scope, $http) {
	$scope.categories = ['Appetizers', 'Salad', 'Dessert'];
	function reset() {
    	$scope.item = {};
    	// $scope.item.category = $scope.categories[0];
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
        // $http.post(url, data);  
    };

    
});
