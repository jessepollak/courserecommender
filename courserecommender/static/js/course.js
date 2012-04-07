// ┌────────────────────────────────────────────────────────────────────┐ \\
// │ JAVASCRIPT FOR COURSE RECOMMENDER SITE                             │ \\
// ├────────────────────────────────────────────────────────────────────┤ \\
// │ THE NEURO LOUNGE TEAM                     						    │ \\
// │ Jesse, Joseph, Jonathan & Michael                                  │ \\
// └────────────────────────────────────────────────────────────────────┘ \\

function course(code, name, instructor) {
	this.code       = code       || "College 101";
	this.name       = name 		 || "Unknown"    ;
	this.instructor = instructor || "Staff"      ;
    this.toString = function () {
    	return this.code+" - "+this.name;   
    };
}

var database = [
new course("ENGL 101","A brief history of American Classics","Prof Byzarre"),
new course("PSYCH 22","The Brain : an introspection","Mr Sandman"),
new course("MATH 952","Simple Logic","Dr. Raiman"),
new course("PE 12 PZ","Bungee Jumping","Antoine Domain"),
new course("PE 11","Fly Fishing with Ralp","Evil Eye Bob"),
new course("ENGL 250","The Great Minds of Jenzabar : a review by Joseph L.","Joseph Long"),
new course("CS 12","How to simple things in Python without Rails","Dr. M. Maltese"),
new course("ENGL 55","A brief history of American Classics","Prof Byzarre"),
new course("ENG 101","Material structures in outer space","Prof Orbit"),
new course("MATH 570","Complexifications","Prof Slitherin"),
new course("ID 1","Seminars by Seminaries","Prof Closing"),
new course("ANTHRO 250","The indigeneous cultures of Tanzania","Dr. Jones"),
new course("CS 909","API Design","Dr. M. Maltese"),
new course("MEDIA 99","ESCAPING the usual GOTCHAS","Bruce Wayne"),
new course("HIST 150","From Randomness to Importations","Prof Jesse"),
new course("BIO 105","Friction between ambiguous cellular bodies","Prof Synecdoche"),
new course("CHEM 51","Making Nitro","Prof Swarthmore"),
new course("PHYS 128","Arduinos & Piano Playing","Prof Raphie"),
new course("ART 15","The grand use of Raphael JS in the world of Modern Art: a review","Dr. M. Maltese")
];

$(".staricon").live('mouseover', function() {
	var starvalue = $(this).attr('strength');
	console.log($(this).parent().children().length);
	for (var i =0;i<$(this).parent().children().length;i++){
			console.log($(this).parent().children()[i].type == "path");
		}
		
		// $(this).parent().children()[i].css({fill:"#ea4c89"})
	});

var selected_courses = [];

function course_for_id(id) {
    for (var i = 0; i < selected_courses.length; i++) {
        if(selected_courses[i].id == id) {
            return selected_courses[i];
        }
    }
    return false; // if no selected course matches
}

function remove_course(course) {
    $("#"+course.id).remove();
    $("#rating_"+course.id).remove();
    selected_courses.splice(selected_courses.indexOf(course), 1);
}

function select_course(course) {
    for (var i = 0; i < selected_courses.length; i++) {
        if(selected_courses[i].id == course.id) {
            return false;
        }
    }
    selected_courses.push(course);
    $("#autocomplete").append('<tr id="' + course.id + '"><td>' +
        course.name+'</td></tr>');
    deletebtn("#" + course.id);
    $("form#course_ratings").append('<input id="'+ course.id + '" type="hidden" name="'+ course.id + '" value="0">');
    $("#" + course.id + " .remove").click(function (evt) {
        remove_course(course_for_id(this.parentNode.parentNode.parentNode.id));
    });
}

function deletebtn(somedivid) {
	var target = $(somedivid).append("<td class='removebox'></td>").find("td")[1];
	var canvas = Raphael($("body"), 20,20);
	target.appendChild(canvas.canvas);
	var circ = canvas.ellipse(10,10,10,10).attr({fill:"rgb(50,52,50)", "stroke-width": 0,cursor: "pointer"});
	var icon = canvas.path("m"+(8.5)+","+(8.5)+"v-5h3v5h5v3h-5v5h-3v-5h-5v-3z").attr({fill:"rgb(254,254,254)", "stroke-width": 0,cursor: "pointer"}).transform("r45");
	icon[0].setAttribute("class","remove");
	circ[0].setAttribute("class","remove");
}

$("document").ready( function () {
	for (var i=0; i<database.length;i++){
		console.log(database[i]+"");
	}
	
	autocompletions = [];
	for (var i = 0; i < database.length; i++) {
	    autocompletions.push({
	        label: database[i].code + ' - ' + database[i].name + ' - ' + database[i].instructor,
	        value: database[i]
        });
	}
	
	$("#userinput input[type='text']").autocomplete({
	    source: '/courses',
	    autoFocus: true,
	    search: function (event, ui) { console.log("Searching..."); },
	    select: function (event, ui) {
	        var course =  {"id": ui.item.value, "name": ui.item.label};
	        select_course(course);
	        $("#userinput input").val('');
	        return false;
	    }
	});
})