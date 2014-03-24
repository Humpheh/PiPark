<?php

/**
 * Admin page for managing the car parks.
 *
 * @author	Humphrey Shotton
 * @version	1.1 (2014-03-21)
 */

require_once ('../init.php');

$nav_selected = 1;
$breadcrumb = '<li class="active">Park Management</li>';
require_once ('../includes/header.php');
?>

<h1><span class="glyphicon glyphicon-wrench"></span> Car Park Management</h1>

<div class="tbrow block">
	<div class="row row-header">
		<div class="col-xs-1">
			ID
		</div>
		<div class="col-xs-2">
			Name
		</div>
		<div class="col-xs-3">
			Description
		</div>
		<div class="col-xs-2">
			Location
		</div>
		<div class="col-xs-2">
			Spaces
		</div>
		<div class="col-xs-2">
			Action
		</div>
	</div>
	<?php

	$stmt = DB::get()->prepare('SELECT *,
		(SELECT count(*) FROM spaces WHERE space_park_id = park_id) AS park_spaces FROM parks');
	$stmt->execute();
	$res = $stmt->fetchAll(PDO::FETCH_ASSOC);

	foreach ($res as $row){
	?>
	<div class="row">
		<div class="col-xs-1">
			<?php echo $row['park_id']; ?>
		</div>
		<div class="col-xs-2">
			<a href="<?php echo Conf::URL_BASE; ?>spaces.php?id=<?php echo $row['park_id']; ?>">
                <?php echo $row['park_name']; ?>
            </a>
		</div>
		<div class="col-xs-3">
			<?php echo $row['park_desc']; ?>
		</div>
		<div class="col-xs-2">
			<?php echo $row['park_location'] == null ? '<span class="badge">not set</span>' : $row['park_location']; ?>
		</div>
		<div class="col-xs-2">
			<?php echo $row['park_spaces']; ?>
		</div>
		<div class="col-xs-2">
			<button type="button" onclick="updateParkField(<?php echo $row['park_id']; ?>, '<?php echo $row['park_name']; ?>', '<?php echo $row['park_desc']; ?>', 
			<?php echo $row['park_spaces']; ?>, '<?php echo $row['park_location']; ?>')" class="btn btn-xs btn-default">
				Edit
			</button>
			<button type="button" onclick="$('#del-confirm-<?php echo $row['park_id']; ?>').show();" class="btn btn-xs btn-danger">
				Delete
			</button>
			<form id="del-confirm-<?php echo $row['park_id']; ?>"  style="display:none;" action="parkaction.php" method="POST">
				<input type="text" value="<?php echo $row['park_id']; ?>" name="park_id" class="form-hidden" style="display:none;">
				<input type="text"  name="park_action" value="delete" style="display:none;">
				<button type="button" onclick="submit();" class="btn btn-xs btn-danger" >
					Confirm Delete
				</button>
			</form>
		</div>
	</div>
	<?php
	}
	?>
</div>

<script type="text/javascript">
	function updateParkField(id, name, desc, spaces, location) {
		$('#park_id').val(id);
		$('#park_name').val(name);
		$('#park_desc').val(desc);
		$('#park_spaces').val(spaces);
		$('#park_location').val(location);
		$('#park_action').val('update');
		$('#park_form_title').html('Edit Park #' + id);
	}
</script>

<form class="form-signin" role="form" action="parkaction.php" method="POST">
	<h2 id="park_form_title" class="form-signin-heading">Add Park</h2>

	<input type="text" id="park_action" name="park_action" value="add" class="form-hidden">
	<input type="text" id="park_id" name="park_id" class="form-hidden" >

	<input type="text" id="park_name" name="park_name" class="form-control form-control-first" placeholder="Name" required="" autofocus="">
	<textarea id="park_desc" name="park_description" class="form-control form-control-last" placeholder="Park Description"></textarea>
	
	<input type="text" id="park_location" name="park_location" class="form-control form-control-first form-control-last" placeholder="Location">
	
	<button class="btn btn-lg btn-primary btn-block" type="submit">
		Confirm
	</button>
</form>

<?php
require_once ('../includes/footer.php');
?>