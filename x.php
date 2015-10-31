<!DOCTYPE HTML>

<html>
	<head>
		<title>Latest Results</title>
		<meta http-equiv="content-type" content="text/html; charset=utf-8" />
		<meta name="description" content="" />
		<meta name="keywords" content="" />
		<!--[if lte IE 8]><script src="js/html5shiv.js"></script><![endif]-->
		<script src="js/jquery.min.js"></script>
		<script src="js/skel.min.js"></script>
		<script src="js/skel-layers.min.js"></script>
		<script src="js/init.js"></script>
		<noscript>
			<link rel="stylesheet" href="css/skel.css" />
			<link rel="stylesheet" href="css/style.css" />
			<link rel="stylesheet" href="css/style-xlarge.css" />
		</noscript>
	<script src="jquery-1.11.3.js"></script>
	<script>
		function varyNum() {
			var password = prompt("For full admin privledges, please enter password");
			
			if (password=="") {
				$("#sub2").load("myAjax1.php");
			}
		}
	</script>
	</head>
	<body id="top">

		<!-- Header -->
			<header id="header" class="skel-layers-fixed">
				<h1><a href="#">UFT Testing</a></h1>
				<nav id="nav">
					<ul>
						<li><a href="teg.php">Home</a></li>
						<li><a href="yyy.php">Search Database</a></li>
						<li><a href="x.php">Latest Results</a></li>
						<li><a href="w.php">All Results</a></li>
						<li><button class="button special" button onclick="varyNum()">Admin Priv</a></li>
					</ul>
				</nav>
			</header>

		<!-- Main -->
			<section id="main" class="wrapper style1">
				<header class="major">
					<h2>Latest Results</h2>
					<p>Select the number of results using the dropbox</p>
				</header>
				<div class="container">
					<div id="sub2" class="row">
					    <p>
						<form action="x.php" method='post'>
						<select name="number">
							<option value="">--Select--</option>
							<option value="10">10</option>
							<option value="15">15</option>
							<option value="25">25</option>
							<option value="50">50</option>
							<option value="100">100</option>
						</select>
						<input type="submit" name="submit"/>
						</form>
						</p>
					</ul>
					<?php
					// Check connection 
					$con=mysqli_connect("host","","","");  //enter in the passwords and whatnot
					if (mysqli_connect_errno()) {
						echo "Failed to connect to MySQL: " . mysqli_connect_error();
					}

					//Send MySQL command to resort the table by date/time
					$sql1 = "ALTER TABLE test2 ORDER BY DateTime DESC";
					if (mysqli_query($con, $sql1) === TRUE) {
						//echo "New records created successfully";
					} else {
						echo "Error: " . $sql1 . "<br>" . $con->error;
					}
					
					$result = mysqli_query($con,"SELECT * FROM test2"); //info is currently stored in test2 table
					
					$amount = 10;
				//default if num is 10 but you can reload the page with more
				//depending on the number selected
					if(isset($_POST['number'])) {	//draw on the value in the dropbox if not empty
						$amount = $_POST['number'];
					}
					
					echo "<table border='1'>
					<tr>
					<th>Project Title</th>
					<th>Date/Time finished</th>
					<th>Full Test Title</th>
					<th>Number of Tests</th>
					<th>Version Tested Against</th>
					<th>Model</th>
					<th>Percent Passed</th>
					</tr>";
					$counter= 0;
					while($counter<$amount)
					{
					$row = mysqli_fetch_array($result);
					echo "<tr>";
					echo "<td>" . $row['ProjectTitle'] . "</td>";
					echo "<td>" . $row['DateTime'] . "</td>";
					echo "<td>" . $row['FullTestTitle'] . "</td>";
					echo "<td>" . $row['NumberTests'] . "</td>";
					echo "<td>" . $row['VersionAgainst'] . "</td>";
					echo "<td>" . $row['TestTitle'] . "</td>";
					if ($row['Percent'] < "90") {
						echo "<td><font color='red'>" . $row['Percent'] . "</td>";
					} else {
						echo "<td><font color='green'>" . $row['Percent'] . "</td>";
					}
					//echo "<td>" . $row['TestTitle'] . "</td>"; //temporarily leave out test title row					
					echo "</tr>";

					$counter++;
					}
					echo "</table>";

					mysqli_close($con);
					?>
						</div>
					</div>

	</body>
</html>