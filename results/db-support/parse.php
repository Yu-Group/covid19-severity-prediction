<?php
if(isSet($_POST['Submit'])) {

echo 'State (Code): <strong>'.$_POST['state'].'</strong><br />'.
	 'Country: <strong>'.$_POST['county'].'</strong><br /><br />'.
	'<a href="index.php">Go back</a>';

}
?>