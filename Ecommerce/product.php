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
        include './includes/header.php';
        include './includes/check-if-added.php';
        ?>


        <div class="container">
            <div class="jumbotron" style="margin-top: 90px">
                <h1>Welcome to our Lifestyle Store!</h1>
                <p>We have the best cameras, watches and shirts for you. No need to hunt around, wehave all in one place.</p>
            </div>

            <div class="row text-center">
                <div class="col-md-3 col-sm-3">       	
                    <div class="thumbnail"><img src="img/5.jpg" class="img-responsive" alt=""/>
                        <div class="caption">
                            <h3>Canon EOS</h3>
                            <p>Price: Rs. 36000.00</p> 
                            <?php if (!isset($_SESSION['email'])) { ?>
                                <p><a href="login.php" role="button" class="btn btn-primary btn-block">Buy Now</a></p>
                                <?php
                            } else {
                                //We have created a function to check whether this particular product is added to cart or not.
                                if (check_if_added_to_cart(1)) { //This is same as if(check_if_added_to_cart !=0)
                                    echo '<a href="#" class="btn btn-block btn-success" disabled>Added to
cart</a>';
                                } else {
                                    ?>
                                <a href="cart-add.php?id=1" name="add" value="add" class="btn btn-block
                                       btn-primary">Add to cart</a>
                                       <?php
                                   }
                               }
                               ?>

                            <p><a href="#" class="btn btn-primary btn-block" role="button">Add to cart</a></p>
                        </div>
                    </div>
                </div>          
                <div class="col-md-3 col-sm-3">       	
                    <div class="thumbnail"><img src="img/2.jpg"class="img-responsive" alt=""/>
                        <div class="caption">
                            <h3>Sony DSLR</h3>
                            <p>Price: Rs. 40000.00</p>       
                            <?php if (!isset($_SESSION['email'])) { ?>
                                <p><a href="login.php" role="button" class="btn btn-primary btn-block">Buy Now</a></p>
                                <?php
                            } else {
                                //We have created a function to check whether this particular product is added to cart or not.
                                if (check_if_added_to_cart(2)) { //This is same as if(check_if_added_to_cart !=0)
                                    echo '<a href="#" class="btn btn-block btn-success" disabled>Added to
cart</a>';
                                } else {
                                    ?>
                                    <a href="cart-add.php?id=2" name="add" value="add" class="btn btn-block
                                       btn-primary">Add to cart</a>
                                       <?php
                                   }
                               }
                               ?>

                            <p><a href="#" class="btn btn-primary btn-block" role="button">Add to cart</a></p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 col-sm-3">       	
                    <div class="thumbnail"><img src="img/3.jpg" class="img-responsive" alt=""/>
                        <div class="caption">
                            <h3>Sony DSLR</h3>
                            <p>Price: Rs. 50000.00</p>  
                            <?php if (!isset($_SESSION['email'])) { ?>
                                <p><a href="login.php" role="button" class="btn btn-primary btn-block">Buy Now</a></p>
                                <?php
                            } else {
                                //We have created a function to check whether this particular product is added to cart or not.
                                if (check_if_added_to_cart(3)) { //This is same as if(check_if_added_to_cart !=0)
                                    echo '<a href="#" class="btn btn-block btn-success" disabled>Added to
cart</a>';
                                } else {
                                    ?>
                                    <a href="cart-add.php?id=3" name="add" value="add" class="btn btn-block
                                       btn-primary">Add to cart</a>
                                       <?php
                                   }
                               }
                               ?>

                            <p><a href="#" class="btn btn-primary btn-block" role="button">Add to cart</a></p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">       	
                    <div class="thumbnail"><img src="img/4.jpg" class="img-responsive" alt=""/>
                        <div class="caption">
                            <h3>Olympus DSLR</h3>
                            <p>Price: Rs. 80000.00</p>                
                            <?php if (!isset($_SESSION['email'])) { ?>
                                <p><a href="login.php" role="button" class="btn btn-primary btn-block">Buy Now</a></p>
                                <?php
                            } else {
                                //We have created a function to check whether this particular product is added to cart or not.
                                if (check_if_added_to_cart(4)) { //This is same as if(check_if_added_to_cart !=0)
                                    echo '<a href="#" class="btn btn-block btn-success" disabled>Added to
cart</a>';
                                } else {
                                    ?>
                                    <a href="cart-add.php?id=4" name="add" value="add" class="btn btn-block
                                       btn-primary">Add to cart</a>
                                       <?php
                                   }
                               }
                               ?>

                            <p><a href="#" class="btn btn-primary btn-block" role="button">Add to cart</a></p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row text-center">
                <div class="col-md-3">       	
                    <div class="thumbnail"><img src="img/9.jpg" alt=""/>
                        <div class="caption">
                            <h3>Titan Model #301</h3>
                            <p>Price: Rs. 13000.00</p>              
                            <?php if (!isset($_SESSION['email'])) { ?>
                                <p><a href="login.php" role="button" class="btn btn-primary btn-block">Buy Now</a></p>
                                <?php
                            } else {
                                //We have created a function to check whether this particular product is added to cart or not.
                                if (check_if_added_to_cart(5)) { //This is same as if(check_if_added_to_cart !=0)
                                    echo '<a href="#" class="btn btn-block btn-success" disabled>Added to
cart</a>';
                                } else {
                                    ?>
                                    <a href="cart-add.php?id=5" name="add" value="add" class="btn btn-block
                                       btn-primary">Add to cart</a>
                                       <?php
                                   }
                               }
                               ?>

                            <p><a href="#" class="btn btn-primary btn-block" role="button">Add to cart</a></p>
                        </div>
                    </div>
                </div>          
                <div class="col-md-3">       	
                    <div class="thumbnail"><img src="img/10.jpg" alt=""/>
                        <div class="caption">
                            <h3>Titan Model #201</h3>
                            <p>Price: Rs. 3000.00</p>              
                            <?php if (!isset($_SESSION['email'])) { ?>
                                <p><a href="login.php" role="button" class="btn btn-primary btn-block">Buy Now</a></p>
                                <?php
                            } else {
                                //We have created a function to check whether this particular product is added to cart or not.
                                if (check_if_added_to_cart(6)) { //This is same as if(check_if_added_to_cart !=0)
                                    echo '<a href="#" class="btn btn-block btn-success" disabled>Added to
cart</a>';
                                } else {
                                    ?>
                                    <a href="cart-add.php?id=6" name="add" value="add" class="btn btn-block
                                       btn-primary">Add to cart</a>
                                       <?php
                                   }
                               }
                               ?>

                            <p><a href="#" class="btn btn-primary btn-block" role="button">Add to cart</a></p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">       	
                    <div class="thumbnail"><img src="img/11.jpg" alt=""/>
                        <div class="caption">
                            <h3>HMT Milan</h3>
                            <p>Price: Rs. 8000.00</p>      
                            <?php if (!isset($_SESSION['email'])) { ?>
                                <p><a href="login.php" role="button" class="btn btn-primary btn-block">Buy Now</a></p>
                                <?php
                            } else {
                                //We have created a function to check whether this particular product is added to cart or not.
                                if (check_if_added_to_cart(7)) { //This is same as if(check_if_added_to_cart !=0)
                                    echo '<a href="#" class="btn btn-block btn-success" disabled>Added to
cart</a>';
                                } else {
                                    ?>
                                    <a href="cart-add.php?id=7" name="add" value="add" class="btn btn-block
                                       btn-primary">Add to cart</a>
                                       <?php
                                   }
                               }
                               ?>

                            <p><a href="#" class="btn btn-primary btn-block" role="button">Add to cart</a></p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">       	
                    <div class="thumbnail"><img src="img/12.jpg" alt=""/>
                        <div class="caption">
                            <h3>Faber Luba #111</h3>
                            <p>Price: Rs. 18000.00</p>   
                            <?php if (!isset($_SESSION['email'])) { ?>
                                <p><a href="login.php" role="button" class="btn btn-primary btn-block">Buy Now</a></p>
                                <?php
                            } else {
                                //We have created a function to check whether this particular product is addedto cart or not.
                                if (check_if_added_to_cart(8)) { //This is same as if(check_if_added_to_cart !=0)
                                    echo '<a href="#" class="btn btn-block btn-success" disabled>Added to
cart</a>';
                                } else {
                                    ?>
                                    <a href="cart-add.php?id=8" name="add" value="add" class="btn btn-block
                                       btn-primary">Add to cart</a>
                                       <?php
                                   }
                               }
                               ?>

                            <p><a href="#" class="btn btn-primary btn-block" role="button">Add to cart</a></p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row text-center">
                <div class="col-md-3">       	
                    <div class="thumbnail"><img src="img/8.jpg"  alt="" style="width: auto"/>
                        <div class="caption">
                            <h3>HW</h3>
                            <p>Price: Rs. 800.00</p>   
                            <?php if (!isset($_SESSION['email'])) { ?>
                                <p><a href="login.php" role="button" class="btn btn-primary btn-block">Buy Now</a></p>
                                <?php
                            } else {
                                //We have created a function to check whether this particular product is addedto cart or not.
                                if (check_if_added_to_cart(9)) { //This is same as if(check_if_added_to_cart !=0)
                                    echo '<a href="#" class="btn btn-block btn-success" disabled>Added to
cart</a>';
                                } else {
                                    ?>
                                    <a href="cart-add.php?id=9" name="add" value="add" class="btn btn-block
                                       btn-primary">Add to cart</a>
                                       <?php
                                   }
                               }
                               ?>
                            <p><a href="#" class="btn btn-primary btn-block" role="button">Add to cart</a></p>
                        </div>
                    </div>
                </div>          
                <div class="col-md-3">       	
                    <div class="thumbnail"><img src="img/6.jpg" alt=""/>
                        <div class="caption">
                            <h3>Luis Phil</h3>
                            <p>Price: Rs. 1000.00</p>
                            <?php if (!isset($_SESSION['email'])) { ?>
                                <p><a href="login.php" role="button" class="btn btn-primary btn-block">Buy Now</a></p>
                                <?php
                            } else {
                                //We have created a function to check whether this particular product is addedto cart or not.
                                if (check_if_added_to_cart(10)) { //This is same as if(check_if_added_to_cart !=0)
                                    echo '<a href="#" class="btn btn-block btn-success" disabled>Added to
cart</a>';
                                } else {
                                    ?>
                                    <a href="cart-add.php?id=10" name="add" value="add" class="btn btn-block
                                       btn-primary">Add to cart</a>
                                       <?php
                                   }
                               }
                               ?>                        
                            <p><a href="#" class="btn btn-primary btn-block" role="button">Add to cart</a></p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">       	
                    <div class="thumbnail"><img src="img/13.jpg" alt=""/>
                        <div class="caption">
                            <h3>John Zok</h3>
                            <p>Price: Rs. 1500.00</p>   
                            <?php if (!isset($_SESSION['email'])) { ?>
                                <p><a href="login.php" role="button" class="btn btn-primary btn-block">Buy Now</a></p>
                                <?php
                            } else {
                                //We have created a function to check whether this particular product is addedto cart or not.
                                if (check_if_added_to_cart(11)) { //This is same as if(check_if_added_to_cart !=0)
                                    echo '<a href="#" class="btn btn-block btn-success" disabled>Added to
cart</a>';
                                } else {
                                    ?>
                                    <a href="cart-add.php?id=11" name="add" value="add" class="btn btn-block
                                       btn-primary">Add to cart</a>
                                       <?php
                                   }
                               }
                               ?>
                            <p><a href="#" class="btn btn-primary btn-block" role="button">Add to cart</a></p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">       	
                    <div class="thumbnail"><img src="img/14.jpg" alt=""/>
                        <div class="caption">
                            <h3>Jhalsani</h3>
                            <p>Price: Rs. 1300.00</p> 
                            <?php if (!isset($_SESSION['email'])) { ?>
                                <p><a href="login.php" role="button" class="btn btn-primary btn-block">Buy Now</a></p>
                                <?php
                            } else {
                                //We have created a function to check whether this particular product is addedto cart or not.
                                if (check_if_added_to_cart(12)) { //This is same as if(check_if_added_to_cart !=0)
                                    echo '<a href="#" class="btn btn-block btn-success" disabled>Added to
cart</a>';
                                } else {
                                    ?>
                                    <a href="cart-add.php?id=12" name="add" value="add" class="btn btn-block
                                       btn-primary">Add to cart</a>
                                       <?php
                                   }
                               }
                               ?>
                            <p><a href="#" class="btn btn-primary btn-block" role="button">Add to cart</a></p>
                        </div>
                    </div>
                </div>
            </div>    
        </div>
        <br><br><br>

          <?php
        require './includes/footer.php';
    ?>        
    </body>
</html>