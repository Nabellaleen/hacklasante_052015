angular
	.module('hack.controllers', [])

	.controller('SearchController', function($scope, $state, $http) {
		$scope.search = {name: '', firstname: '', lastname: '', birthyear: ''};
		$scope.search_ref = angular.copy($scope.search);

		$scope.$watch('search', function(search) {
			if (angular.equals($scope.search, $scope.search_ref))
				$scope.results = undefined;
			else
				$http.post('/;get_users', {fields: $scope.search}).then(function(result) {
					result.data.users.sort(function(b, a) { return 100 * (a.score - b.score); });
					result.data.users.splice(10, 10000)
					$scope.results = result.data.users;
				});
		}, true);

		$('#reader').html5_qrcode(
			function(data){
				console.log(data)
				$state.go('user.preview', {userId: data});
				// do something when code is read
			},
			function(error){
				//show read errors 
			}, function(videoError){
				//the video stream could be opened
			}
		);

		$scope.$on('$destroy', function() {
			$('#reader').html5_qrcode_stop();
		})
	})

	.controller('UserController', function($scope, $http, $state, $stateParams, user) {
		$scope.user = user;
		$scope.master = angular.copy($scope.user);

		$scope.isUnchanged = function() {
			return angular.equals($scope.master, $scope.user);
		};

		$scope.save = function() {
			if ($stateParams.userId == 'new')
				return $http.post('/users', {fields:$scope.user}).then(function(result) {
					$state.go('user.patient', {userId: result.data.user_id});
				});
			else
				return $http.put('/users/' + user.user_id, {fields:$scope.user}).then(function() {
					$scope.master = angular.copy($scope.user);
				});
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

