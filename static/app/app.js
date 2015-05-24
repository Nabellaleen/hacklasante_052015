angular
	.module('hack.app', ['ui.router', 'hack.controllers'])

	.config(function($stateProvider, $urlRouterProvider) {

		$urlRouterProvider.otherwise('/');

		$stateProvider
			.state('search', {
				url: "/",
				controller: 'SearchController',
				templateUrl: "/static/templates/search.html"
			})

			.state('user', {
				abstract: true,
				url: "/user/:userId",
				controller: "UserController",
				templateUrl: '/static/templates/user-menu.html',
				resolve: {
					user: function($http, $stateParams) {
						return $http.get('/users/' + $stateParams.userId).then(function(user) {
							return user.data;
						})
					}
				}
			})

			.state('user.preview', {
				url: "/preview",
				controller: "UserPreviewController",
				templateUrl: '/static/templates/user-preview.html',
			})

			.state('user.patient', {
				url: "/patient",
				controller: "UserPatientController",
				templateUrl: '/static/templates/user-patient.html',
			})

			.state('user.meetings', {
				url: "/meeting",
				controller: "UserMeetingController",
				templateUrl: '/static/templates/user-meeting.html',
			})

			.state('user.merge', {
				url: "/merge",
				controller: "UserMergeController",
				templateUrl: '/static/templates/user-merge.html',
				resolve: {
					users: function($http, user) {
						return $http.post('/;get_users', {fields: user}).then(function(result) {
							result.data.users.sort(function(a, b) { return 100 * (a.score - b.score); });
							return result.data.users;
						});
					}
				}
			})

			.state('user.consolidate', {
				url: "/consolidate/:otherId",
				controller: "UserConsolidateController",
				templateUrl: '/static/templates/user-consolidate.html',
				resolve: {
					other: function($http, $stateParams) {
						return $http.get('/users/' + $stateParams.otherId).then(function(user) {
							return user.data;
						})
					}
				}
			})			
	})

	.run(function($rootScope, $state) {

		$rootScope.$on('$stateChangeError', function(event, toState, toParams, fromState, fromParams, error) {
			console.log(error)
			console.log(error.stack)
		});
	})
	
