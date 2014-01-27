<!DOCTYPE HTML>
<html>
	<head>
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<link href="<?php echo Conf::URL_BASE; ?>bootstrap/css/bootstrap.min.css" rel="stylesheet">
		<title><?php echo Conf::TITLE; ?></title>
		<link href="<?php echo Conf::URL_BASE; ?>style.css" rel="stylesheet">
	</head>
	<body>
		<div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
			<div class="container">
				<div class="navbar-header">
					<button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
						<span class="sr-only">Toggle navigation</span>
						<span class="icon-bar"></span>
						<span class="icon-bar"></span>
						<span class="icon-bar"></span>
					</button>
					<a class="navbar-brand" href="<?php echo Conf::URL_BASE; ?>"><?php echo Conf::TITLE; ?></a>
				</div>
				<div class="collapse navbar-collapse">
					<ul class="nav navbar-nav">
						<li class="active">
							<a href="<?php echo Conf::URL_BASE; ?>">Home</a>
						</li>
						<li>
							<a href="<?php echo Conf::URL_BASE; ?>admin/parks.php">Park Management</a>
						</li>
					</ul>
				</div><!--/.nav-collapse -->
			</div>
		</div>

		<div class="container">
