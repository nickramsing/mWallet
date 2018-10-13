<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="description" content="">
    <meta name="keywords" content="">
    <!-- From Simple Grid: makes responsive to mobile
	<meta name="viewport" content="width=device-width, initial-scale=1" > -->
    <title>mWallet message test</title>

    <!-- link to javascript files -->
    <script type="text/javascript" src="{{ get_url('static', filename='jquery-1.11.1.js') }}" ></script>
    <script type="text/javascript" src="{{ get_url('static', filename='jquery-ui.1.10.3.js') }}" ></script>
    <!-- link to stylesheet files -->
    <link rel="stylesheet" type="text/css" href="{{ get_url('static', filename='jquery-ui.1.10.3.css') }}" />
    <link rel="stylesheet" type="text/css" href="{{ get_url('static', filename='layout.css') }}" />

    <script type="text/javascript">
	</script>

</head>


<body>
<div class="wrapper">
    <div class="box header">Header</div>
    <div class="box title">mWallet Test response</div>
    <div class="box content_form">Welcome to mWallet Test!
        <form action="/testmessage">
            <input class="submitButton" type="submit" value="Go to test message page" />
        </form>
    </div>
    <div class="box content_response">Response text: [none at this time]</div>
    <div class="box footer">Footer: testing response</div>
</div>

</body>

</html>