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
                        <li><a href="signup.php"><span class="glyphicon glyphicon-user"></span> Sign Up</a></li>
                        <li><a href="login.php"><span class="glyphicon glyphicon-log-in"></span> Login</a></li>
                    </ul>
                </div>
            </div>
        </nav>


        <div class="container">


            <div class="row_style">

                <h2>
                    Sign Up
                </h2>
                <form method="POST" action="signup_script.php">
                    <div class="form-group">
                        <input class="form-control" placeholder="Name" name="name"   pattern="^[A-Za-z\s]{1,}[\.]{0,1}[A-Za-z\s]{0,}$" required>                        </div>

                    <div class="form-group">
                        <input type="email" class="form-control"  placeholder="Email" pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$"  name="email" required>
                      </div>

                    <div class="form-group">
                        <input type="password" class="form-control" placeholder="Password" name="password" required = "true" pattern=".{6,}">
                    </div>

                    <div class="form-group">
                        <input type="tel" class="form-control" name="contact" placeholder="Contact" maxlength="10" size="10" required="true" pattern="[\+]\d{2}[\(]\d{2}[\)]\d{4}[\-]\d{4}">
                    </div>

                    <div class="form-group">
                        <input type="text" class="form-control" name="city" placeholder="City">
                    </div>

                    <div class="form-group">
                        <input type="text" class="form-control" name="address" placeholder="Address">
                    </div>
                </form>
                <div class="btn-signup">
                    <button class="btn btn-primary">Submit</button>
                </div>
            </div>

        </div>

        <?php
        include './includes/footer.php';
        ?>
    </body>
</html>
