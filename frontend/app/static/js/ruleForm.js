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

	humiditySetpointMinBox = document.getElementById("humiditySetpoint_min");
	humiditySetpointMaxBox = document.getElementById("humiditySetpoint_max");
	tempSetpointMinBox = document.getElementById("tempSetpoint_min");
	tempSetpointMaxBox = document.getElementById("tempSetpoint_max");


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
	actionCategory = getActionCategory(actionText);


	antecent = ""
	consequent = ""


	if (triggerCategory == "DEFAULT"){
		antecent = "if " + triggerText;
	}

	if (triggerCategory == "TEMPERATURE")
	{
		tempFromText = temperatureFrom.options[temperatureFrom.selectedIndex].text;
		tempToText = temperatureTo.options[temperatureTo.selectedIndex].text;
		antecent = "if " + triggerText + " " + tempFromText + " and " + tempToText;
	}

	if (triggerCategory == "TIME")
	{
		timeFromText = timeFrom.options[timeFrom.selectedIndex].text;
		timeToText = timeTo.options[timeTo.selectedIndex].text;
		antecent=  "if " + triggerText + " " + timeFromText + " and " + timeToText;
	}

	if (triggerCategory == "DATE")
	{
		dateDayFromText = dateDayFrom.options[dateDayFrom.selectedIndex].text;
		dateMonthFromText = dateMonthFrom.options[dateMonthFrom.selectedIndex].text;
		dateDayToText = dateDayTo.options[dateDayTo.selectedIndex].text;
		dateMonthToText = dateMonthTo.options[dateMonthTo.selectedIndex].text;

		antecent =  "if " + triggerText + " " + dateDayFromText + "/" + dateMonthFromText + " and " + dateDayToText + "/" + dateMonthToText;
	}

	if (triggerCategory == "DAY")
	{
		dayText = day.options[day.selectedIndex].text;
		antecent=  "if " + triggerText + " " + dayText;
	}

	if (actionCategory == "DEFAULT")
	{
		consequent = actionText;
	}

	if (actionCategory == "TEMPERATURE")
	{
		consequent = actionText + " " + tempSetpointMinBox.value + " and " + tempSetpointMaxBox.value;
	}



	if (actionCategory == "HUMIDITY")
	{
		consequent = actionText + " " + humiditySetpointMinBox.value + " and " + humiditySetpointMaxBox.value;
	}


	ruleBody.value = antecent + " then " + consequent


}


function updateHumiditySetpoint()
{

	unit = "%"
	
	desiredValueBox = document.getElementById("desired_humidity");
	rangeValueBox = document.getElementById("accepted_humidity_range");
	humiditySetpointMinBox = document.getElementById("humiditySetpoint_min");
	humiditySetpointMaxBox = document.getElementById("humiditySetpoint_max");

	maxAllowedTemp = desiredValueBox.max;
	minAllowedTemp = desiredValueBox.min;

	desiredValue = desiredValueBox.value;
	rangeValue = rangeValueBox.value;

	humiditySetpointMin = parseInt(desiredValue) - parseInt(rangeValue);
	humiditySetpointMax = parseInt(desiredValue) + parseInt(rangeValue);

	orangeArea = humiditySetpointMin - minAllowedTemp;
	orangeArea_perc = parseInt(rangeValue) * 5;

	
	document.getElementById("humiditySetpoint_bar_value").width = orangeArea_perc + "%" ;
	
	document.getElementById("humiditySetpoint_bar_min").innerHTML = humiditySetpointMin + unit;
	document.getElementById("humiditySetpoint_bar_value").innerHTML = desiredValue + unit;
	document.getElementById("humiditySetpoint_bar_max").innerHTML = humiditySetpointMax + unit;
	
	humiditySetpointMinBox.value = humiditySetpointMin + unit;
	humiditySetpointMaxBox.value = humiditySetpointMax + unit;

	compose();


}

function updateTemperatureSetpoint()
{

	unit = "F"
	
	desiredValueBox = document.getElementById("desired_temperature");
	rangeValueBox = document.getElementById("accepted_temperature_range");
	tempSetpointMinBox = document.getElementById("tempSetpoint_min");
	tempSetpointMaxBox = document.getElementById("tempSetpoint_max");

	maxAllowedTemp = desiredValueBox.max;
	minAllowedTemp = desiredValueBox.min;

	desiredValue = desiredValueBox.value;
	rangeValue = rangeValueBox.value;

	tempSetpointMin = parseInt(desiredValue) - parseInt(rangeValue);
	tempSetpointMax = parseInt(desiredValue) + parseInt(rangeValue);

	orangeArea = tempSetpointMin - minAllowedTemp;
	orangeArea_perc = parseInt(rangeValue) * 5;

	
	document.getElementById("tempSetpoint_bar_value").width = orangeArea_perc + "%" ;
	
	document.getElementById("tempSetpoint_bar_min").innerHTML = tempSetpointMin + unit;
	document.getElementById("tempSetpoint_bar_value").innerHTML = desiredValue + unit;
	document.getElementById("tempSetpoint_bar_max").innerHTML = tempSetpointMax + unit;
	
	tempSetpointMinBox.value = tempSetpointMin + unit;
	tempSetpointMaxBox.value = tempSetpointMax + unit;

	compose();


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


