angular.module('listapp', [])
.value('Words', ["apple", "berry", "cherry", "durian"])
.controller('ListController', function($scope, Words) {
    var myitems = Words[Math.floor(Math.random() * Words.length)];



  //   $http.get("/list.json").then(function(response) {
  //     $scope.myitems = response.data.items;
    
  //     console.log($scope.myitems);
  // });
});
