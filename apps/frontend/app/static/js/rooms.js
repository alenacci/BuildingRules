
ruleCategories = [];
currentCategory = "SHOWALL";
currentDayPeriod = "ALLPERIOD";

function hideClass(className)
{
	var elements = document.getElementsByClassName(className), i;

	for (i = 0; i < elements.length; i ++) {
	    elements[i].style.display = 'none';
	}
}

function showClass(className)
{
	var elements = document.getElementsByClassName(className), i;

	for (i = 0; i < elements.length; i ++) {
	    elements[i].style.display = 'block';
	}
}

function filterByDayPeriod(roomName, dayPeriod,fromCategoryFilter)
{

    currentDayPeriod = dayPeriod;
    if (!fromCategoryFilter) {
        filterByRuleCategory(roomName,currentCategory);
    }
    var i;


	if (dayPeriod == "ALLPERIOD")
	{
		document.getElementById("btn_" + roomName + "_NIGHT").setAttribute("class", "btn");
        document.getElementById("btn_" + roomName + "_EVENING").setAttribute("class", "btn");
        document.getElementById("btn_" + roomName + "_AFTERNOON").setAttribute("class", "btn");
        document.getElementById("btn_" + roomName + "_MORNING").setAttribute("class", "btn");
		document.getElementById("btn_" + roomName + "_ALLPERIOD").setAttribute("class", "btn active");

	} else if (dayPeriod == "MORNING")
	{

        var elements = document.getElementsByClassName('rule_' + roomName + "_AFTERNOON" );
        for (i = 0; i < elements.length; i ++) {
            if (elements[i].style.display == "block"){
                elements[i].style.display = "none"
            }
        }

        elements = document.getElementsByClassName('rule_' + roomName + "_EVENING" );
        for (i = 0; i < elements.length; i ++) {
            if (elements[i].style.display == "block"){
                elements[i].style.display = "none"
            }
        }

        elements = document.getElementsByClassName('rule_' + roomName + "_NIGHT" );
        for (i = 0; i < elements.length; i ++) {
            if (elements[i].style.display == "block"){
                elements[i].style.display = "none"
            }
        }

        elements = document.getElementsByClassName('rule_' + roomName + "_ALLPERIOD" );
        for (i = 0; i < elements.length; i ++) {
            if (elements[i].style.display == "block"){
                elements[i].style.display = "none"
            }
        }

		document.getElementById("btn_" + roomName + "_NIGHT").setAttribute("class", "btn");
        document.getElementById("btn_" + roomName + "_EVENING").setAttribute("class", "btn");
        document.getElementById("btn_" + roomName + "_AFTERNOON").setAttribute("class", "btn");
        document.getElementById("btn_" + roomName + "_MORNING").setAttribute("class", "btn active");
		document.getElementById("btn_" + roomName + "_ALLPERIOD").setAttribute("class", "btn");

	} else if (dayPeriod == "AFTERNOON")
	{
        var elements = document.getElementsByClassName('rule_' + roomName + "_MORNING");
        for (i = 0; i < elements.length; i ++) {
            if (elements[i].style.display == "block"){
                elements[i].style.display = "none"
            }
        }

        elements = document.getElementsByClassName('rule_' + roomName + "_EVENING" );
        for (var i = 0; i < elements.length; i ++) {
            if (elements[i].style.display == "block"){
                elements[i].style.display = "none"
            }
        }

        elements = document.getElementsByClassName('rule_' + roomName + "_NIGHT" );
        for (i = 0; i < elements.length; i ++) {
            if (elements[i].style.display == "block"){
                elements[i].style.display = "none"
            }
        }

        elements = document.getElementsByClassName('rule_' + roomName + "_ALLPERIOD" );
        for ( i = 0; i < elements.length; i ++) {
            if (elements[i].style.display == "block"){
                elements[i].style.display = "none"
            }
        }

		document.getElementById("btn_" + roomName + "_NIGHT").setAttribute("class", "btn");
        document.getElementById("btn_" + roomName + "_EVENING").setAttribute("class", "btn");
        document.getElementById("btn_" + roomName + "_AFTERNOON").setAttribute("class", "btn active");
        document.getElementById("btn_" + roomName + "_MORNING").setAttribute("class", "btn");
		document.getElementById("btn_" + roomName + "_ALLPERIOD").setAttribute("class", "btn");

	} else if (dayPeriod == "EVENING")
	{
        var elements = document.getElementsByClassName('rule_' + roomName + "_MORNING");
        for ( i = 0; i < elements.length; i ++) {
            if (elements[i].style.display == "block"){
                elements[i].style.display = "none"
            }
        }

        elements = document.getElementsByClassName('rule_' + roomName + "_AFTERNOON" );
        for ( i = 0; i < elements.length; i ++) {
            if (elements[i].style.display == "block"){
                elements[i].style.display = "none"
            }
        }

        elements = document.getElementsByClassName('rule_' + roomName + "_NIGHT" );
        for ( i = 0; i < elements.length; i ++) {
            if (elements[i].style.display == "block"){
                elements[i].style.display = "none"
            }
        }

        elements = document.getElementsByClassName('rule_' + roomName + "_ALLPERIOD" );
        for ( i = 0; i < elements.length; i ++) {
            if (elements[i].style.display == "block"){
                elements[i].style.display = "none"
            }
        }

		document.getElementById("btn_" + roomName + "_NIGHT").setAttribute("class", "btn");
        document.getElementById("btn_" + roomName + "_EVENING").setAttribute("class", "btn active");
        document.getElementById("btn_" + roomName + "_AFTERNOON").setAttribute("class", "btn");
        document.getElementById("btn_" + roomName + "_MORNING").setAttribute("class", "btn");
		document.getElementById("btn_" + roomName + "_ALLPERIOD").setAttribute("class", "btn");

	}
    else if (dayPeriod == "NIGHT")
	{
        var elements = document.getElementsByClassName('rule_' + roomName + "_MORNING");
        for ( i = 0; i < elements.length; i ++) {
            if (elements[i].style.display == "block"){
                elements[i].style.display = "none"
            }
        }

        elements = document.getElementsByClassName('rule_' + roomName + "_AFTERNOON" );
        for ( i = 0; i < elements.length; i ++) {
            if (elements[i].style.display == "block"){
                elements[i].style.display = "none"
            }
        }

        elements = document.getElementsByClassName('rule_' + roomName + "_EVENING" );
        for ( i = 0; i < elements.length; i ++) {
            if (elements[i].style.display == "block"){
                elements[i].style.display = "none"
            }
        }

        elements = document.getElementsByClassName('rule_' + roomName + "_ALLPERIOD" );
        for ( i = 0; i < elements.length; i ++) {
            if (elements[i].style.display == "block"){
                elements[i].style.display = "none"
            }
        }

		document.getElementById("btn_" + roomName + "_NIGHT").setAttribute("class", "btn active");
        document.getElementById("btn_" + roomName + "_EVENING").setAttribute("class", "btn");
        document.getElementById("btn_" + roomName + "_AFTERNOON").setAttribute("class", "btn");
        document.getElementById("btn_" + roomName + "_MORNING").setAttribute("class", "btn");
		document.getElementById("btn_" + roomName + "_ALLPERIOD").setAttribute("class", "btn");

	}
}

function filterByRuleCategory(roomName, ruleCategory,fromDayPeriodFilter)
{
    currentCategory = ruleCategory;

	if (ruleCategory == "SHOWALL")
	{
		for (var i = 0; i < ruleCategories.length; i ++)
		{
			showClass('rule_' + roomName + "_" + ruleCategories[i]);
			document.getElementById("btn_" + roomName + "_" + ruleCategories[i]).setAttribute("class", "btn");
		}
		
		document.getElementById("btn_" + roomName + "_SHOWALL").setAttribute("class", "btn active");

	} else {

		document.getElementById("btn_" + roomName + "_SHOWALL").setAttribute("class", "btn");

		for (var i = 0; i < ruleCategories.length; i ++)
		{
			hideClass('rule_' + roomName + "_" + ruleCategories[i]);
			document.getElementById("btn_" + roomName + "_" + ruleCategories[i]).setAttribute("class", "btn");
		}
		showClass('rule_' + roomName + "_" + ruleCategory);
		
		document.getElementById("btn_" + roomName + "_" + ruleCategory).setAttribute("class", "btn active");
	}

    if (!fromDayPeriodFilter) {
        filterByDayPeriod(roomName, currentDayPeriod, true);
    }

}


function show(elementId)
{
	document.getElementById(elementId).style.display = "block";
}

function hide(elementId)
{
	document.getElementById(elementId).style.display = "none";
}

function hideAll()
{
	hide("btnShowMaps");
	hide("btnHideMaps");
	hide("btnShowThMaps");
	hide("btnShowAccMaps");
	hide("accessMap");
	hide("thZoneMap");
}

function hideMaps()
{
	hideAll();
	show("btnShowMaps");

}

function showMaps()
{
	hideAll();
	showAccessMaps();
}

function showAccessMaps()
{
	hideAll();
	show("accessMap");
	show("btnShowThMaps");
	show("btnHideMaps");
}

function showThermalZoneMaps()
{
	hideAll();
	show("thZoneMap");
	show("btnShowAccMaps");
	show("btnHideMaps");
}

function hideMTurk()
{
	hide('mturkPanel');
	hide('btnHideMTurk');
	show('btnShowMTurk');
}

function showMTurk()
{
	show('mturkPanel');
	hide('btnShowMTurk');
	show('btnHideMTurk');
}

function init()
{
	showAccessMaps();
	showMTurk();
}

function showGame()
{
	show('gameFrame');
    hide('btnShowGame');
	show('btnHideGame');
}

function hideGame()
{
	hide('gameFrame');
    hide('btnHideGame');
    show('btnShowGame');

}
