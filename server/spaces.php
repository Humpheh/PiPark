<?php

/**
 * Page for showing car parking spaces
 *
 * @author	Humphrey Shotton
 * @version	1.0 (2014-01-16)
 */

require_once ('init.php');

// Get the ID of the carpark through the GET request.
$id = intval($_GET['id']);

// Check the ID exists and get park information.
$pstmt = DB::get()->prepare("SELECT *, (SELECT count(*) FROM spaces WHERE space_park_id = park_id) AS ps, 
	(".get_num_space_query("park_id").") AS spaces FROM parks WHERE park_id = ?");
$pstmt->bindValue(1, $id, PDO::PARAM_INT);
$pstmt->execute();

// Go back to homepage if carpark does not exist on database.
if ($pstmt->rowCount() != 1){
	header ('Location: '.Conf::URL_BASE);
	exit();
}

// Get the carpark data
$park = $pstmt->fetch(PDO::FETCH_ASSOC);

require_once ('includes/header.php');

?>

<a class="btn btn-default" href="<?php echo Conf::URL_BASE; ?>">Back</a>

<h1><?php print $park['park_name']; ?> <span class="small"><?php print $park['ps']; ?> Spaces (<b><?php print $park['ps'] - $park['spaces']; ?> Available)</b></span></h1>

<p><?php print $park['park_desc']; ?></p>


<div class="row row-header">
	<div class="col-xs-3">Space</div>
	<div class="col-xs-4">Status</div>
	<div class="col-xs-4">Last Updated</div>
	<div class="col-xs-1">ID</div>
</div>

<?php
/*
Alternative Query
$query = "SELECT  a.*, c.*
		FROM updates a
        INNER JOIN
        (
            SELECT update_space_id, MAX(update_time) max_date
            FROM    updates
            GROUP BY update_space_id
        ) b ON a.update_space_id = b.update_space_id AND
                a.update_time = b.max_date
        LEFT JOIN spaces c ON space_id = a.update_space_id
        WHERE space_park_id = ".$id;*/

// Get the status of the car parking spaces
$query = "SELECT * 
		FROM spaces a
		LEFT JOIN (
			SELECT *
			FROM updates
			WHERE update_time = (
				SELECT max( update_time )
				FROM updates um
				WHERE um.update_id = update_id
			)
			GROUP BY update_space_id
		) b ON a.space_id = b.update_space_id
		WHERE space_park_id = ".$id;

$stmt = DB::get()->query($query);
$rows = $stmt->fetchAll(PDO::FETCH_ASSOC);

// Print the information about the spaces
$i = 0;
foreach ($rows as $row){
	$i++;
	?>
	<div class="row">
		<div class="col-xs-3"><?php echo $i; ?></div>
		<div class="col-xs-4"><?php echo $row['update_status'] == 0 ? '<span class="alert alert-small alert-success">Empty</span>' : '<span class="alert alert-small alert-danger">Filled</span>'; ?></div>
		<div class="col-xs-4"><?php echo isset($row['update_time']) ? ago($row['update_time']) : 'Never'; ?></div>
		<div class="col-xs-1"><?php echo 'pi'.$row['space_pi_id'].'-'.$row['space_area_code']; ?></div>
	</div>
	<?php
}

require_once ('includes/footer.php');
?>