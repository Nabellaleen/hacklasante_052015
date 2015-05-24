angular
	.module('hack.controllers', [])

	.controller('SearchController', function($scope, $http) {
		$scope.search = {};

		var first = true

		$scope.$watch('search', function(search) {
			if (first) {
				first = false
				return;
			}

			$http.post('/;get_users', {fields: $scope.search}).then(function(result) {
				result.data.users.sort(function(a, b) { return 100 * (a.score - b.score); });
				$scope.results = result.data.users;
			});
		}, true);
	})
	
	.controller('UserController', function($scope, $http, user) {
		$scope.user = user;
		
		$scope.save = function() {
			$http.put('/users/' + user.user_id, $scope.user)
		};

		// $scope.delete = function() {
		// 	$http.delete('/')
		// };
	})
	
	.controller('UserPreviewController', function($scope) {
	})
	
	.controller('UserPatientController', function($scope) {
	})
	
	.controller('UserMeetingController', function($scope) {
	})
	
	.controller('UserMergeController', function($scope, users) {
		$scope.results = users.filter(function(result) {
			return $scope.user.user_id !== result.user.user_id;
		});
	})
	
	.controller('UserRemoveController', function($scope) {

	});

