//Create a constructor function and put all relevant properties and 
// functions inside it.
function Suggest() 
{
	//:( .. Save "this"
	othis = this;
	
	this.xhr = new XMLHttpRequest(); // object to make the AJAX call
	
	//A document.getElementById() NOW will fail. We can do it later
	this.course = null;
	this.div = null;
	
	//Define a timer for the "Suggest" functionality
	this.timer = null;
	
	//This function will get called when the user "keys" up. 
	// We need to decide whether to go to server at all?? Or fetch 
	// from cache or (do we need to do anything at all????)
	
	this.getElectiveList = function()
	{
		//If there is a timer already registered, clear that and create a 
		// new one, 1 second from now (our pause is 1 second)
		// Else, just create a timer for 1s ( first time keyup)
		if(this.timer)
		{
			clearTimeout(this.timer);
		}

		//In any case
		this.timer = setTimeout(this.fetchcourse, 1000);
	}
	
	this.fetchcourse = function()
	{
		//Check if the text box (course) is empty.
		// This can happen if the user has pressed backspace repeatedly
		// and cleared the text field
		
		othis.course = document.getElementById("search_box");
		othis.div = document.getElementById("suggestions");
		if(othis.course.value == "")
		{
			//There is nothing to do
			othis.div.innerHTML = "";
			othis.div.style.display = "none";
			return;
		}
		
		// Else we have two choices. One, we can check in our cache.
		// If we had previously searched for this coursepart, we will find it
		// in our cache. We load it from there. Else, we have no option 
		// but to go to the server
		else
		{
			urlstr = "/getElectiveNames?coursepart=" + othis.course.value;
			if(localStorage[urlstr])
			{
				othis.fillcourses(JSON.parse(localStorage[urlstr]));
			}
			else
			{
				//Now we have to go to the server
				othis.xhr.onreadystatechange = othis.populatecourses;
				
				// Open a GET connection
				othis.xhr.open("GET", "/getElectiveNames?coursepart=" + othis.course.value, true);
				
				othis.xhr.send();
	
			}
		}
	}
	
	this.populatecourses = function()
	{
		if(this.readyState == 4 && this.status == 200)
		{
			courses = JSON.parse(this.responseText);
			
			//Maybe there were no suggestions.
			if(courses.length == 0)
			{
				othis.course.classList.add = "notfound";
				othis.div.style.display = "none";
			}
			else//there are some suggestions
			{
				othis.course.classList.add = "found";
				
				//Add it to the browser cache. We will use localStorage
				localStorage[this.responseURL] = this.responseText;
				
				othis.fillcourses(courses);
			}
		}
	}
	
	this.fillcourses = function(courses)
	{
		othis.div.innerHTML = "";
		for(i=0;i<courses.length;i++)
		{
			newdiv = document.createElement("div");
			newdiv.innerHTML = courses[i]['c_name'];
			newdiv.classList.add = "suggest";
			othis.div.appendChild(newdiv);
			
			//Now we need to register the event where the div is "Selected"
			// We use "onclick"
			newdiv.onclick = othis.setcourse;
		}
		othis.div.style.display = "block";
	}
	
	//Function to set the selected value inside the textbox
	// After setting the value, clear the "div" container
	
	this.setcourse = function(event)
	{
		othis.course.value = event.target.innerHTML;
	
		//Clear the div
		othis.div.innerHTML = "";
		othis.div.style.display = "none";
	}
}

//Create the object using the constructor
obj = new Suggest();