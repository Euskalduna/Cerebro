function mostrar1() {
	
    var numVar = $("#option").val();
	$("#actividades").text("");
	
		if(numVar == 2){
			
			$("#actividades").append("<label>Numero de variables</label><br><input id=variableNum type='text' name='variableNum' value=''><br><br>");
						
		}else if( numVar ==1){
			
			$("#actividades").append("<label>Numero de actividades</label><br><input id='activityNum' type='text'><br><br>");
			
		}
		
		
		$('#variableNum').focusout(function(e) {
	
				var numVar = $('#variableNum').val();
				$("#variables").text("");
				for(var i=0;i<numVar;i++){			
					$("#variables").append("<label>Nombre de variable "+(i+1)+":</label><br><input name=var"+(i+1)+"Name type='text'><br>");
					$("#variables").append("<label>Tipo de variable "+(i+1)+":</label><br><input name=var"+(i+1)+"Type type='text'><br><br>");
					
				}
				
			});

			$('#numDeveloper').focusout(function(e) {
	
				var numVar = $('#numDeveloper').val();
				$("#desarrolladores").text("");
				for(var i=0;i<numVar;i++){			
					$("#desarrolladores").append("<label>Nombre del desarrollador "+(i+1)+":</label><br><input name=dev"+(i+1)+"Name type='text'><br>");
					$("#desarrolladores").append("<label>Apellido del desarrollador "+(i+1)+":</label><br><input name=dev"+(i+1)+"LastName type='text'><br><br>");
					
				}
				
			});		
}

