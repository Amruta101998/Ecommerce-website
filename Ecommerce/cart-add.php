<?php
    require("./includes/common.php");
    if (isset($_GET['id']) && is_numeric($_GET['id'])) {
        $item_id = $_GET['pid'];
        $user_id = $_SESSION['user_id'];

        $query = "INSERT INTO users_items (user_id,item_id,status) VALUES ('$user_id','$item_id','Added To Cart')";

        $result = mysqli_query($con,$query) or die(mysqli_error($con));

        header("location:product.php");
        
    }
?>   