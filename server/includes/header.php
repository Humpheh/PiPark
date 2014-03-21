<!DOCTYPE HTML>
<html>
	<head>
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<link href="<?php echo Conf::URL_BASE; ?>bootstrap/css/bootstrap.min.css" rel="stylesheet">
		<title><?php echo Conf::TITLE; ?></title>
		<link href="<?php echo Conf::URL_BASE; ?>style.css" rel="stylesheet">
		<link rel="icon" type="image/png" href="<?php echo Conf::URL_BASE; ?>favicon.png">
	</head>
	<body>
		<nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
			<div class="container">
				<div class="navbar-header">
					<button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
						<span class="sr-only">Toggle navigation</span>
						<span class="icon-bar"></span>
						<span class="icon-bar"></span>
						<span class="icon-bar"></span>
					</button>
					<a href="<?php echo Conf::URL_BASE; ?>">
                        <img src="<?php echo Conf::URL_BASE; ?>logo.png" class="logo" alt="<?php echo Conf::TITLE; ?>">
                    </a>
				</div>
				<div class="collapse navbar-collapse">
					<ul class="nav navbar-nav">
						<li <?php if(!isset($nav_selected)) echo 'class="active"'; ?>>
							<a href="<?php echo Conf::URL_BASE; ?>">Home</a>
						</li>
						<li <?php if(isset($nav_selected) && $nav_selected == 1) echo 'class="active"'; ?>>
							<a href="<?php echo Conf::URL_BASE; ?>admin/parks.php">Park Management</a>
						</li>
					</ul>
				</div><!--/.nav-collapse -->
			</div>
		</nav>

		<div class="container">
			<ol class="breadcrumb">
			  <li><a href="<?php echo Conf::URL_BASE; ?>">Home</a></li>
			  <?php if(isset($breadcrumb)) echo $breadcrumb; ?>
			</ol>