<?php

$flag = "Securinets{4g3nts_4r3_1mP0rT4nt_m0R7y}";

if ($_SERVER['HTTP_USER_AGENT'] == 'Galactic Federation') {
	echo $flag;
} else {
	echo "
	<html>
		<head>
		</head>
		<body style=\"background: url('https://free4kwallpapers.com/uploads/wallpaper/rick-and-morty-retrowave-wallpaper-1440x900-wallpaper.jpg'); background-size:cover;\">
			<p style=\"color:white;\"> You need to be an agent of the \"Galactic Federation\" to access this site and uncover the secret. </p>
		</body>
	</html>";
}

?>
