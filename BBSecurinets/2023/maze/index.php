<html>
<?php
$filelist = file("dimensions.txt");
foreach ($filelist as $file) {
	echo "<a href=\"/dimensions/$file\">$file</a><br>";
}
?>
</html>
