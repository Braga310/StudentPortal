<?php

session_start();
header('location:navigation.html');


$con= mysqli_connect('localhost', 'root');
if($con){
    echo "connection successful";
}else{
    echo "no connection";
}
mysqli_select_db($con, 'project2');

$regNo= $_POST['regNo'];
$pass= $_POST['password'];
$email= $_POST['email'];
$q= "select * from login where regNo= '$regNo' && password='$pass' && email='$email' ";

$result=mysqli_query($con, $q);
 
$num = mysqli_num_rows($result);

if($num ==1){
    echo "duplicate data";
}else{
    $qy = "insert into login(regNo,email,password) values('$regNo','$email','$pass')";
    mysqli_query($con, $qy);
}



?>