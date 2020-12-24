<?php
require "./includes/common.php";
?>
<!DOCTYPE html>
<html>
        <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" >
        

        <!--jQuery library--> 
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
        

        <!--Latest compiled and minified JavaScript--> 
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Navbar in Bootstrap</title>
        
        <link rel="stylesheet" href="css/style.css">
    
        
    </head>
<body>
      <nav class="navbar navbar-inverse navbar-fixed-top">
            <div class="container">
                <div class="navbar-header">
                    <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>                        
                    </button>
                    <a class="navbar-brand" href="index.php">Lifestyle Store</a>
                </div>
              <div class="collapse navbar-collapse" id="myNavbar">
                    <ul class="nav navbar-nav navbar-right">
                    	<li><a href="cart.php"><span class="glyphicon glyphicon-shopping-cart"></span> Cart</a></li>
                        <li><a href="settings.php"><span class="glyphicon glyphicon-user"></span> Settings</a></li>
                        <li><a href="logout.php"><span class="glyphicon glyphicon-log-in"></span> Logout</a></li>
                    </ul>
                </div>
            </div>
        </nav>
    <?php
        require './includes/header.php';
         $user_id = $_SESSION["user_id"];
         $query = "SELECT item_id FROM users_items WHERE user_id = '$user_id'";
         $result = mysqli_query($con, $query) or die(mysqli_error($con));

         while($row = mysqli_fetch_array($result)){
             $item_id = $row["item_id"];
             $query_update = "UPDATE users_items SET status = 'Confirmed' WHERE item_id = '$item_id'";            
             $result_update = mysqli_query($con, $query_update) or die(mysqli_error($con));
         }
        require 'index.php';
    ?>
<div class="content">
          <div class="container">
            <div class="col-xs-12">
              <div class="jumbotron">
                <h3 class="text-center">Thank You for Ordering from LIFESTORE!</h3>
                <h4 class="text-center">The Order will be delivered to you shortly.</h4>
                <hr>
                <h5 class="text-center">Thank you for shopping with us. <a href="product.php">Click here</a>to purchase any other item </h5>
              </div>
            </div>
          </div>
        </div>
  <?php
        require './includes/footer.php';
    ?>      
</body>
</html>
