<?php
/* CREATE THE TABLES AND FILL THEM */

set_time_limit(5000);

include 'db.php';

echo '<strong>Importing...Please wait...</strong><br /><br />';

flush();
sleep(2);

/* Create table `states` */

$sql_create_states = 'CREATE TABLE IF NOT EXISTS `states` (
  `id` int(11) NOT NULL auto_increment,
  `code` char(5) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=52;';

echo $sql_create_states."<br /><br />";

$mysql->query($sql_create_states);

/* Create table `counties` */

$sql_create_counties = 'CREATE TABLE IF NOT EXISTS `counties` (
  `id` int(11) NOT NULL auto_increment,
  `state_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3114;';

echo $sql_create_counties."<br /><br />";

$mysql->query($sql_create_counties);


/* Fill both tables */

$lines = file('to-insert.txt');

foreach($lines as $query) {
	if($query) {
		echo $query."<br />";
$mysql->query($query);
	}
}
?>