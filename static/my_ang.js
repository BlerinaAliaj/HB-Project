//  Angular code for application Hiker

var lists = angular.module('lists', []);
var trips = angular.module('trips', []);
var hiker = angular.module('hiker', ['lists', 'trips']);

// Code loads all the trips that a user has taken or will take
trips.controller('ListLatestTrips', function ($scope, $http) {
    $http.get("/list_trips").then(function(response) {
      $scope.mytrips = response.data.trips;
      // console.log($scope.mytrips);
    });
});


// Code loads all list items and updates them //
lists.controller('ListController', function($scope, $http) {
    $scope.listData = {};
    $scope.listData['tripCode'] = tripCode;

    var config = {headers: {'trip_code': tripCode}};
    $http.get("/list.json", config).then(function(response) {
        $scope.itemDetails = response.data.items;
        $scope.userDetails = response.data.users;

        $scope.usernames = [];

        $scope.userDetails.forEach(function(userDetail){
            $scope.usernames.push({"userName": userDetail[0],
                                   "userID": userDetail[1]
            });
        });
        
        console.log($scope.usernames);


        $scope.addAll = function(itemDetail, addItem) {
                $scope.mydata = [];
                $scope.newdata = [];

            $scope.itemDetails.forEach(function(itemDetail) {
                $scope.mydata.push({"description": itemDetail.description,
                                                "userid": itemDetail.userid,
                                                "completed": itemDetail.selected,
                                                "list_id": itemDetail.item_id});
                                    });
            if (!addItem.description || !addItem.userid) {
                addItem.description = "";
                addItem.userid = "";
            }
            $scope.newdata.push({"description": addItem.description,
                                            "userid": addItem.userid,
                                            "completed": addItem.selected,
                                            "list_id": "newItem"});

            // console.log($scope.mydata);
            // console.log($scope.newdata);

            $scope.listData["data"] = angular.toJson($scope.mydata);
            $scope.listData["newdata"] = angular.toJson($scope.newdata);
            console.log($scope.listData);

            $http.post("/list.json", $scope.listData).then(function(response) {
                $scope.itemDetails = response.data.items;
                // $scope.addItem.$setPristine();

                $scope.addItem.description = "";
                $scope.addItem.userid = "";
                $scope.addItem.completed= false;
                });

            };
      });
});