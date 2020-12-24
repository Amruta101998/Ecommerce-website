<?php
require "./includes/common.php";
 if (isset($_SESSION['email']))
                      { 
                      header('location: product.php');
                      } 
?>
 <!DOCTYPE html>
<!--
To change this license header, choose License Headers in Project Properties.
To change this template file, choose Tools | Templates
and open the template in the editor.
-->
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
       <body>
        <?php
        include './includes/header.php';
        ?>
        
             <div id="banner_image">
    		<div class="container">
                        <div>
                    	<center>
                  <div id="banner_content">                  	
                    <h1>We sell lifestyle.</h1>
                    <p>Flat 40% OFF on premium brands</p>
                    <br/>
                    <a href="product.php" class="btn btn-danger btn-lg active">Shop Now</a>                                        
                  </div>
                  </center>                
            </div>
        </div>
        </div>
   
    <body>
        <?php
        include './includes/footer.php';
        ?>       
</body>
</html>
