<?php

require "./includes/common.php";

$email= $_POST["email"];
$email = mysqli_real_escape_string($con, $email);

$password = $_POST['password'];
$password = mysqli_real_escape_string($con, $password);
$password = md5($password);

$select_query = "SELECT id , email from users WHERE email = '$email' AND password = '$password'";
$select_query_result = mysqli_query($con, $select_query) or die(mysqli_error($con));
if (mysqli_num_rows($select_query_result) == 0) {
    $error = "<span class='red'>Invalid Credentials</span>";
    header("location:login.php=" . $error);
} else {
    mysqli_fetch_array($select_query_result);
    $_SESSION['email'] = $email;
    $_SESSION['user_id'] = $row['id'];
    header("location:product.php");
}
?>
 