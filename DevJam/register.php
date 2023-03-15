<?php

$regno= $_POST['regno'];
$email = $_POST['email'];
$pswd=$_POST['pswd'];

if (!empty($regno) || !empty($email) || !empty($pswd))
{

    $host="localhost";
    $dbusername="root";
    $dbpassword="";
    $dbname="project";




//Creating a connection

$conn= new mysqli ($host, $dbusername, $dbpassword, $dbname);

if(mysqli_connect_error()){
    die('Connect Error('.mysqli_connect_error() .')'. mysqli_connect_error());

}

else{
    $SELECT= "SELECT email from register Where email= ? Limit 1";
    $INSERT= "INSERT INTO register(regno, email, pswd) values(?,?,?)";

    //Prepare Statement
    $stmt= $conn->prepare($SELECT);
    $stmt->bind_param("s", $email);
    $stmt->execute();
    $stmt->bind_result($email);
    $stmt->store_result();
    $rnum = $stmt->num_rows;

    //checking the username;
    if($rnum==0){
        $stmt-->close();
        $stmt= $conn-->prepare($INSERT);
        $stmt-->bind_param("sss",$regno, $email, $pswd);
        $stmt-->execute();
        echo "New record inserted successfully";

    }
    else{
        echo "Someone already registred using this Email";
    }
    $stmt->close();
    $conn->close();
    }



}else{
    echo "All fields are required";
    die();
}
?>