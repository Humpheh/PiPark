<?php

/**
 * Main page for car parking website.
 *
 * @author	Humphrey Shotton
 * @version	1.0 (2014-01-19)
 */

require_once ('init.php');
require_once ('includes/header.php');
?>
<h1>Car Parks</h1>
<div class="row row-header">
	<div class="col-sm-3 col-xs-4">
		Name
	</div>
	<div class="col-sm-4 col-xs-5">
		Description
	</div>
	<div class="col-sm-2 col-xs-3">
		Spaces
	</div>
	<div class="col-sm-3 hidden-xs">
		Capacity
	</div>
</div>

<?php
$stmt = DB::get()->prepare('SELECT *, (SELECT count(*) FROM spaces WHERE space_park_id = p.park_id) AS ps, 
			('.get_num_space_query("p.park_id").') AS spaces FROM parks p');
$stmt->execute();
$res = $stmt->fetchAll(PDO::FETCH_ASSOC);

foreach ($res as $row){	?>
	<a href="<?php echo Conf::URL_BASE; ?>spaces.php?id=<?php echo $row['park_id']; ?>">
	<div class="row">
		<div class="col-sm-3 col-xs-4">
			<?php echo $row['park_name']; ?>
		</div>
		<div class="col-sm-4 col-xs-5">
			<?php echo $row['park_desc']; ?>
		</div>
		<div class="col-sm-2 col-xs-3">
			<?php echo $row['ps'] - $row['spaces']; ?> spaces <span class="small" style="color:gray;">/ <?php echo $row['ps']; ?></span>
		</div>
		<div class="col-sm-3 col-xs-12">
			<div class="progress">
	        	<div class="progress-bar" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" 
	        			style="width: <?php echo ($row['spaces']/$row['ps'])*100;?>%;"><?php echo $row['spaces'].' / '.$row['ps']; ?> used</div>
	        </div>
		</div>
	</div>
	</a>
<?php
}

require_once ('includes/footer.php');
?>