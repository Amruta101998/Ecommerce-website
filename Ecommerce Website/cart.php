<?php
require "./includes/common.php";
?>
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

        <?php
        require './includes/header.php';
        ?>
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

        <div class="container">
            <br><br><br><br>
            <div class="table-responsive" style="margin-left: 300px; margin-right: 300px">

                <table class="table table-striped">
                   <?php
                   $sum = 0;
                    $user_id = $_SESSION['user_id'];
                    $query = "SELECT items.price AS Price, items.pid, items.name AS Name FROM users_items JOIN items ON users_items.item_id = items.pid WHERE users_items.id='$user_id' and status='Added To Cart'";
                    $result = mysqli_query($con, $query)or die($mysqli_error($con));
                    if (mysqli_num_rows($result) == 0) {
                        echo "Add items to the cart first!";
                        ?>
                        } else {
                        <thead>	
                            <tr>
                                <th>Item Number</th>
                                <th>Item Name</th>
                                <th>Price</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php
                            while ($row = mysqli_fetch_array($result)) {
                                $sum += $row["Price"];
                                $id = $row["pid"];
                                echo "<tr><td>" . "#" . $row["pid"] . "</td><td>" . $row["Name"] . "</td><td>Rs " . $row["Price"] . "</td><td><a href='cart-remove.php?id={$row['pid']}' class='remove_item_link btn btn-danger btn-block'> Remove</a></td></tr>";
                            }
                            if (isset($disc)) {
                                $sum = $sum - $sum * (0.2);
                            }
                            echo "<tr><td></td><td>Total</td><td>Rs " . $sum . "</td><td><a href='success.php' class='btn btn-success btn-block'>Confirm Order</a></td></tr>";
                            ?>
                        </tbody>
                        <?php
                    }
                    ?>
                    <?php
                    ?>
                </table>
            </div>
        </div>
        <br>       
        <?php
        require './includes/footer.php';
        ?> 

    </body>
</html>