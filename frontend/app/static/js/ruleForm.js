
var ruleNumber = 1;

function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

function goCdegree(){
	this.location = "index_celsius.html?usrcat=" + getParameterByName('usrcat')
}

function goFdegree(){
	this.location = "index.html?usrcat=" + getParameterByName('usrcat')
}


function show(elementId)
{
	document.getElementById(elementId).style.display = "block";
}

function hide(elementId)
{
	document.getElementById(elementId).style.display = "none";
}

function triggerSelected(groupId)
{

	triggerBox = document.getElementById("trigger_" + groupId)
	index = triggerBox.selectedIndex;
	
	
	hide('temperature_box_' + groupId);
	hide('time_box_' + groupId);
	hide('day_box_' + groupId);
	hide('date_box_' + groupId);

	if (index == 3 || index == 4)	
	{
		show('temperature_box_' + groupId);
	}

	if (index == 5)	
	{
		show('time_box_' + groupId);
	}

	if (index == 6)	
	{
		show('date_box_' + groupId);
	}


	if (index == 7)	
	{
		show('day_box_' + groupId);
	}


}

function addRule()
{

	if (ruleNumber == 19)
	{
		alert("No more rule available!");
		return
	}

	ruleNumber += 1;

	show('div_rule_' + ruleNumber);
	show('hr_rule_' + ruleNumber);

}

function removeRule()
{

	if (ruleNumber == 0)
	{
		alert("You cannot remove rule #1!");
		return
	}

	
	hide('div_rule_' + ruleNumber);
	hide('hr_rule_' + ruleNumber);

	ruleNumber -= 1;

}

function goToConfirmPage() {
    setTimeout(function () {
        this.location = "thanks.html"
    }, 4000);
}

function compose()
{

	groupId = 0;

	triggerBox = document.getElementById("trigger_" + groupId)
	actionBox = document.getElementById("action_" + groupId)

	temperatureFrom = document.getElementById("temperature_from_" + groupId);
	temperatureTo = document.getElementById("temperature_to_" + groupId);

	timeFrom = document.getElementById("time_from_" + groupId);
	timeTo = document.getElementById("time_to_" + groupId);

	dateDayFrom = document.getElementById("date_day_from_" + groupId);
	dateMonthFrom = document.getElementById("date_month_from_" + groupId);
	dateDayTo = document.getElementById("date_day_to_" + groupId);
	dateMonthTo = document.getElementById("date_month_to_" + groupId);

	day = document.getElementById("day_" + groupId);

	index = triggerBox.selectedIndex;

	ruleBody = document.getElementById('ruleBody');

	triggerText = triggerBox.options[triggerBox.selectedIndex].text;
	actionText = actionBox.options[actionBox.selectedIndex].text;


	if (index == 1 || index == 2 || index == 8 || index == 9 || index == 10){
		ruleBody.value = "if " + triggerText + " then " + actionText;
	}

	if (index == 3 || index == 4)
	{
		tempFromText = temperatureFrom.options[temperatureFrom.selectedIndex].text;
		tempToText = temperatureTo.options[temperatureTo.selectedIndex].text;
		ruleBody.value = "if " + triggerText + " " + tempFromText + " and " + tempToText + " then " + actionText;	
	}

	if (index == 5)
	{
		timeFromText = timeFrom.options[timeFrom.selectedIndex].text;
		timeToText = timeTo.options[timeTo.selectedIndex].text;
		ruleBody.value =  "if " + triggerText + " " + timeFromText + " and " + timeToText + " then " + actionText;	
	}

	if (index == 6)
	{
		dateDayFromText = dateDayFrom.options[dateDayFrom.selectedIndex].text;
		dateMonthFromText = dateMonthFrom.options[dateMonthFrom.selectedIndex].text;
		dateDayToText = dateDayTo.options[dateDayTo.selectedIndex].text;
		dateMonthToText = dateMonthTo.options[dateMonthTo.selectedIndex].text;

		ruleBody.value =  "if " + triggerText + " " + dateDayFromText + "/" + dateMonthFromText + " and " + dateDayToText + "/" + dateMonthToText + " then " + actionText;	
	}

	if (index == 7)
	{
		dayText = day.options[day.selectedIndex].text;
		ruleBody.value =  "if " + triggerText + " " + dayText + " then " + actionText;	
	}


}

function ruleBodyAlert()
{
	alert("Please use the menu below to compose the rule! :) ")
	
}

function init()
{

	for (var i=0; i<= 19; i++)
	{
		hide('temperature_box_' + i);
		hide('time_box_' + i);
		hide('day_box_' + i);
		hide('date_box_' + i);
		
	}


}


