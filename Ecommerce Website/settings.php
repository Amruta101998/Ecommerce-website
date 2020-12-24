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
        <link rel="stylesheet" href="../bootstrap/bootstrap-3.3.7-dist/css/bootstrap-theme.css" type="text/css"/>

    
        
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
        
                
            <div class="container">
                
                
                <div class="row_style">
                    
                    <h3>
                        Change Password
                    </h3>
                    <form action="settings-script.php" method="POST">
                  <div class="form-group">
                    <label for="oldPassword">Old Password</label>
                    <input type="password" class="form-control" name="oldPassword" requiredvalue="<?php echo $password; ?>">                    
                  </div>
                  <div class="form-group">
                    <label for="newPassword">New Password</label>
                    <input type="password" class="form-control" name="newPassword" required value="<?php echo $newPassword; ?>">
                  </div>
                  <div class="form-group">
                    <label for="newPasswordRe">Re-type New Password</label>
                    <input type="password" class="form-control" name="newPasswordRe" required value="<?php echo $newPasswordRe; ?>">                    
                  </div>
                 <input type="submit" class="btn btn-setting btn-block" value="Confirm">
                </form>
                </div>
           </div>
          
    
   <?php
        require './includes/footer.php';
    ?> 
</body>
</html>
