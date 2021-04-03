TestApp = angular.module('TestApp', ['TestApp.controllers', 'smart-table']);	
angular.module('TestApp.controllers', []).controller('testController',  ['$scope', '$http', function($scope, $http) {
	$scope.loading = false;
	$scope.getData = function() {
		$scope.loading = true;
		$http.get("https://coderszine.com/demo/rest-api/v1/employee/read")
		.then(function(response){
			$scope.employees = response.data;
			$scope.loading = false;
		});
	}
	$scope.getData();
}]);