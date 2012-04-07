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

var deletebox = '<svg height="20" version="1.1" width="20" xmlns="http://www.w3.org/2000/svg" style="overflow-x: hidden; overflow-y: hidden; position: absolute; top: 20px; "><ellipse cx="10" cy="10" rx="10" ry="10" fill="#323432" stroke="#000" style="cursor: pointer; " stroke-width="0" class="remove"></ellipse><path style="cursor: pointer; " fill="#fefefe" stroke="#000000" d="M8.5,8.5V3.5H11.5V8.5H16.5V11.5H11.5V16.5H8.5V11.5H3.5V8.5Z" stroke-width="0" transform="matrix(0.7071,0.7071,-0.7071,0.7071,10,-4.1421)" class="remove"></path></svg>'
var star = '<svg class="staricon" height="20px" width="20px"><path style="opacity: 1; fill-opacity: 1; stroke-opacity: 0; cursor: default; stroke-width: 0;" fill="rgb(60,62,60)"  d="M9,8l0,0,3,-8l0,0,3,8h7l0,0,-6,4l0,0,2,8l0,0,-6,-6l0,0,-6,6l0,0,2,-8l0,0,-6,-4z" opacity="1" stroke-opacity="1"></path></svg>';
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
    // $("#autocomplete").append('<tr id="' + id_for_course(course) + '"><td class="coursecode">' +
    //     '<strong>' + course.code + "</strong>" + "</td><td>" +
    //     course.name+'<font class="professor">' + "\t"+course.instructor + '</font></td></tr>');
    // $("#"+id_for_course(course)).append("<td class='deletebox'>"+deletebox+"</td>");
    
    // $("#"+id_for_course(course)+" .remove").click(function (evt) {
    $("#autocomplete").append('<tr id="' + course.id + '"><td>' +
        course.name+'</td></tr>');
    deletebtn("#" + course.id);
    $("form#course_ratings").append('<input id="'+ course.id + '" type="hidden" name="'+ course.id + '" value="0">');
    $("#" + course.id + " .remove").click(function (evt) {
        remove_course(course_for_id(this.parentNode.parentNode.parentNode.id));
    });
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