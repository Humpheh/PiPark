<?php

/**
 * Admin page for managing the car parks.
 *
 * @author	Humphrey Shotton
 * @version	1.0 (2014-01-16)
 */

require_once ('../init.php');
require_once ('../includes/header.php');
?>

<h1>Car Park Management</h1>
<div class="row row-header">
	<div class="col-xs-1">
		ID
	</div>
	<div class="col-xs-3">
		Name
	</div>
	<div class="col-xs-4">
		Description
	</div>
	<div class="col-xs-2">
		Spaces
	</div>
	<div class="col-xs-2">
		Action
	</div>
</div>
<?php
$stmt = DB::get()->prepare('SELECT * FROM parks');
$stmt->execute();
$res = $stmt->fetchAll(PDO::FETCH_ASSOC);

foreach ($res as $row){
?>
<div class="row">
	<div class="col-xs-1">
		<?php echo $row['park_id']; ?>
	</div>
	<div class="col-xs-3">
		<?php echo $row['park_name']; ?>
	</div>
	<div class="col-xs-4">
		<?php echo $row['park_desc']; ?>
	</div>
	<div class="col-xs-2">
		<?php echo $row['park_spaces']; ?>
	</div>
	<div class="col-xs-2">
		<button type="button" onclick="updateParkField(<?php echo $row['park_id']; ?>, '<?php echo $row['park_name']; ?>', '<?php echo $row['park_desc']; ?>',
		<?php echo $row['park_spaces']; ?>)" class="btn btn-xs btn-default">
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

<script type="text/javascript">
	function updateParkField(id, name, desc, spaces) {
		$('#park_id').val(id);
		$('#park_name').val(name);
		$('#park_desc').val(desc);
		$('#park_spaces').val(spaces);
		$('#park_action').val('update');
		$('#park_form_title').html('Edit Park #' + id);
	}
</script>

<form class="form-signin" role="form" action="parkaction.php" method="POST">
	<h2 id="park_form_title" class="form-signin-heading">Add Park</h2>

	<input type="text" id="park_action" name="park_action" value="add" class="form-hidden">
	<input type="text" id="park_id" name="park_id" class="form-hidden" >

	<input type="text" id="park_name" name="park_name" class="form-control form-control-first" placeholder="Name" required="" autofocus="">
	<textarea id="park_desc" name="park_description" class="form-control" placeholder="Park Description"></textarea>
	<input type="text" id="park_spaces" name="park_spaces" class="form-control form-control-last" placeholder="Spaces" required="">
	<button class="btn btn-lg btn-primary btn-block" type="submit">
		Confirm
	</button>
</form>

<?php
require_once ('../includes/footer.php');
?>