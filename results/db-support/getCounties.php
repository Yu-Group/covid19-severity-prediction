<?php
if(isSet($_POST['state_code'])) {

include 'db.php';

$stmt = $mysql->prepare("SELECT c.id, c.name FROM counties c LEFT JOIN states s ON s.id = c.state_id WHERE s.code='".$_POST['state_code']."'");
$stmt->execute();
$stmt->bind_result($id, $name);

while ($row = $stmt->fetch()) : ?>

<option value="<?php echo $name; ?>"><?php echo $name; ?></option>

<?php endwhile; ?>

<?php } ?>