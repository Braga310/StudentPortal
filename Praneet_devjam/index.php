<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "results";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
	$student_id = $_POST["student_id"];

	$conn = new mysqli($servername, $username, $password, $dbname);

	if ($conn->connect_error) {
		die("Connection failed: " . $conn->connect_error);
	}

	$sql = "SELECT * FROM students WHERE id = $student_id";
	$result = $conn->query($sql);

	if ($result->num_rows > 0) {
		$row = $result->fetch_assoc();
		$student_name = $row["name"];

		$sql = "SELECT * FROM results WHERE student_id = $student_id";
		$result = $conn->query($sql);

		$results = array();
		if ($result->num_rows > 0) {
			while($row = $result->fetch
