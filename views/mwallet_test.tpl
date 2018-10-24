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

        
        //var jsondata = '{{response}}'.replace(/&quot;/g, '"');
        var responsetext = '{{response}}';
        //alert(responsetext);
	
	</script>	
	
  </head>
  
  
  <body>
        <div class="wrapper">
        <div class="box header">Header</div>
        <div class="box title">mWallet Test response</div>
        <!-- Exercise input content -->
        <div class="box content_form">Enter message information:
          <form id="messageinput" action="testmessage" method="POST" accept-charset="utf-8">
		  	 	   <label for="account">Account:</label>
			 	     <select id="account" name="account" type="text" placeholder="Enter the account number">
	 		 		     <option value ="+14437669188">Nick: 443-766-9188</option>
			 		      <option value ="+14437669061">Becky: 443-766-9061</option>
                         <option value ="+14437669053">Jadon: 443-766-9053</option>
				      </select>
  	 			   <label for="message">Message:</label>
	 			     <input id="message" name="message" type="text" placeholder="Enter the SMS message">
				      <input class="submitButton" type="submit" value="Submit"> 
          </form>  
        </div>
        <div class="box content_response">Response text: {{response}}</div>
        <div class="box footer">Footer: testing response</div>
      </div>
 
 </body>
  
</html>