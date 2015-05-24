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
	
	.controller('UserController', function($scope, $http, $stateParams, user) {
		$scope.user = user;
		
		$scope.save = function() {
			if ($stateParams.userId == 'new')
				return $http.post('/users', $scope.user).then(function(user) {
					console.log(user)
				});
			else
				return $http.put('/users/' + user.user_id, $scope.user)
		};
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
	
	.controller('UserConsolidateController', function($scope, $http, $state, other) {
		$scope.other = other;
		
		$scope.consolidate = function() {
			for (var key in $scope.user)
				if (!$scope.user[key] && $scope.other[key])
					$scope.user[key] = $scope.other[key];
			
			$http.delete('/users/' + $scope.other.user_id).then(function() {
				$scope.save();

				$state.go('user.preview')
			});
		}
	});

