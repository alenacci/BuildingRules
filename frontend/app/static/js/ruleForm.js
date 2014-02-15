var ruleNumber = 1;

function updatePriority(value)
{
	priorityTextBox = document.getElementById('priorityTextBox');
	priorityTextBox.value = value;
}

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

function hideAllTriggerSubBox()
{

	groupId = 0;
	hide('temperature_box_' + groupId);
	hide('time_box_' + groupId);
	hide('day_box_' + groupId);
	hide('date_box_' + groupId);	
}

function hideAllActionSubBox()
{
	hide('action_temperature_box');
	hide('action_humidity_box');
}

function getTriggerCategory(triggerText)
{

	if (triggerText == "room temperature is between") return "TEMPERATURE";
	if (triggerText == "external temperature is between") return "TEMPERATURE";
	if (triggerText == "time is between") return "TIME";
	if (triggerText == "the date is between") return "DAY";

	return "DEFAULT";
}

function getActionCategory(actionText)
{

	if (actionText == "Select an action") return "NOT_VALID";
	if (actionText == "set temperature between") return "TEMPERATURE";
	if (actionText == "set humidity between") return "HUMIDITY";

	return "DEFAULT";
}


function triggerSelected()
{

	groupId = 0;

	triggerBox = document.getElementById("trigger_" + groupId)
	triggerText = triggerBox.options[triggerBox.selectedIndex].text;

	hideAllTriggerSubBox();

	triggerCategory = getTriggerCategory(triggerText);

	if (triggerCategory == "TEMPERATURE")	
	{
		show('temperature_box_' + groupId);
	}

	if (triggerCategory == "TIME")	
	{
		show('time_box_' + groupId);
	}

	if (triggerCategory == "DATE")	
	{
		show('date_box_' + groupId);
	}

	if (triggerCategory == "DAY")	
	{
		show('day_box_' + groupId);
	}


}

function actionSelected()
{
	actionBox = document.getElementById("action_" + groupId);
	actionText = actionBox.options[actionBox.selectedIndex].text;

	actionCategory = getActionCategory(actionText);

	hideAllActionSubBox();

	
	if (actionCategory == "DEFAULT")
	{
		compose();
	}

	if (actionCategory == "TEMPERATURE")
	{
		show('action_temperature_box');
	}

	if (actionCategory == "HUMIDITY")
	{
		show('action_humidity_box');
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

	triggerBox = document.getElementById("trigger_" + groupId);
	actionBox = document.getElementById("action_" + groupId);

	temperatureFrom = document.getElementById("temperature_from_" + groupId);
	temperatureTo = document.getElementById("temperature_to_" + groupId);

	timeFrom = document.getElementById("time_from_" + groupId);
	timeTo = document.getElementById("time_to_" + groupId);

	dateDayFrom = document.getElementById("date_day_from_" + groupId);
	dateMonthFrom = document.getElementById("date_month_from_" + groupId);
	dateDayTo = document.getElementById("date_day_to_" + groupId);
	dateMonthTo = document.getElementById("date_month_to_" + groupId);

	day = document.getElementById("day_" + groupId);

	ruleBody = document.getElementById('ruleBody');

	triggerText = triggerBox.options[triggerBox.selectedIndex].text;
	actionText = actionBox.options[actionBox.selectedIndex].text;



	triggerCategory = getTriggerCategory(triggerText);


	if (triggerCategory == "DEFAULT"){
		ruleBody.value = "if " + triggerText + " then " + actionText;
	}

	if (triggerCategory == "TEMPERATURE")
	{
		tempFromText = temperatureFrom.options[temperatureFrom.selectedIndex].text;
		tempToText = temperatureTo.options[temperatureTo.selectedIndex].text;
		ruleBody.value = "if " + triggerText + " " + tempFromText + " and " + tempToText + " then " + actionText;	
	}

	if (triggerCategory == "TIME")
	{
		timeFromText = timeFrom.options[timeFrom.selectedIndex].text;
		timeToText = timeTo.options[timeTo.selectedIndex].text;
		ruleBody.value =  "if " + triggerText + " " + timeFromText + " and " + timeToText + " then " + actionText;	
	}

	if (triggerCategory == "DATE")
	{
		dateDayFromText = dateDayFrom.options[dateDayFrom.selectedIndex].text;
		dateMonthFromText = dateMonthFrom.options[dateMonthFrom.selectedIndex].text;
		dateDayToText = dateDayTo.options[dateDayTo.selectedIndex].text;
		dateMonthToText = dateMonthTo.options[dateMonthTo.selectedIndex].text;

		ruleBody.value =  "if " + triggerText + " " + dateDayFromText + "/" + dateMonthFromText + " and " + dateDayToText + "/" + dateMonthToText + " then " + actionText;	
	}

	if (triggerCategory == "DAY")
	{
		dayText = day.options[day.selectedIndex].text;
		ruleBody.value =  "if " + triggerText + " " + dayText + " then " + actionText;	
	}


}


function updateTemperatureSetpoint()
{
	
	desiredValue = document.getElementById("desired_temperature");
	rangeValue = document.getElementById("accepted_temperature_range");

	alert(desiredValue.value);
	alert(desiredValue.value);

	


}

function ruleBodyAlert()
{
	alert("Please use the menu below to compose the rule! :) ")
	
}

function init()
{

	hideAllTriggerSubBox();
	hideAllActionSubBox();
}


